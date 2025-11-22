from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .utils.scraper import buscar_precios_sodimac
from .models import Cotizacion

@login_required
def api_search_material_prices(request):
    """
    API para buscar precios de materiales en tiendas externas (Sodimac).
    Recibe 'query' por GET.
    """
    query = request.GET.get('query', '')
    if not query:
        return JsonResponse({'error': 'Query parameter is required'}, status=400)
        
    try:
        resultados = buscar_precios_sodimac(query)
        return JsonResponse({'results': resultados})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
