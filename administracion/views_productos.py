from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from productos.models import Producto
from django.core.files.storage import FileSystemStorage

# Create your views here.

@login_required
def lista_productos(request):
    """Vista para listar todos los productos"""
    productos = Producto.objects.all().order_by('orden', '-fecha_creacion')
    
    context = {
        'productos': productos,
        'total_productos': productos.count()
    }
    
    return render(request, 'administracion/productos_lista.html', context)


@login_required
def crear_producto(request):
    """Vista para crear un nuevo producto"""
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            nombre = request.POST.get('nombre')
            descripcion = request.POST.get('descripcion')
            precio = request.POST.get('precio')
            orden = request.POST.get('orden', 0)
            activo = request.POST.get('activo') == 'on'
            imagen = request.FILES.get('imagen')
            
            # Validar campos requeridos
            if not all([nombre, descripcion, precio, imagen]):
                messages.error(request, 'Todos los campos son obligatorios.')
                return redirect('admin_crear_producto')
            
            # Crear producto
            producto = Producto.objects.create(
                nombre=nombre,
                descripcion=descripcion,
                precio=precio,
                orden=orden,
                activo=activo,
                imagen=imagen
            )
            
            messages.success(request, f'Producto "{producto.nombre}" creado exitosamente.')
            return redirect('admin_lista_productos')
            
        except Exception as e:
            messages.error(request, f'Error al crear el producto: {str(e)}')
            return redirect('admin_crear_producto')
    
    return render(request, 'administracion/producto_form.html', {
        'titulo': 'Crear Producto',
        'accion': 'Crear'
    })


@login_required
def editar_producto(request, producto_id):
    """Vista para editar un producto existente"""
    producto = get_object_or_404(Producto, id=producto_id)
    
    if request.method == 'POST':
        try:
            # Actualizar datos
            producto.nombre = request.POST.get('nombre')
            producto.descripcion = request.POST.get('descripcion')
            producto.precio = request.POST.get('precio')
            producto.orden = request.POST.get('orden', 0)
            producto.activo = request.POST.get('activo') == 'on'
            
            # Actualizar imagen si se proporciona una nueva
            if 'imagen' in request.FILES:
                producto.imagen = request.FILES['imagen']
            
            producto.save()
            
            messages.success(request, f'Producto "{producto.nombre}" actualizado exitosamente.')
            return redirect('admin_lista_productos')
            
        except Exception as e:
            messages.error(request, f'Error al actualizar el producto: {str(e)}')
            return redirect('admin_editar_producto', producto_id=producto_id)
    
    context = {
        'titulo': 'Editar Producto',
        'accion': 'Actualizar',
        'producto': producto
    }
    
    return render(request, 'administracion/producto_form.html', context)


@login_required
def eliminar_producto(request, producto_id):
    """Vista para eliminar (desactivar) un producto"""
    producto = get_object_or_404(Producto, id=producto_id)
    
    if request.method == 'POST':
        # Soft delete: marcar como inactivo en lugar de eliminar
        producto.activo = False
        producto.save()
        
        messages.success(request, f'Producto "{producto.nombre}" desactivado exitosamente.')
        return redirect('admin_lista_productos')
    
    context = {
        'producto': producto
    }
    
    return render(request, 'administracion/producto_confirmar_eliminar.html', context)
