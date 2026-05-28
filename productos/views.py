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
    productos = Producto.objects.filter(activo=True).select_related('categoria')
    
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
    
    # Paginación (12 productos por página)
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    paginator = Paginator(productos, 12)
    page_number = request.GET.get('page')
    try:
        productos_paginados = paginator.page(page_number)
    except PageNotAnInteger:
        productos_paginados = paginator.page(1)
    except EmptyPage:
        productos_paginados = paginator.page(paginator.num_pages)
    
    # Obtener todas las categorías para el sidebar
    categorias = Categoria.objects.all().order_by('orden', 'nombre')
    
    context = {
        'productos': productos_paginados,
        'total_productos': productos.count(),
        'categorias': categorias,
        'categoria_actual': categoria_actual,
        'query': query
    }
    
    return render(request, 'catalogo.html', context)
