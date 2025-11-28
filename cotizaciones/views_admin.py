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
    from .utils.pricing import calcular_precio_estimado
    
    cotizaciones = Cotizacion.objects.filter(estado='pendiente_aprobacion').order_by('-fecha_solicitud')
    
    # Calcular precio sugerido para cada cotización
    for cot in cotizaciones:
        try:
            cot.precio_sugerido = calcular_precio_estimado(cot)
        except Exception as e:
            print(f"Error en cálculo de precio para cotización {cot.id}: {e}")
            cot.precio_sugerido = 0
    
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
    
    # Capturar precio cotizado si existe
    precio_cotizado = request.POST.get('precio_cotizado')
    if precio_cotizado:
        cotizacion.precio_cotizado = precio_cotizado
        
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
            
        # Generar y adjuntar archivo .ics (Calendario)
        try:
            from .utils.calendar import generate_ics_content
            ics_content = generate_ics_content(cita)
            email.attach(f'cita_muebles_barguay_{cita.id}.ics', ics_content, 'text/calendar')
        except Exception as e:
            print(f"Error generando calendario: {e}")
            
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


# ==============================================================================
# NUEVAS FUNCIONALIDADES - ADMIN PANEL ENHANCEMENTS
# ==============================================================================

@login_required(login_url='admin_login')
def admin_scraper_precios(request):
    """Vista para buscar precios de materiales en tiendas externas"""
    from .utils.scraper import buscar_precios, STORES_CONFIG
    
    query = request.GET.get('q', '')
    store = request.GET.get('store', 'sodimac')
    resultados = []
    
    if query:
        try:
            resultados = buscar_precios(query, store_key=store)
        except Exception as e:
            messages.error(request, f'Error al buscar precios: {str(e)}')
    
    context = {
        'query': query,
        'store': store,
        'stores': STORES_CONFIG,
        'resultados': resultados,
    }
    
    return render(request, 'admin_panel/scraper_view.html', context)


