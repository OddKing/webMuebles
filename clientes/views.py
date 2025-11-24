from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Count
from django.utils import timezone
from .models import Cliente
from .forms import ClienteForm


@login_required(login_url='admin_login')
def admin_clientes_lista(request):
    """Vista para listar todos los clientes con búsqueda"""
    search_query = request.GET.get('q', '')
    
    # Base queryset con anotaciones
    clientes = Cliente.objects.annotate(
        num_cotizaciones=Count('cotizacion')
    )
    
    # Aplicar búsqueda si existe
    if search_query:
        clientes = clientes.filter(
            Q(nombre_completo__icontains=search_query) |
            Q(rut__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(empresa__icontains=search_query)
        )
    
    # Ordenar por última cotización
    clientes = clientes.order_by('-ultima_cotizacion', '-fecha_registro')
    
    context = {
        'clientes': clientes,
        'search_query': search_query,
        'total_clientes': Cliente.objects.filter(activo=True).count(),
        'clientes_count': clientes.count(),
    }
    
    return render(request, 'admin_panel/clientes_lista.html', context)


@login_required(login_url='admin_login')
def admin_cliente_crear(request):
    """Vista para crear un nuevo cliente"""
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            messages.success(request, f'Cliente {cliente.nombre_completo} creado exitosamente.')
            return redirect('admin_cliente_detalle', cliente_id=cliente.id)
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario.')
    else:
        form = ClienteForm()
    
    context = {
        'form': form,
        'titulo': 'Crear Nuevo Cliente',
        'accion': 'Crear'
    }
    
    return render(request, 'admin_panel/cliente_form.html', context)


@login_required(login_url='admin_login')
def admin_cliente_editar(request, cliente_id):
    """Vista para editar un cliente existente"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            cliente = form.save()
            messages.success(request, f'Cliente {cliente.nombre_completo} actualizado exitosamente.')
            return redirect('admin_cliente_detalle', cliente_id=cliente.id)
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario.')
    else:
        form = ClienteForm(instance=cliente)
    
    context = {
        'form': form,
        'cliente': cliente,
        'titulo': f'Editar Cliente: {cliente.nombre_completo}',
        'accion': 'Actualizar'
    }
    
    return render(request, 'admin_panel/cliente_form.html', context)


@login_required(login_url='admin_login')
def admin_cliente_detalle(request, cliente_id):
    """Vista detallada de un cliente con su historial de cotizaciones"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    
    # Obtener cotizaciones del cliente ordenadas por fecha
    cotizaciones = cliente.cotizacion_set.all().order_by('-fecha_solicitud')
    
    # Calcular estadísticas
    total_cotizaciones = cotizaciones.count()
    cotizaciones_aprobadas = cotizaciones.filter(estado='aprobada').count()
    cotizaciones_pendientes = cotizaciones.filter(estado='pendiente_aprobacion').count()
    
    # Calcular total cotizado
    total_cotizado = sum(
        cot.precio_cotizado for cot in cotizaciones 
        if cot.precio_cotizado and cot.estado in ['aprobada', 'aceptada']
    )
    
    context = {
        'cliente': cliente,
        'cotizaciones': cotizaciones[:10],  # Últimas 10
        'total_cotizaciones': total_cotizaciones,
        'cotizaciones_aprobadas': cotizaciones_aprobadas,
        'cotizaciones_pendientes': cotizaciones_pendientes,
        'total_cotizado': total_cotizado,
    }
    
    return render(request, 'admin_panel/cliente_detalle.html', context)


@login_required(login_url='admin_login')
def admin_cliente_eliminar(request, cliente_id):
    """Soft delete - Desactiva el cliente en lugar de eliminarlo"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    cliente = get_object_or_404(Cliente, id=cliente_id)
    
    # Soft delete - solo desactivar
    cliente.activo = False
    cliente.save()
    
    messages.success(request, f'Cliente {cliente.nombre_completo} desactivado exitosamente.')
    return redirect('admin_clientes')


@login_required(login_url='admin_login')
def api_buscar_cliente(request):
    """API para buscar clientes (autocompletado en formularios)"""
    query = request.GET.get('q', '')
    
    if len(query) < 2:
        return JsonResponse({'results': []})
    
    # Buscar clientes activos
    clientes = Cliente.objects.filter(
        Q(nombre_completo__icontains=query) |
        Q(rut__icontains=query) |
        Q(email__icontains=query),
        activo=True
    )[:10]  # Limitar a 10 resultados
    
    resultados = []
    for cliente in clientes:
        resultados.append({
            'id': cliente.id,
            'nombre_completo': cliente.nombre_completo,
            'rut': cliente.rut,
            'email': cliente.email,
            'telefono': cliente.telefono,
            'direccion': cliente.direccion,
            'empresa': cliente.empresa,
            'descuento_habitual': float(cliente.descuento_habitual),
        })
    
    return JsonResponse({'results': resultados})
