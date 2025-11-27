from django.shortcuts import render
from django.db.models import Q
from .models import Producto, Categoria

# Create your views here.

def catalogo(request):
    """
    Vista del catálogo de productos con búsqueda y filtros.
    """
    # Obtener parámetros de búsqueda y filtro
    query = request.GET.get('q')
    categoria_slug = request.GET.get('categoria')
    
    # Base queryset
    productos = Producto.objects.filter(activo=True)
    
    # Aplicar búsqueda por texto
    if query:
        productos = productos.filter(
            Q(nombre__icontains=query) | 
            Q(descripcion__icontains=query)
        )
    
    # Aplicar filtro por categoría
    categoria_actual = None
    if categoria_slug:
        try:
            categoria_actual = Categoria.objects.get(slug=categoria_slug)
            productos = productos.filter(categoria=categoria_actual)
        except Categoria.DoesNotExist:
            pass
            
    # Ordenar resultados
    productos = productos.order_by('orden', '-fecha_creacion')
    
    # Obtener todas las categorías para el sidebar
    categorias = Categoria.objects.all().order_by('orden', 'nombre')
    
    context = {
        'productos': productos,
        'total_productos': productos.count(),
        'categorias': categorias,
        'categoria_actual': categoria_actual,
        'query': query
    }
    
    return render(request, 'catalogo.html', context)
