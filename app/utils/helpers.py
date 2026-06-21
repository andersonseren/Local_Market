import random
import string

def generate_invoice_number():
    """Genera un número de factura único: FACT- + fecha + aleatorio"""
    from datetime import datetime
    now = datetime.now()
    random_part = ''.join(random.choices(string.digits, k=4))
    return f"FACT-{now.strftime('%Y%m%d%H%M%S')}-{random_part}"