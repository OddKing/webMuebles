from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .utils.scraper import buscar_precios
from .models import Cotizacion

@login_required
def api_search_material_prices(request):
    """
    API para buscar precios de materiales en tiendas externas.
    Recibe 'query' y 'store' (opcional) por GET.
    """
    query = request.GET.get('query', '')
    store = request.GET.get('store', 'sodimac')
    
    if not query:
        return JsonResponse({'error': 'Query parameter is required'}, status=400)
        
    try:
        resultados = buscar_precios(query, store_key=store)
        return JsonResponse({'results': resultados})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
