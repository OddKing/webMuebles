import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webMuebles.settings')
django.setup()

def check_columns():
    with connection.cursor() as cursor:
        cursor.execute("DESCRIBE cotizaciones_cotizacion")
        columns = [row[0] for row in cursor.fetchall()]
        print("Columns in cotizaciones_cotizacion:")
        for col in columns:
            print(f"- {col}")

        print("\n" + "="*30 + "\n")

        cursor.execute("DESCRIBE cotizaciones_consentimientolegal")
        columns = [row[0] for row in cursor.fetchall()]
        print("Columns in cotizaciones_consentimientolegal:")
        for col in columns:
            print(f"- {col}")

if __name__ == '__main__':
    check_columns()
