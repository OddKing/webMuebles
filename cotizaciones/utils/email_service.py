import os
import threading
from django.core.mail import EmailMessage
from django.conf import settings
from email.mime.image import MIMEImage

def _send_email_thread(email):
    """Función para ejecutar el envío del correo en un hilo independiente"""
    try:
        email.send(fail_silently=False)
        print("✅ Correo enviado con éxito en segundo plano.")
    except Exception as e:
        print(f"❌ Error al enviar correo en segundo plano: {e}")

def send_async_email(subject, html_body, to_emails, attachments=None, reply_to=None, attach_logo=True):
    """
    Construye y envía un correo electrónico de manera asíncrona usando hilos de fondo.
    Adjunta automáticamente el logo si se solicita.
    """
    if isinstance(to_emails, str):
        to_emails = [to_emails]
        
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'contacto@mueblesbarguay.cl')
    
    email = EmailMessage(
        subject=subject,
        body=html_body,
        from_email=from_email,
        to=to_emails,
        reply_to=reply_to
    )
    email.content_subtype = 'html'
    
    # Adjuntar archivos genéricos si se proporcionan (lista de tuplas (filename, content, mimetype))
    if attachments:
        for filename, content, mimetype in attachments:
            email.attach(filename, content, mimetype)
        
    # Adjuntar el logo de la empresa para correos con formato de marca
    if attach_logo:
        logo_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'logo.jpg')
        if os.path.exists(logo_path):
            try:
                with open(logo_path, 'rb') as f:
                    logo_data = f.read()
                logo = MIMEImage(logo_data)
                logo.add_header('Content-ID', '<logo>')
                email.attach(logo)
            except Exception as e:
                print(f"Error al adjuntar el logotipo: {e}")
                
    # Iniciar el hilo de fondo
    thread = threading.Thread(target=_send_email_thread, args=(email,))
    thread.daemon = True
    thread.start()