@login_required(login_url='admin_login')
def admin_cotizaciones_historial(request):
    """Vista de historial completo de cotizaciones con filtros"""
    from django.db.models import Q
    
    # Obtener parámetros de búsqueda y filtrado
    estado_filter = request.GET.get('estado', '')
    search_query = request.GET.get('q', '')
    
    # Base queryset
    cotizaciones = Cotizacion.objects.all().select_related('producto', 'cliente')
    
    # Aplicar filtro de estado
    if estado_filter:
        cotizaciones = cotizaciones.filter(estado=estado_filter)
    
    # Aplicar búsqueda
    if search_query:
        cotizaciones = cotizaciones.filter(
            Q(folio__icontains=search_query) |
            Q(nombre_completo__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(cliente__nombre_completo__icontains=search_query)
        )
    
    # Ordenar por fecha
    cotizaciones = cotizaciones.order_by('-fecha_solicitud')
    
    # Calcular estadísticas
    total_cotizaciones = Cotizacion.objects.count()
    total_aprobadas = Cotizacion.objects.filter(estado='aprobada').count()
    total_pendientes = Cotizacion.objects.filter(estado='pendiente_aprobacion').count()
    
    context = {
        'cotizaciones': cotizaciones,
        'estado_filter': estado_filter,
        'search_query': search_query,
        'total_cotizaciones': total_cotizaciones,
        'total_aprobadas': total_aprobadas,
        'total_pendientes': total_pendientes,
        'estados': Cotizacion.ESTADO_CHOICES,
    }
    
    return render(request, 'admin_panel/cotizaciones_historial.html', context)


@login_required(login_url='admin_login')
def admin_citas_historial(request):
    """Vista de historial completo de citas con filtros"""
    from django.db.models import Q
    
    # Obtener parámetros de búsqueda y filtrado
    estado_filter = request.GET.get('estado', '')
    search_query = request.GET.get('q', '')
    
    # Base queryset
    citas = Cita.objects.all()
    
    # Aplicar filtro de estado
    if estado_filter:
        citas = citas.filter(estado=estado_filter)
    
    # Aplicar búsqueda
    if search_query:
        citas = citas.filter(
            Q(nombre_completo__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(telefono__icontains=search_query)
        )
    
    # Ordenar por fecha
    citas = citas.order_by('-fecha', '-hora')
    
    # Calcular estadísticas
    total_citas = Cita.objects.count()
    total_aprobadas = Cita.objects.filter(estado='aprobada').count()
    total_pendientes = Cita.objects.filter(estado='pendiente_aprobacion').count()
    
    context = {
        'citas': citas,
        'estado_filter': estado_filter,
        'search_query': search_query,
        'total_citas': total_citas,
        'total_aprobadas': total_aprobadas,
        'total_pendientes': total_pendientes,
        'estados': Cita.ESTADO_CHOICES,
    }
    
    return render(request, 'admin_panel/citas_historial.html', context)


@login_required(login_url='admin_login')
def admin_cotizacion_detalle(request, cotizacion_id):
    """Vista detallada de una cotización específica"""
    from .utils.pricing import calcular_precio_estimado
    
    cotizacion = get_object_or_404(Cotizacion, id=cotizacion_id)
    
    # Calcular precio sugerido
    precio_sugerido = None
    try:
        precio_data = calcular_precio_estimado(cotizacion)
        if precio_data:
            precio_sugerido = precio_data
    except Exception as e:
        print(f"Error calculando precio: {e}")
    
    context = {
        'cotizacion': cotizacion,
        'precio_sugerido': precio_sugerido,
    }
    
    return render(request, 'admin_panel/cotizacion_detalle.html', context)


@login_required(login_url='admin_login')
def admin_crear_cotizacion(request):
    """Vista para crear una cotización desde el admin panel"""
    from .forms import CotizacionForm
    from .utils.folio import generar_folio
    from .utils.pricing import calcular_precio_estimado
    from productos.models import Producto
    
    if request.method == 'POST':
        # Crear formulario sin campos de consentimiento
        form_data = request.POST.copy()
        
        cotizacion = Cotizacion()
        
        # Cliente (si se seleccionó)
        cliente_id = form_data.get('cliente')
        if cliente_id:
            from clientes.models import Cliente
            try:
                cliente = Cliente.objects.get(id=cliente_id)
                cotizacion.cliente = cliente
                # Actualizar última cotización del cliente
                cliente.ultima_cotizacion = timezone.now()
                cliente.save()
            except Cliente.DoesNotExist:
                pass
        
        # Datos del formulario
        cotizacion.nombre_completo = form_data.get('nombre_completo')
        cotizacion.rut = form_data.get('rut', '')
        cotizacion.direccion = form_data.get('direccion', '')
        cotizacion.email = form_data.get('email')
        cotizacion.telefono = form_data.get('telefono', '')
        cotizacion.medidas_alto = form_data.get('medidas_alto')
        cotizacion.medidas_ancho = form_data.get('medidas_ancho')
        cotizacion.medidas_profundidad = form_data.get('medidas_profundidad')
        cotizacion.material_preferido = form_data.get('material_preferido')
        cotizacion.descripcion_proyecto = form_data.get('descripcion_proyecto', '')
        
        # Producto (si se seleccionó)
        producto_id = form_data.get('producto')
        if producto_id:
            try:
                producto = Producto.objects.get(id=producto_id)
                cotizacion.producto = producto
            except Producto.DoesNotExist:
                pass
        
        # Generar folio
        cotizacion.folio = generar_folio()
        
        # Estado y precio
        cotizacion.estado = form_data.get('estado', 'en_revision')
        precio_cotizado = form_data.get('precio_cotizado')
        if precio_cotizado:
            cotizacion.precio_cotizado = precio_cotizado
        else:
            # Calcular precio automáticamente
            try:
                precio_data = calcular_precio_estimado(cotizacion)
                if precio_data:
                    cotizacion.precio_cotizado = precio_data['precio_final']
            except:
                pass
        
        cotizacion.admin_notas = form_data.get('admin_notas', '')
        
        # Guardar
        try:
            cotizacion.save()
            messages.success(request, f'Cotización {cotizacion.folio} creada exitosamente.')
            return redirect('admin_cotizacion_detalle', cotizacion_id=cotizacion.id)
        except Exception as e:
            messages.error(request, f'Error al crear cotización: {str(e)}')
    
    # GET request - mostrar formulario
    productos = Producto.objects.filter(activo=True)
    
    # Si viene un cliente en query params, pre-cargar datos
    cliente_id = request.GET.get('cliente')
    cliente_data = None
    if cliente_id:
        from clientes.models import Cliente
        try:
            cliente = Cliente.objects.get(id=cliente_id)
            cliente_data = {
                'id': cliente.id,
                'nombre_completo': cliente.nombre_completo,
                'rut': cliente.rut,
                'email': cliente.email,
                'telefono': cliente.telefono,
                'direccion': cliente.direccion,
                'descuento_habitual': float(cliente.descuento_habitual),
            }
        except Cliente.DoesNotExist:
            pass
    
    context = {
        'productos': productos,
        'materiales': Cotizacion.MATERIAL_CHOICES,
        'estados': Cotizacion.ESTADO_CHOICES,
        'cliente_data': cliente_data,
    }
    
    return render(request, 'admin_panel/cotizacion_crear.html', context)


@login_required(login_url='admin_login')
def admin_editar_cotizacion(request, cotizacion_id):
    """Vista para editar una cotización existente"""
    from .utils.pricing import calcular_precio_estimado
    from productos.models import Producto
    
    cotizacion = get_object_or_404(Cotizacion, id=cotizacion_id)
    
    if request.method == 'POST':
        form_data = request.POST.copy()
        
        # Actualizar datos
        cotizacion.nombre_completo = form_data.get('nombre_completo')
        cotizacion.rut = form_data.get('rut', '')
        cotizacion.direccion = form_data.get('direccion', '')
        cotizacion.email = form_data.get('email')
        cotizacion.telefono = form_data.get('telefono', '')
        cotizacion.medidas_alto = form_data.get('medidas_alto')
        cotizacion.medidas_ancho = form_data.get('medidas_ancho')
        cotizacion.medidas_profundidad = form_data.get('medidas_profundidad')
        cotizacion.material_preferido = form_data.get('material_preferido')
        cotizacion.descripcion_proyecto = form_data.get('descripcion_proyecto', '')
        cotizacion.estado = form_data.get('estado')
        cotizacion.admin_notas = form_data.get('admin_notas', '')
        
        precio_cotizado = form_data.get('precio_cotizado')
        if precio_cotizado:
            cotizacion.precio_cotizado = precio_cotizado
        
        # Producto
        producto_id = form_data.get('producto')
        if producto_id:
            try:
                producto = Producto.objects.get(id=producto_id)
                cotizacion.producto = producto
            except Producto.DoesNotExist:
                cotizacion.producto = None
        else:
            cotizacion.producto = None
        
        try:
            cotizacion.save()
            messages.success(request, f'Cotización {cotizacion.folio} actualizada exitosamente.')
            return redirect('admin_cotizacion_detalle', cotizacion_id=cotizacion.id)
        except Exception as e:
            messages.error(request, f'Error al actualizar cotización: {str(e)}')
    
    # GET - mostrar formulario
    productos = Producto.objects.filter(activo=True)
    
    # Calcular precio sugerido
    precio_sugerido = None
    try:
        precio_data = calcular_precio_estimado(cotizacion)
        if precio_data:
            precio_sugerido = precio_data
    except:
        pass
    
    context = {
        'cotizacion': cotizacion,
        'productos': productos,
        'materiales': Cotizacion.MATERIAL_CHOICES,
        'estados': Cotizacion.ESTADO_CHOICES,
        'precio_sugerido': precio_sugerido,
    }
    
    return render(request, 'admin_panel/cotizacion_editar.html', context)
