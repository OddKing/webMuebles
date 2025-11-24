import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webMuebles.settings')
django.setup()

from cotizaciones.models import ConsentimientoLegal, Cotizacion, Cita

def check_broken_references():
    print("Checking ConsentimientoLegal references...")
    for c in ConsentimientoLegal.objects.all():
        try:
            if c.cita_id:
                print(f"Checking Cita {c.cita_id} for Consentimiento {c.id}...")
                _ = c.cita
            if c.cotizacion_id:
                print(f"Checking Cotizacion {c.cotizacion_id} for Consentimiento {c.id}...")
                _ = c.cotizacion
        except Cita.DoesNotExist:
            print(f"ERROR: Consentimiento {c.id} references non-existent Cita {c.cita_id}")
        except Cotizacion.DoesNotExist:
            print(f"ERROR: Consentimiento {c.id} references non-existent Cotizacion {c.cotizacion_id}")
        except Exception as e:
            print(f"ERROR: Consentimiento {c.id} raised {e}")

    print("\nDone checking references.")
    
    print("\nChecking Cotizacion -> Producto references...")
    from productos.models import Producto
    for c in Cotizacion.objects.all():
        if c.producto_id:
            try:
                _ = c.producto
            except Producto.DoesNotExist:
                print(f"ERROR: Cotizacion {c.id} references non-existent Producto {c.producto_id}")
            except Exception as e:
                print(f"ERROR: Cotizacion {c.id} raised {e} accessing producto")
    print("Done checking product references.")

if __name__ == '__main__':
    check_broken_references()
