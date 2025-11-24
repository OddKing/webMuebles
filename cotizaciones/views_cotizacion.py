"""
Vista para solicitar cotización de productos
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from productos.models import Producto
from .models import Cotizacion, ConsentimientoLegal
from .forms import CotizacionForm
from .utils.folio import generar_folio
from .utils.pdf_generator import generate_quote_pdf


def get_client_ip(request):
    """Obtiene la IP del cliente"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def solicitar_cotizacion(request, producto_id=None):
    """
    Vista para solicitar cotización de un producto o diseño personalizado
    """
    producto = None
    if producto_id:
        # Buscar el producto en los datos hardcodeados
        from productos.views import catalogo as catalogo_view
        productos_data = catalogo_view.__code__.co_consts[1]  # Obtener productos hardcodeados
        
        # Mejor buscar en la base de datos si el producto existe
        try:
            producto = Producto.objects.get(id=producto_id)
        except Producto.DoesNotExist:
            # Si no existe en BD, buscar en datos hardcodeados
            productos_hardcoded = [
                {'id': 1, 'nombre': 'Sofá Moderno', 'descripcion': 'Sofá de 3 puestos con diseño contemporáneo'},
                {'id': 2, 'nombre': 'Mesa de Comedor', 'descripcion': 'Mesa de madera maciza para 6 personas'},
                {'id': 3, 'nombre': 'Silla Ejecutiva', 'descripcion': 'Silla ergonómica para oficina'},
                {'id': 4, 'nombre': 'Librero Minimalista', 'descripcion': 'Estantería moderna de 5 niveles'},
                {'id': 5, 'nombre': 'Cama King Size', 'descripcion': 'Cama de madera con cabecero acolchado'},
                {'id': 6, 'nombre': 'Escritorio Ejecutivo', 'descripcion': 'Escritorio de oficina con cajones'},
                {'id': 7, 'nombre': 'Sillón Reclinable', 'descripcion': 'Sillón individual con sistema reclinable'},
                {'id': 8, 'nombre': 'Rack TV Moderno', 'descripcion': 'Mueble para TV hasta 55 pulgadas'},
            ]
            producto_dict = next((p for p in productos_hardcoded if p['id'] == producto_id), None)
            if producto_dict:
                # Crear un objeto simple para pasar al template
                class ProductoTemp:
                    def __init__(self, data):
                        self.id = data['id']
                        self.nombre = data['nombre']
                        self.descripcion = data['descripcion']
                producto = ProductoTemp(producto_dict)
    
    if request.method == 'POST':
        form = CotizacionForm(request.POST, request.FILES)
        
        if form.is_valid():
            # Guardar la cotización
            cotizacion = form.save(commit=False)
            
            # Asignar producto si existe
            if producto and hasattr(producto, 'pk'):
                cotizacion.producto = producto
            
            # Generar folio único
            cotizacion.folio = generar_folio()
            
            # Guardar cotización
            cotizacion.save()
            
            # Crear registro de consentimiento legal
            ConsentimientoLegal.objects.create(
                cotizacion=cotizacion,
                acepto_terminos=form.cleaned_data['acepto_terminos'],
                acepto_privacidad=form.cleaned_data['acepto_privacidad'],
                version_terminos='1.0',
                version_privacidad='1.0',
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')[:500]
            )
            
            # Generar PDF
            try:
                pdf_buffer = generate_quote_pdf(cotizacion)
                
                # Enviar email con el PDF
                email_context = {
                    'cotizacion': cotizacion,
                    'producto': producto,
                    'folio': cotizacion.folio
                }
                
                html_message = render_to_string(
                    'emails/confirmacion_cotizacion.html',
                    email_context
                )
                
                email = EmailMessage(
                    subject=f'Cotización {cotizacion.folio} - Muebles Barguay',
                    body=html_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[cotizacion.email],
                )
                email.content_subtype = 'html'
                
                # Adjuntar PDF
                email.attach(
                    f'Cotizacion_{cotizacion.folio}.pdf',
                    pdf_buffer.getvalue(),
                    'application/pdf'
                )
                
                email.send(fail_silently=False)
                
                messages.success(
                    request,
                    f'¡Cotización enviada! Revisa tu email para ver los detalles. Folio: {cotizacion.folio}'
                )
                
            except Exception as e:
                # Si falla el envío del email, igual guardamos la cotización
                messages.warning(
                    request,
                    f'Cotización guardada (Folio: {cotizacion.folio}), pero hubo un problema al enviar el email. Nos contactaremos contigo pronto.'
                )
                print(f"Error enviando email: {e}")
            
            return redirect('cotizacion_enviada')
    else:
        form = CotizacionForm()
    
    context = {
        'form': form,
        'producto': producto,
        'producto_id': producto_id
    }
    
    return render(request, 'cotizaciones/solicitar_cotizacion.html', context)


def cotizacion_enviada(request):
    """
    Página de confirmación después de enviar una cotización
    """
    return render(request, 'cotizaciones/cotizacion_enviada.html')
