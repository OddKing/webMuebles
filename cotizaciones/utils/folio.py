"""
Utilidades para generar número de folio único para cotizaciones
"""
from cotizaciones.models import Cotizacion


def generar_folio():
    """
    Genera un número de folio único para una cotización
    Formato: COT-001, COT-002, etc.
    """
    # Obtener la última cotización con folio
    ultima_cotizacion = Cotizacion.objects.filter(
        folio__startswith='COT-'
    ).order_by('-folio').first()
    
    if ultima_cotizacion and ultima_cotizacion.folio:
        # Extraer el número del último folio
        try:
            ultimo_numero = int(ultima_cotizacion.folio.split('-')[1])
            nuevo_numero = ultimo_numero + 1
        except (IndexError, ValueError):
            nuevo_numero = 1
    else:
        nuevo_numero = 1
    
    # Formatear con ceros a la izquierda (3 dígitos)
    folio = f"COT-{nuevo_numero:03d}"
    
    # Verificar que no existe (por seguridad)
    while Cotizacion.objects.filter(folio=folio).exists():
        nuevo_numero += 1
        folio = f"COT-{nuevo_numero:03d}"
    
    return folio


def calcular_precio_con_iva(precio_base):
    """
    Calcula el precio con IVA (19% en Chile)
    
    Args:
        precio_base (Decimal): Precio base sin IVA
    
    Returns:
        dict: Diccionario con subtotal, iva y total
    """
    if not precio_base:
        return {
            'subtotal': 0,
            'iva': 0,
            'total': 0
        }
    
    subtotal = float(precio_base)
    iva = subtotal * 0.19
    total = subtotal + iva
    
    return {
        'subtotal': subtotal,
        'iva': iva,
        'total': total
    }
