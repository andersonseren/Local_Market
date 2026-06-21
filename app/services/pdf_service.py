import os
from flask import current_app
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.units import cm
from app.extensions import db
from app.models.order import Order

def generate_invoice_pdf(order_id):
    order = Order.query.get(order_id)
    if not order or not order.invoice:
        return None

    user = order.customer
    pdf_dir = os.path.join(current_app.root_path, 'static', 'invoices')
    os.makedirs(pdf_dir, exist_ok=True)

    filename = f"factura_{order.invoice.invoice_number}.pdf"
    filepath = os.path.join(pdf_dir, filename)

    c = canvas.Canvas(filepath, pagesize=A4)
    width, height = A4  # 595 x 842 puntos (aprox)

    # Colores
    azul = HexColor("#122474")
    naranja = HexColor("#f75407")
    gris = HexColor("#333333")
    gris_claro = HexColor("#666666")

    # --- LOGO (esquina superior izquierda) ---
    logo_path = os.path.join(current_app.root_path, 'static', 'images', 'logo.png')
    if os.path.exists(logo_path):
        c.drawImage(logo_path, 50, height - 70, width=120, height=40, preserveAspectRatio=True)
    else:
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(azul)
        c.drawString(50, height - 60, "Local Market")

    # --- TÍTULO Y NÚMERO DE FACTURA (arriba a la derecha) ---
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(azul)
    c.drawRightString(width - 50, height - 50, "FACTURA")
    c.setFont("Helvetica", 10)
    c.setFillColor(gris_claro)
    c.drawRightString(width - 50, height - 70, f"N° {order.invoice.invoice_number}")
    c.drawRightString(width - 50, height - 85, f"Fecha: {order.order_date.strftime('%d/%m/%Y %H:%M')}")

    # --- DATOS DEL CLIENTE (debajo del logo) ---
    y = height - 130
    c.setFillColor(azul)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Cliente:")
    c.setFillColor(gris)
    c.setFont("Helvetica", 10)
    c.drawString(50, y - 15, f"{user.first_name} {user.last_name}")
    c.drawString(50, y - 30, f"Email: {user.email}")

    # --- TABLA DE PRODUCTOS ---
    # Encabezados de la tabla
    table_y = y - 80
    c.setFillColor(azul)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, table_y, "Producto")
    c.drawString(250, table_y, "Cantidad")
    c.drawString(350, table_y, "Precio Unit.")
    c.drawString(470, table_y, "Subtotal")

    # Línea separadora
    c.setStrokeColor(azul)
    c.line(50, table_y - 5, 550, table_y - 5)

    # Contenido de la tabla
    current_y = table_y - 25
    c.setFont("Helvetica", 9)
    c.setFillColor(gris_claro)

    for detail in order.details:
        product_name = detail.product.name[:35]  # Limitar longitud
        quantity = detail.quantity
        unit_price = float(detail.unit_price)
        subtotal = float(detail.subtotal)

        unit_price_str = f"${unit_price:,.0f}".replace(",", ".")
        subtotal_str = f"${subtotal:,.0f}".replace(",", ".")

        c.drawString(50, current_y, product_name)
        c.drawString(250, current_y, str(quantity))
        c.drawString(350, current_y, unit_price_str)
        c.drawString(470, current_y, subtotal_str)

        current_y -= 20
        if current_y < 100:
            c.showPage()
            current_y = height - 50
            c.setFont("Helvetica", 9)

    # --- TOTAL ---
    total = float(order.total)
    total_str = f"${total:,.0f}".replace(",", ".")
    c.setFillColor(naranja)
    c.setFont("Helvetica-Bold", 12)
    c.drawRightString(width - 50, current_y - 15, f"Total: {total_str} COP")

    # --- PIE DE PÁGINA ---
    c.setFillColor(gris_claro)
    c.setFont("Helvetica-Oblique", 8)
    c.drawCentredString(width / 2, 30, "Gracias por su compra. Esta factura es válida en Colombia.")
    c.drawCentredString(width / 2, 20, "Local Market - Todos los derechos reservados")

    c.save()
    order.invoice.pdf_path = filepath
    db.session.commit()
    return filepath