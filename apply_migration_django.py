import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webMuebles.settings')
django.setup()

from django.db import connection

# SQL queries a ejecutar
queries = [
    "ALTER TABLE `cotizaciones_cita` ADD COLUMN `admin_notas` longtext NULL;",
    "ALTER TABLE `cotizaciones_cita` ADD COLUMN `fecha_aprobacion` datetime(6) NULL;",
    "ALTER TABLE `cotizaciones_cotizacion` ADD COLUMN `fecha_aprobacion` datetime(6) NULL;",
    "ALTER TABLE `cotizaciones_cotizacion` ADD COLUMN `admin_notas` longtext NULL;",
]

print("Aplicando migraciones directamente a la base de datos...")

with connection.cursor() as cursor:
    for i, query in enumerate(queries, 1):
        try:
            print(f"\n{i}. Ejecutando: {query[:70]}...")
            cursor.execute(query)
            print(f"   ✓ Exitoso")
        except Exception as err:
            error_msg = str(err)
            if 'Duplicate column name' in error_msg:
                print(f"   ⚠ La columna ya existe, omitiendo...")
            else:
                print(f"   ✗ Error: {err}")
                raise

print("\n✓ Todas las migraciones se aplicaron exitosamente!")
