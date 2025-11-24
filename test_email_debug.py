import os
import django
import sys

# Configurar entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webMuebles.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

try:
    print(f"Intentando enviar correo con configuración:")
    print(f"HOST: {settings.EMAIL_HOST}")
    print(f"PORT: {settings.EMAIL_PORT}")
    print(f"USER: {settings.EMAIL_HOST_USER}")
    print(f"USE_SSL: {settings.EMAIL_USE_SSL}")
    
    send_mail(
        subject='Prueba de Diagnóstico - Muebles Barguay',
        message='Si recibes esto, el envío de correos funciona correctamente.',
        from_email='contacto@mueblesbarguay.cl',
        recipient_list=['contacto@mueblesbarguay.cl'],
        fail_silently=False,
    )
    print("\n✅ ¡Correo enviado exitosamente!")
except Exception as e:
    print(f"\n❌ Error al enviar correo: {e}")
