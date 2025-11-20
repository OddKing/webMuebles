from django.shortcuts import render

# Create your views here.

def catalogo(request):
    # Productos de ejemplo para la tienda de muebles
    productos = [
        {
            'id': 1,
            'nombre': 'Sofá Moderno',
            'descripcion': 'Sofá de 3 puestos con diseño contemporáneo',
            'precio': '$450.000',
            'imagen': 'img/1.jpeg'
        },
        {
            'id': 2,
            'nombre': 'Mesa de Comedor',
            'descripcion': 'Mesa de madera maciza para 6 personas',
            'precio': '$320.000',
            'imagen': 'img/2.jpeg'
        },
        {
            'id': 3,
            'nombre': 'Silla Ejecutiva',
            'descripcion': 'Silla ergonómica para oficina',
            'precio': '$89.000',
            'imagen': 'img/3.jpeg'
        },
        {
            'id': 4,
            'nombre': 'Librero Minimalista',
            'descripcion': 'Estantería moderna de 5 niveles',
            'precio': '$125.000',
            'imagen': 'img/4.jpeg'
        },
        {
            'id': 5,
            'nombre': 'Cama King Size',
            'descripcion': 'Cama de madera con cabecero acolchado',
            'precio': '$580.000',
            'imagen': 'img/5.jpeg'
        },
        {
            'id': 6,
            'nombre': 'Escritorio Ejecutivo',
            'descripcion': 'Escritorio de oficina con cajones',
            'precio': '$210.000',
            'imagen': 'img/6.jpeg'
        },
        {
            'id': 7,
            'nombre': 'Sillón Reclinable',
            'descripcion': 'Sillón individual con sistema reclinable',
            'precio': '$195.000',
            'imagen': 'img/7.jpeg'
        },
        {
            'id': 8,
            'nombre': 'Rack TV Moderno',
            'descripcion': 'Mueble para TV hasta 55 pulgadas',
            'precio': '$145.000',
            'imagen': 'img/8.jpeg'
        },
    ]
    
    context = {
        'productos': productos,
        'total_productos': len(productos)
    }
    
    return render(request, 'catalogo.html', context)
