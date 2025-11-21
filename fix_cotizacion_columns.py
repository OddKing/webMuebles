import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webMuebles.settings')
django.setup()

print("Corrigiendo columnas en cotizaciones_cotizacion...")

queries = [
    # Renombrar alto_espacio a medidas_alto
    "ALTER TABLE `cotizaciones_cotizacion` CHANGE `alto_espacio` `medidas_alto` decimal(6,2) NOT NULL DEFAULT 0.00;",
    # Renombrar ancho_espacio a medidas_ancho
    "ALTER TABLE `cotizaciones_cotizacion` CHANGE `ancho_espacio` `medidas_ancho` decimal(6,2) NOT NULL DEFAULT 0.00;",
    # Agregar medidas_profundidad
    "ALTER TABLE `cotizaciones_cotizacion` ADD COLUMN `medidas_profundidad` decimal(6,2) NOT NULL DEFAULT 0.00;"
]

with connection.cursor() as cursor:
    for i, query in enumerate(queries, 1):
        try:
            print(f"\n{i}. Ejecutando: {query[:60]}...")
            cursor.execute(query)
            print(f"   ✓ Exitoso")
        except Exception as err:
            error_msg = str(err)
            if "Unknown column 'alto_espacio'" in error_msg:
                print("   ⚠ Columna 'alto_espacio' no encontrada, intentando agregar 'medidas_alto' directamente...")
                try:
                    cursor.execute("ALTER TABLE `cotizaciones_cotizacion` ADD COLUMN `medidas_alto` decimal(6,2) NOT NULL DEFAULT 0.00;")
                    print("   ✓ Columna 'medidas_alto' agregada")
                except Exception as e:
                     if "Duplicate column name" in str(e):
                        print("   ⚠ La columna 'medidas_alto' ya existe")
                     else:
                        print(f"   ✗ Error: {e}")

            elif "Unknown column 'ancho_espacio'" in error_msg:
                print("   ⚠ Columna 'ancho_espacio' no encontrada, intentando agregar 'medidas_ancho' directamente...")
                try:
                    cursor.execute("ALTER TABLE `cotizaciones_cotizacion` ADD COLUMN `medidas_ancho` decimal(6,2) NOT NULL DEFAULT 0.00;")
                    print("   ✓ Columna 'medidas_ancho' agregada")
                except Exception as e:
                     if "Duplicate column name" in str(e):
                        print("   ⚠ La columna 'medidas_ancho' ya existe")
                     else:
                        print(f"   ✗ Error: {e}")
            
            elif "Duplicate column name" in error_msg:
                print(f"   ⚠ La columna ya existe, omitiendo...")
            else:
                print(f"   ✗ Error: {err}")

print("\n✓ Corrección de columnas completada!")
