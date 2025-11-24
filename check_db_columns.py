import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webMuebles.settings')
django.setup()

def check_columns():
    with connection.cursor() as cursor:
        cursor.execute("DESCRIBE cotizaciones_cotizacion;")
        columns = [col[0] for col in cursor.fetchall()]
        print("Columnas en cotizaciones_cotizacion:")
        for col in columns:
            print(f"- {col}")
            
        print("\nVerificando columnas críticas:")
        critical_cols = ['medidas_alto', 'medidas_ancho', 'medidas_profundidad', 'fecha_aprobacion', 'admin_notas']
        for col in critical_cols:
            if col in columns:
                print(f"✓ {col} existe")
            else:
                print(f"✗ {col} NO existe")

if __name__ == '__main__':
    check_columns()
