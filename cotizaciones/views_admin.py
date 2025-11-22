from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils import timezone
from django.http import JsonResponse
from .models import Cotizacion, Cita
from .utils.pdf_generator import generate_quote_pdf
import os
from django.conf import settings
from email.mime.image import MIMEImage


def admin_login(request):
    """Vista de login para el panel de administración"""
    if request.user.is_authenticated:
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenido, {user.username}!')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Credenciales inválidas. Por favor, intente nuevamente.')
    
    return render(request, 'admin_panel/login.html')


def admin_logout(request):
    """Vista de logout para el panel de administración"""
    logout(request)
    messages.success(request, 'Sesión cerrada exitosamente.')
    return redirect('admin_login')


@login_required(login_url='admin_login')
def admin_dashboard(request):
    """Dashboard principal del panel de administración"""
    from productos.models import Producto
    
    # Contar elementos pendientes
    cotizaciones_pendientes = Cotizacion.objects.filter(estado='pendiente_aprobacion').count()
    citas_pendientes = Cita.objects.filter(estado='pendiente_aprobacion').count()
    productos_total = Producto.objects.count()
    productos_activos = Producto.objects.filter(activo=True).count()
    
    # Obtener registros recientes
    cotizaciones_recientes = Cotizacion.objects.filter(estado='pendiente_aprobacion').order_by('-fecha_solicitud')[:5]
    citas_recientes = Cita.objects.filter(estado='pendiente_aprobacion').order_by('-fecha_creacion')[:5]
    
    context = {
        'cotizaciones_pendientes_count': cotizaciones_pendientes,
        'citas_pendientes_count': citas_pendientes,
        'productos_total': productos_total,
        'productos_activos': productos_activos,
        'admin_cotizaciones': cotizaciones_recientes,
        'citas_recientes': citas_recientes,
    }
    
    return render(request, 'admin_panel/dashboard.html', context)


@login_required(login_url='admin_login')
def admin_cotizaciones_pendientes(request):
    """Vista de cotizaciones pendientes de aprobación"""
    cotizaciones = Cotizacion.objects.filter(estado='pendiente_aprobacion').order_by('-fecha_solicitud')
    
    context = {
        'admin_cotizaciones': cotizaciones,
    }
    
    return render(request, 'admin_panel/cotizaciones_pendientes.html', context)


@login_required(login_url='admin_login')
def admin_citas_pendientes(request):
    """Vista de citas pendientes de aprobación"""
    citas = Cita.objects.filter(estado='pendiente_aprobacion').order_by('-fecha_creacion')
    
    context = {
        'citas': citas,
    }
    
    return render(request, 'admin_panel/citas_pendientes.html', context)


@login_required(login_url='admin_login')
def aprobar_cotizacion(request, cotizacion_id):
    """Aprobar una cotización y enviar email al cliente"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    cotizacion = get_object_or_404(Cotizacion, id=cotizacion_id)
    
    # Actualizar estado
    cotizacion.estado = 'aprobada'
    cotizacion.fecha_aprobacion = timezone.now()
    cotizacion.save()
    
    # Generar PDF
    try:
        producto_nombre = cotizacion.producto.nombre if cotizacion.producto else "Diseño Personalizado"
        pdf_buffer = generate_quote_pdf(cotizacion)
        
        # Preparar email
        html_content = render_to_string('emails/confirmacion_cotizacion.html', {
            'nombre_cliente': cotizacion.nombre_completo,
            'folio': cotizacion.folio,
            'producto_nombre': producto_nombre,
            'ancho': cotizacion.medidas_ancho,
            'alto': cotizacion.medidas_alto,
            'profundidad': cotizacion.medidas_profundidad,
            'material': cotizacion.get_material_preferido_display(),
        })
        
        email = EmailMessage(
            subject=f'Cotización Aprobada - Folio {cotizacion.folio}',
            body=html_content,
            from_email='contacto@mueblesbarguay.cl',
            to=[cotizacion.email],
        )
        email.content_subtype = 'html'
        
        # Adjuntar PDF desde buffer
        email.attach(f'Cotizacion_{cotizacion.folio}.pdf', pdf_buffer.getvalue(), 'application/pdf')
        
        # Adjuntar Logo
        logo_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'logo.jpg')
        if os.path.exists(logo_path):
            with open(logo_path, 'rb') as f:
                logo_data = f.read()
            logo = MIMEImage(logo_data)
            logo.add_header('Content-ID', '<logo>')
            email.attach(logo)
        
        # Enviar email
        email.send(fail_silently=False)
        
        messages.success(request, f'Cotización {cotizacion.folio} aprobada y enviada al cliente.')
        
    except Exception as e:
        messages.warning(request, f'Cotización aprobada pero hubo un error al enviar el email: {str(e)}')
    
    return redirect('admin_cotizaciones')


@login_required(login_url='admin_login')
def rechazar_cotizacion(request, cotizacion_id):
    """Rechazar una cotización"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    cotizacion = get_object_or_404(Cotizacion, id=cotizacion_id)
    admin_notas = request.POST.get('admin_notas', '')
    
    # Actualizar estado
    cotizacion.estado = 'rechazada'
    cotizacion.admin_notas = admin_notas
    cotizacion.fecha_aprobacion = timezone.now()
    cotizacion.save()
    
    # Opcional: Enviar email de rechazo al cliente
    enviar_email_rechazo = request.POST.get('enviar_email', 'no') == 'si'
    
    if enviar_email_rechazo and admin_notas:
        try:
            html_content = render_to_string('emails/cotizacion_rechazada.html', {
                'nombre_cliente': cotizacion.nombre_completo,
                'folio': cotizacion.folio,
                'motivo_rechazo': admin_notas,
            })
            
            email = EmailMessage(
                subject=f'Actualización sobre su Cotización - Folio {cotizacion.folio}',
                body=html_content,
                from_email='contacto@mueblesbarguay.cl',
                to=[cotizacion.email],
            )
            email.content_subtype = 'html'
            
            # Adjuntar Logo
            logo_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'logo.jpg')
            if os.path.exists(logo_path):
                with open(logo_path, 'rb') as f:
                    logo_data = f.read()
                logo = MIMEImage(logo_data)
                logo.add_header('Content-ID', '<logo>')
                email.attach(logo)
            
            email.send(fail_silently=False)
            
            messages.success(request, f'Cotización {cotizacion.folio} rechazada y notificación enviada al cliente.')
        except Exception as e:
            messages.warning(request, f'Cotización rechazada pero hubo un error al enviar el email: {str(e)}')
    return redirect('admin_cotizaciones')


