import requests
import json
import re
from decimal import Decimal

def buscar_precios_sodimac(query):
    """
    Busca productos en Sodimac y retorna una lista de resultados con precios.
    """
    url = f"https://sodimac.falabella.com/sodimac-cl/search?Ntt={query}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    resultados = []
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return []
            
        content = response.text
        
        # Extraer JSON de __NEXT_DATA__
        match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', content)
        if not match:
            return []
            
        json_data = match.group(1)
        data = json.loads(json_data)
        
        # Navegar hacia los resultados
        # La estructura puede variar, intentamos varias rutas comunes
        props = data.get('props', {}).get('pageProps', {})
        
        # Ruta 1: results directo
        products = props.get('results', [])
        
        # Ruta 2: searchData -> results
        if not products:
            products = props.get('searchData', {}).get('results', [])
            
        # Procesar productos
        for prod in products:
            try:
                # Nombre
                name = prod.get('displayName', 'Sin nombre')
                
                # Precio
                prices = prod.get('prices', [])
                price_value = 0
                
                if prices:
                    # Intentar obtener el precio de venta o el más bajo
                    # Estructura usual: prices[0]['price'][0] -> string "12.990"
                    # O prices[0]['originalPrice']
                    
                    # Buscamos precio formateado o valor crudo
                    for p in prices:
                        if 'price' in p:
                            # A veces viene como lista de strings ["12.990"]
                            p_val = p['price']
                            if isinstance(p_val, list) and p_val:
                                price_str = p_val[0]
                            else:
                                price_str = str(p_val)
                                
                            # Limpiar precio (quitar $ y puntos)
                            clean_price = price_str.replace('$', '').replace('.', '').replace(',', '')
                            price_value = int(clean_price)
                            break
                
                # Imagen
                media_urls = prod.get('mediaUrls', [])
                image_url = media_urls[0] if media_urls else ''
                
                # URL del producto
                prod_url = prod.get('url', '')
                if prod_url and not prod_url.startswith('http'):
                    prod_url = f"https://sodimac.falabella.com{prod_url}"
                
                if price_value > 0:
                    resultados.append({
                        'nombre': name,
                        'precio': price_value,
                        'precio_formateado': f"${price_value:,.0f}".replace(',', '.'),
                        'imagen': image_url,
                        'url': prod_url,
                        'tienda': 'Sodimac'
                    })
                    
            except Exception as e:
                continue
                
        return resultados[:10] # Retornar top 10
        
    except Exception as e:
        print(f"Error scraping Sodimac: {e}")
        return []
