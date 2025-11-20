from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import Cita
from datetime import datetime, timedelta, time
import json

# Create your views here.

def get_horarios_disponibles(request):
    """Endpoint AJAX para obtener horarios disponibles de una fecha específica"""
    if request.method == 'GET':
        fecha_str = request.GET.get('fecha')
        
        if not fecha_str:
            return JsonResponse({'error': 'Fecha requerida'}, status=400)
        
        try:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            
            # Obtener todas las citas de ese día
            citas_del_dia = Cita.objects.filter(fecha=fecha).values_list('hora', flat=True)
            
            # Convertir a strings de formato HH:MM
            horarios_ocupados = [hora.strftime('%H:%M') for hora in citas_del_dia]
            
            # Generar todos los horarios posibles
            horarios_todos = []
            hora_actual = time(10, 0)
            hora_final = time(18, 0)
            
            while hora_actual <= hora_final:
                horarios_todos.append(hora_actual.strftime('%H:%M'))
                dt = datetime.combine(datetime.today(), hora_actual)
                dt += timedelta(minutes=30)
                hora_actual = dt.time()
            
            # Filtrar horarios disponibles
            horarios_disponibles = [h for h in horarios_todos if h not in horarios_ocupados]
            
            return JsonResponse({
                'horarios_disponibles': horarios_disponibles,
                'horarios_ocupados': horarios_ocupados
            })
            
        except ValueError:
            return JsonResponse({'error': 'Formato de fecha inválido'}, status=400)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def agendar_reunion(request):
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre_completo = request.POST.get('nombre_completo')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')
        email = request.POST.get('email')
        tipo_reunion = request.POST.get('tipo_reunion')
        fecha_str = request.POST.get('fecha')
        hora_str = request.POST.get('hora')
        
        # Validar que todos los campos estén presentes
        if all([nombre_completo, telefono, direccion, email, tipo_reunion, fecha_str, hora_str]):
            try:
                # Convertir fecha y hora
                fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
                hora = datetime.strptime(hora_str, '%H:%M').time()
                
                # Validaciones de negocio
                hoy = datetime.now().date()
                
                # Validar que la fecha sea mínimo mañana
                if fecha <= hoy:
                    messages.error(request, 'La fecha debe ser al menos un día después de hoy.')
                    return redirect('agendar_reunion')
                
                # Validar que no sea fin de semana (0=Monday, 6=Sunday)
                if fecha.weekday() >= 5:
                    messages.error(request, 'Solo se pueden agendar reuniones de lunes a viernes.')
                    return redirect('agendar_reunion')
                
                # Validar horario (10:00 - 18:00)
                hora_inicio = time(10, 0)
                hora_fin = time(18, 0)
                if not (hora_inicio <= hora <= hora_fin):
                    messages.error(request, 'El horario debe estar entre 10:00 AM y 6:00 PM.')
                    return redirect('agendar_reunion')
                
                # NUEVA VALIDACIÓN: Verificar que el horario no esté ocupado
                if Cita.objects.filter(fecha=fecha, hora=hora).exists():
                    messages.error(request, f'Lo sentimos, el horario {hora.strftime("%H:%M")} del día {fecha.strftime("%d/%m/%Y")} ya está reservado. Por favor selecciona otro horario.')
                    return redirect('agendar_reunion')
                
                # Crear la cita
                cita = Cita.objects.create(
                    nombre_completo=nombre_completo,
                    telefono=telefono,
                    direccion=direccion,
                    email=email,
                    tipo_reunion=tipo_reunion,
                    fecha=fecha,
                    hora=hora
                )
                
                # ENVIAR EMAIL DE CONFIRMACIÓN
                try:
                    from django.core.mail import EmailMultiAlternatives
                    from django.template.loader import render_to_string
                    from django.conf import settings
                    from email.mime.image import MIMEImage
                    import os
                    
                    # Formatear fecha en español
                    meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
                            'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
                    dias_semana = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
                    
                    dia_semana = dias_semana[fecha.weekday()]
                    fecha_formateada = f"{dia_semana.capitalize()}, {fecha.day} de {meses[fecha.month-1]} de {fecha.year}"
                    
                    tipo_reunion_display = 'Online' if tipo_reunion == 'online' else 'Presencial'
                    
                    # Contexto para el template
                    context = {
                        'nombre_completo': nombre_completo,
                        'fecha_formateada': fecha_formateada,
                        'hora': hora.strftime('%H:%M'),
                        'tipo_reunion': tipo_reunion,
                        'tipo_reunion_display': tipo_reunion_display,
                    }
                    
                    # Renderizar templates
                    html_content = render_to_string('emails/confirmacion_cita.html', context)
                    text_content = render_to_string('emails/confirmacion_cita.txt', context)
                    
                    # Crear email
                    subject = f'Confirmación de Reunión - {fecha_formateada} a las {hora.strftime("%H:%M")}'
                    from_email = settings.DEFAULT_FROM_EMAIL
                    to_email = [email]
                    
                    msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
                    msg.attach_alternative(html_content, "text/html")
                    
                    # Adjuntar logo como imagen embebida
                    logo_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'logo.jpg')
                    if os.path.exists(logo_path):
                        with open(logo_path, 'rb') as f:
                            logo_img = MIMEImage(f.read())
                            logo_img.add_header('Content-ID', '<logo>')
                            logo_img.add_header('Content-Disposition', 'inline', filename='logo.jpg')
                            msg.attach(logo_img)
                    
                    # Enviar email
                    msg.send(fail_silently=False)
                    
                    messages.success(request, f'¡Reunión agendada exitosamente! Hemos enviado un email de confirmación a {email}')
                    
                except Exception as e:
                    # Si falla el email, la cita ya fue creada, pero notificamos el error
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.error(f'Error al enviar email de confirmación: {str(e)}')
                    messages.warning(request, f'Reunión agendada para el {fecha.strftime("%d/%m/%Y")} a las {hora.strftime("%H:%M")}, pero hubo un problema al enviar el email de confirmación.')
                
                return redirect('agendar_reunion')
                
            except ValueError as e:
                messages.error(request, 'Error en el formato de fecha u hora.')
                return redirect('agendar_reunion')
        else:
            messages.error(request, 'Por favor complete todos los campos.')
            return redirect('agendar_reunion')
    
    # GET request - mostrar formulario
    # Generar horarios disponibles (de 10:00 a 18:00 en intervalos de 30 minutos)
    horarios = []
    hora_actual = time(10, 0)
    hora_final = time(18, 0)
    
    while hora_actual <= hora_final:
        horarios.append(hora_actual.strftime('%H:%M'))
        # Sumar 30 minutos
        dt = datetime.combine(datetime.today(), hora_actual)
        dt += timedelta(minutes=30)
        hora_actual = dt.time()
    
    # Calcular fecha mínima (mañana)
    fecha_minima = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    
    context = {
        'horarios': horarios,
        'fecha_minima': fecha_minima,
    }
    
    return render(request, 'agendar.html', context)
