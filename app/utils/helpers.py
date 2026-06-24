import random
import string
from datetime import datetime

def generate_invoice_number():
    """
    Genera un número de factura único y corto.
    Formato: FACT-YYYYMMDD-XXXX (ej: FACT-20260624-1218)
    Máximo 20 caracteres: 5 (FACT-) + 8 (fecha) + 1 (-) + 4 (aleatorio) = 19 caracteres
    """
    now = datetime.now()
    # Parte aleatoria de 4 dígitos (más que suficiente para evitar colisiones)
    random_part = ''.join(random.choices(string.digits, k=4))
    return f"FACT-{now.strftime('%Y%m%d')}-{random_part}"
