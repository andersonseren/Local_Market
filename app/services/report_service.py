from app.extensions import db
from app.models.user import User
from app.models.product import Product
from app.models.order import Order
from app.models.order_detail import OrderDetail
from sqlalchemy import func
import csv
import os
from flask import current_app
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor, white, black, gray
from datetime import datetime
import io

# ============================================================
# ESTILOS PERSONALIZADOS
# ============================================================
def get_styles():
    styles = getSampleStyleSheet()
    # Título principal
    styles.add(ParagraphStyle(
        name='TitleBlue',
        parent=styles['Title'],
        fontName='Helvetica-Bold',
        fontSize=18,
        textColor=HexColor('#122474'),
        alignment=TA_LEFT,
        spaceAfter=4
    ))
    # Subtítulo (fecha)
    styles.add(ParagraphStyle(
        name='DateGray',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        textColor=HexColor('#666666'),
        alignment=TA_LEFT,
        spaceAfter=10
    ))
    # Cabecera de tabla
    styles.add(ParagraphStyle(
        name='TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        textColor=white,
        alignment=TA_CENTER,
        backColor=HexColor('#122474')
    ))
    # Celda de tabla normal
    styles.add(ParagraphStyle(
        name='TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        textColor=HexColor('#333333'),
        alignment=TA_LEFT,
        leading=12
    ))
    # Celda de tabla alineada a la derecha
    styles.add(ParagraphStyle(
        name='TableCellRight',
        parent=styles['TableCell'],
        alignment=TA_RIGHT
    ))
    # Celda de tabla centrada
    styles.add(ParagraphStyle(
        name='TableCellCenter',
        parent=styles['TableCell'],
        alignment=TA_CENTER
    ))
    # Pie de página
    styles.add(ParagraphStyle(
        name='FooterText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        textColor=HexColor('#888888'),
        alignment=TA_CENTER
    ))
    return styles

# ============================================================
# FUNCIONES DE REPORTE
# ============================================================
def get_entrepreneurs_report_data():
    entrepreneurs = User.query.filter_by(role='emprendedor').all()
    data = []
    for user in entrepreneurs:
        products = Product.query.filter_by(user_id=user.id).all()
        total_products = len(products)
        orders = db.session.query(Order).join(OrderDetail).join(Product).filter(
            Product.user_id == user.id, Order.status == 'completado'
        ).distinct().all()
        total_sales = sum(order.total for order in orders)
        top_product = db.session.query(
            Product.name, func.sum(OrderDetail.quantity).label('total')
        ).join(OrderDetail).filter(Product.user_id == user.id).group_by(Product.id).order_by(func.sum(OrderDetail.quantity).desc()).first()
        data.append({
            'id': user.id,
            'email': user.email,
            'full_name': f"{user.first_name} {user.last_name}",
            'created_at': user.created_at,
            'total_products': total_products,
            'total_sales': total_sales,
            'top_product': top_product[0] if top_product else 'Ninguno'
        })
    return data

def get_clients_report_data():
    clients = User.query.filter_by(role='cliente').all()
    data = []
    for user in clients:
        orders = Order.query.filter_by(user_id=user.id, status='completado').all()
        total_purchases = len(orders)
        total_spent = sum(order.total for order in orders)
        data.append({
            'id': user.id,
            'email': user.email,
            'full_name': f"{user.first_name} {user.last_name}",
            'created_at': user.created_at,
            'total_purchases': total_purchases,
            'total_spent': total_spent
        })
    return data

