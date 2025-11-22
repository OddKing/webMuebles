from decimal import Decimal

def calcular_precio_estimado(cotizacion):
    """
    Calcula un precio estimado basado en dimensiones y material.
    Retorna un diccionario con el desglose del cálculo.
    """
    try:
        # Validar datos
        if not all([cotizacion.medidas_alto, cotizacion.medidas_ancho, cotizacion.medidas_profundidad]):
            return None
            
        # Convertir a float para cálculos matemáticos (evitar problemas con Decimal)
        alto_m = float(cotizacion.medidas_alto) / 100
        ancho_m = float(cotizacion.medidas_ancho) / 100
        prof_m = float(cotizacion.medidas_profundidad) / 100
        
        # 1. Cálculo de Superficie Estimada (m2)
        area_superficial = 2 * (alto_m * ancho_m + alto_m * prof_m + ancho_m * prof_m)
        area_con_desperdicio = area_superficial * 1.2
        
        # 2. Precios Base por Material (CLP por m2)
        PRECIOS_MATERIAL = {
            'pino': 18000,
            'melamina': 22000,
            'mdf': 25000,
            'roble': 55000,
            'otro': 30000
        }
        
        material_key = cotizacion.material_preferido
        precio_m2 = PRECIOS_MATERIAL.get(material_key, 30000)
        
        costo_material = area_con_desperdicio * precio_m2
        
        # 3. Costos Adicionales
        FACTOR_COMPLEJIDAD = 2.5 
        MANO_OBRA_BASE = 45000
        
        # Cálculo Final
        precio_estimado = (costo_material * FACTOR_COMPLEJIDAD) + MANO_OBRA_BASE
        precio_final = round(precio_estimado / 1000) * 1000
        
        return {
            'precio_final': precio_final,
            'area_m2': round(area_con_desperdicio, 2),
            'precio_base_m2': precio_m2,
            'costo_material': round(costo_material),
            'mano_obra': MANO_OBRA_BASE,
            'factor': FACTOR_COMPLEJIDAD,
            'material_nombre': material_key.title()
        }
        
    except Exception as e:
        print(f"Error calculando precio estimado: {e}")
        return None
