import mysql.connector
import sys

# Configuración de conexión
config = {
    'user': 'root',
    'password': 'El.2014Corina',
    'host': 'server.mueblesbarguay.cl',
    'database': 'mueblesbarguay',
    'raise_on_warnings': True
}

# SQL queries a ejecutar
queries = [
    "ALTER TABLE `cotizaciones_cita` ADD COLUMN `admin_notas` longtext NOT NULL DEFAULT '';",
    "ALTER TABLE `cotizaciones_cita` ADD COLUMN `fecha_aprobacion` datetime(6) NULL;",
    "ALTER TABLE `cotizaciones_cotizacion` ADD COLUMN `fecha_aprobacion` datetime(6) NULL;",
    "ALTER TABLE `cotizaciones_cotizacion` ADD COLUMN `admin_notas` longtext NOT NULL DEFAULT '';",
]

try:
    # Conectar a MySQL
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    
    print("Conectado a MySQL. Aplicando migraciones...")
    
    for i, query in enumerate(queries, 1):
        try:
            print(f"\n{i}. Ejecutando: {query[:60]}...")
            cursor.execute(query)
            print(f"   ✓ Exitoso")
        except mysql.connector.Error as err:
            if err.errno == 1060:  # Duplicate column name
                print(f"   ⚠ La columna ya existe, omitiendo...")
            else:
                print(f"   ✗ Error: {err}")
                raise
    
    # Commit cambios
    cnx.commit()
    print("\n✓ Todas las migraciones se aplicaron exitosamente!")
    
    # Cerrar conexión
    cursor.close()
    cnx.close()
    
except mysql.connector.Error as err:
    print(f"\n✗ Error de conexión: {err}")
    sys.exit(1)
except Exception as e:
    print(f"\n✗ Error inesperado: {e}")
    sys.exit(1)