def export_to_csv(data, headers, filename):
    filepath = os.path.join(current_app.root_path, 'static', 'reports', filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for row in data:
            row_copy = {k: v.strftime('%Y-%m-%d %H:%M') if hasattr(v, 'strftime') else v for k, v in row.items()}
            writer.writerow(row_copy)
    return filepath

def export_to_pdf(data, headers, title, filename):
    """
    Genera un PDF con diseño moderno y minimalista (estilo factura profesional).
    """
    filepath = os.path.join(current_app.root_path, 'static', 'reports', filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    styles = get_styles()
    elements = []

    # ---------- ENCABEZADO ----------
    # Logo + Título en una tabla de 2 columnas
    logo_path = os.path.join(current_app.root_path, 'static', 'images', 'logo.png')
    logo_data = []
    
    if os.path.exists(logo_path):
        # Crear una imagen con dimensiones controladas
        img = Image(logo_path, width=100*mm, height=35*mm)
        img.hAlign = 'LEFT'
        logo_cell = [img]
    else:
        logo_cell = [Paragraph("LOCAL MARKET", styles['TitleBlue'])]
    
    # Celda derecha: título y fecha
    right_cell = [
        Paragraph(title, styles['TitleBlue']),
        Paragraph(f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['DateGray'])
    ]
    
    header_table = Table(
        [[logo_cell, right_cell]],
        colWidths=[100*mm, 120*mm],
        style=TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('ALIGN', (1,0), (1,0), 'RIGHT'),
            ('LEFTPADDING', (0,0), (0,0), 0),
            ('RIGHTPADDING', (1,0), (1,0), 0),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ])
    )
    elements.append(header_table)
    
    # Línea separadora después del encabezado
    elements.append(Spacer(1, 2*mm))
    line_table = Table(
        [['']],
        colWidths=[220*mm],
        style=TableStyle([
            ('LINEABOVE', (0,0), (-1,-1), 1, HexColor('#122474')),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ])
    )
    elements.append(line_table)
    elements.append(Spacer(1, 5*mm))

    # ---------- TABLA DE DATOS ----------
    # Mapeo de headers a nombres legibles
    header_map = {
        'id': 'ID',
        'email': 'Email',
        'full_name': 'Nombre',
        'created_at': 'Fecha registro',
        'total_products': '# Prod.',
        'total_sales': 'Ventas (COP)',
        'top_product': 'Prod. más vendido',
        'total_purchases': '# Compras',
        'total_spent': 'Total gastado'
    }

    # Preparar datos
    col_count = len(headers)
    data_rows = []
    
    # Encabezado de la tabla (con estilo)
    header_row = []
    for key in headers:
        header_row.append(Paragraph(header_map.get(key, key), styles['TableHeader']))
    data_rows.append(header_row)

    # Datos
    for row in data:
        row_cells = []
        for key in headers:
            value = row.get(key, '')
            if hasattr(value, 'strftime'):
                value = value.strftime('%d/%m/%Y')
            if key in ['total_sales', 'total_spent']:
                value = f"${float(value):,.0f}".replace(",", ".")
            # Truncar para evitar desborde
            str_val = str(value)
            if len(str_val) > 35:
                str_val = str_val[:32] + "..."
            # Alineación según tipo
            if key in ['id', 'total_products', 'total_purchases']:
                style = styles['TableCellCenter']
            elif key in ['total_sales', 'total_spent']:
                style = styles['TableCellRight']
            else:
                style = styles['TableCell']
            row_cells.append(Paragraph(str_val, style))
        data_rows.append(row_cells)

    # Calcular anchos de columna
    if col_count == 7:
        col_widths = [20*mm, 45*mm, 45*mm, 30*mm, 20*mm, 35*mm, 45*mm]
    else:
        col_widths = [20*mm, 45*mm, 45*mm, 30*mm, 25*mm, 35*mm]

    # Crear tabla con estilo moderno
    table = Table(data_rows, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle([
        # Bordes y fondo de cabecera
        ('BACKGROUND', (0,0), (-1,0), HexColor('#122474')),
        ('TEXTCOLOR', (0,0), (-1,0), white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 10),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        
        # Bordes de la tabla
        ('GRID', (0,0), (-1,-1), 0.5, HexColor('#cccccc')),
        ('LINEABOVE', (0,0), (-1,0), 1.5, HexColor('#122474')),
        ('LINEBELOW', (0,0), (-1,0), 1, HexColor('#122474')),
        
        # Padding
        ('TOPPADDING', (0,0), (-1,-1), 4*mm),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4*mm),
        ('LEFTPADDING', (0,0), (-1,-1), 3*mm),
        ('RIGHTPADDING', (0,0), (-1,-1), 3*mm),
        
        # Filas alternadas
        ('BACKGROUND', (0,1), (-1,-1), HexColor('#f9f9f9')),
        ('BACKGROUND', (0,2), (-1,-2), white),
        
        # Alineación por columna
        ('ALIGN', (0,1), (0,-1), 'CENTER'),      # ID
        ('ALIGN', (4,1), (4,-1), 'CENTER'),      # # Prod.
        ('ALIGN', (5,1), (5,-1), 'RIGHT'),       # Ventas
        ('ALIGN', (6,1), (6,-1), 'LEFT'),        # Producto más vendido
    ]))

    elements.append(table)
    elements.append(Spacer(1, 10*mm))

    # ---------- PIE DE PÁGINA ----------
    footer_text = Paragraph(
        "THANKS FOR USING LOCAL MARKET — Todos los precios en Pesos Colombianos (COP)",
        styles['FooterText']
    )
    elements.append(footer_text)

    # ---------- GENERAR PDF ----------
    doc = SimpleDocTemplate(
        filepath,
        pagesize=landscape(A4),
        leftMargin=15*mm,
        rightMargin=15*mm,
        topMargin=15*mm,
        bottomMargin=15*mm,
    )
    doc.build(elements)
    
    return filepath