@login_required(login_url='admin_login')
def preview_quote_pdf(request, cotizacion_id):
    """Vista previa del PDF de cotización para el admin"""
    from django.http import HttpResponse
    
    cotizacion = get_object_or_404(Cotizacion, id=cotizacion_id)
    
    try:
        pdf_buffer = generate_quote_pdf(cotizacion)
        response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="Cotizacion_{cotizacion.folio}.pdf"'
        return response
    except Exception as e:
        messages.error(request, f'Error al generar PDF: {str(e)}')
        return redirect('admin_cotizaciones')


@login_required(login_url='admin_login')
def aprobar_cita(request, cita_id):
    """Aprobar una cita y enviar email de confirmación al cliente"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    cita = get_object_or_404(Cita, id=cita_id)
    
    # Actualizar estado
    cita.estado = 'aprobada'
    cita.fecha_aprobacion = timezone.now()
    
    # Capturar link de reunión manual si existe
    meeting_link = request.POST.get('meeting_link')
    if meeting_link and cita.tipo_reunion == 'online':
        cita.meeting_link = meeting_link
        
    cita.save()
    
    # Enviar email de confirmación
    try:
        html_content = render_to_string('emails/confirmacion_cita.html', {
            'nombre_cliente': cita.nombre_completo,
            'tipo_reunion': cita.get_tipo_reunion_display(),
            'fecha': cita.fecha.strftime('%d/%m/%Y'),
            'hora': cita.hora.strftime('%H:%M'),
            'direccion': cita.direccion if cita.tipo_reunion == 'presencial' else 'Online',
            'meeting_link': cita.meeting_link,  # Agregamos el link al contexto
        })
        
        email = EmailMessage(
            subject='Reunión Confirmada - Muebles Barguay',
            body=html_content,
            from_email='contacto@mueblesbarguay.cl',
            to=[cita.email],
        )
        email.content_subtype = 'html'
        
        # Adjuntar Logo
        logo_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'logo.jpg')
        if os.path.exists(logo_path):
            with open(logo_path, 'rb') as f:
                logo_data = f.read()
            logo = MIMEImage(logo_data)
            logo.add_header('Content-ID', '<logo>')
            email.attach(logo)
            
        email.send(fail_silently=False)
        
        messages.success(request, f'Cita de {cita.nombre_completo} aprobada y confirmación enviada.')
        
    except Exception as e:
        messages.warning(request, f'Cita aprobada pero hubo un error al enviar el email: {str(e)}')
    
    return redirect('admin_citas')


@login_required(login_url='admin_login')
def rechazar_cita(request, cita_id):
    """Rechazar una cita"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    cita = get_object_or_404(Cita, id=cita_id)
    admin_notas = request.POST.get('admin_notas', '')
    
    # Actualizar estado
    cita.estado = 'rechazada'
    cita.admin_notas = admin_notas
    cita.fecha_aprobacion = timezone.now()
    cita.save()
    
    # Opcional: Enviar email de rechazo al cliente
    enviar_email_rechazo = request.POST.get('enviar_email', 'no') == 'si'
    
    if enviar_email_rechazo and admin_notas:
        try:
            html_content = render_to_string('emails/cita_rechazada.html', {
                'nombre_cliente': cita.nombre_completo,
                'fecha_solicitada': cita.fecha.strftime('%d/%m/%Y'),
                'hora_solicitada': cita.hora.strftime('%H:%M'),
                'motivo_rechazo': admin_notas,
            })
            
            email = EmailMessage(
                subject='Actualización sobre su Solicitud de Reunión - Muebles Barguay',
                body=html_content,
                from_email='contacto@mueblesbarguay.cl',
                to=[cita.email],
            )
            email.content_subtype = 'html'
            
            # Adjuntar Logo
            logo_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'logo.jpg')
            if os.path.exists(logo_path):
                with open(logo_path, 'rb') as f:
                    logo_data = f.read()
                logo = MIMEImage(logo_data)
                logo.add_header('Content-ID', '<logo>')
                email.attach(logo)
                
            email.send(fail_silently=False)
            
            messages.success(request, f'Cita de {cita.nombre_completo} rechazada y notificación enviada.')
        except Exception as e:
            messages.warning(request, f'Cita rechazada pero hubo un error al enviar el email: {str(e)}')
    else:
        messages.success(request, f'Cita de {cita.nombre_completo} rechazada.')
    
    return redirect('admin_citas')
