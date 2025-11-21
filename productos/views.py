from django.shortcuts import render
from .models import Producto

# Create your views here.

def catalogo(request):
    """
    Vista del catálogo de productos.
    Muestra productos activos desde la base de datos.
    """
    # Obtener productos activos ordenados por 'orden' y fecha de creación
    productos = Producto.objects.filter(activo=True).order_by('orden', '-fecha_creacion')
    
    context = {
        'productos': productos,
        'total_productos': productos.count()
    }
    
    return render(request, 'catalogo.html', context)
