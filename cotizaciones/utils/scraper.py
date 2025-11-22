import requests
import json
import re
try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

# Configuración de Tiendas
STORES_CONFIG = {
    'sodimac': {
        'name': 'Sodimac',
        'type': 'sodimac_api',
        'url': 'https://sodimac.falabella.com/sodimac-cl/search?Ntt={query}'
    },
    'imperial': {
        'name': 'Imperial',
        'type': 'generic_html', # Placeholder, requiere investigación profunda
        'url': 'https://www.imperial.cl/buscar?q={query}' 
    },
    'provelcar': {
        'name': 'Provelcar',
        'type': 'wordpress',
        'url': 'https://provelcar.cl/?s={query}&post_type=product'
    },
    'hbt': {
        'name': 'Hbt',
        'type': 'generic_html',
        'url': 'https://www.hbt.cl/search?q={query}'
    },
    'ledstudio': {
        'name': 'Led Studio',
        'type': 'wordpress',
        'url': 'https://ledstudio.cl/?s={query}&post_type=product'
    },
    'stonecenter': {
        'name': 'Stone Center',
        'type': 'wordpress',
        'url': 'https://stonecenter.cl/?s={query}&post_type=product'
    },
    'casamura': {
        'name': 'Casa Mura',
        'type': 'wordpress',
        'url': 'https://casamura.cl/?s={query}&post_type=product'
    },
    'forpec': {
        'name': 'Forpec',
        'type': 'wordpress',
        'url': 'https://forpec.cl/?s={query}&post_type=product'
    },
    'dph': {
        'name': 'Dph',
        'type': 'wordpress',
        'url': 'https://dph.cl/?s={query}&post_type=product'
    }
}

def buscar_precios(query, store_key='sodimac'):
    """
    Función principal de búsqueda. Despacha al scraper específico según la tienda.
    """
    store_config = STORES_CONFIG.get(store_key)
    if not store_config:
        return []
        
    if store_config['type'] == 'sodimac_api':
        return buscar_sodimac(query, store_config)
    elif store_config['type'] == 'wordpress':
        return buscar_wordpress(query, store_config)
    else:
        return []

def buscar_sodimac(query, config):
    """Scraper específico para Sodimac (Next.js JSON)"""
    url = config['url'].format(query=query)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    resultados = []
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200: return []
        
        match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', response.text)
        if not match: return []
        
        data = json.loads(match.group(1))
        props = data.get('props', {}).get('pageProps', {})
        products = props.get('results', []) or props.get('searchData', {}).get('results', [])
        
        for prod in products:
            try:
                name = prod.get('displayName', 'Sin nombre')
                prices = prod.get('prices', [])
                price_value = 0
                
                if prices:
                    for p in prices:
                        if 'price' in p:
                            p_val = p['price']
                            price_str = p_val[0] if isinstance(p_val, list) and p_val else str(p_val)
                            clean_price = price_str.replace('$', '').replace('.', '').replace(',', '')
                            price_value = int(clean_price)
                            break
                
                media_urls = prod.get('mediaUrls', [])
                image_url = media_urls[0] if media_urls else ''
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
                        'tienda': config['name']
                    })
            except: continue
            
        return resultados[:10]
    except: return []

def buscar_wordpress(query, config):
    """Scraper genérico para sitios WooCommerce/WordPress"""
    url = config['url'].format(query=query)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    resultados = []
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200: return []
        
        # Extracción básica con Regex (ya que bs4 podría no estar instalado o fallar)
        # Buscamos patrones comunes de WooCommerce
        
        # Patrón 1: Títulos de productos
        # <h2 class="woocommerce-loop-product__title">Nombre</h2>
        titles = re.findall(r'class="woocommerce-loop-product__title">([^<]+)<', response.text)
        
        # Patrón 2: Precios
        # <span class="woocommerce-Price-amount amount"><bdi><span class="woocommerce-Price-currencySymbol">$</span>12.990</bdi></span>
        # Simplificado: buscar "$ 12.990" o "$12.990" cerca de un producto
        
        # Si no podemos parsear bien el HTML con regex (es difícil), intentamos una aproximación
        # O usamos bs4 si el usuario lo tiene (el error anterior sugirió que no)
        
        # Plan B: Regex agresivo para encontrar bloques de productos
        product_blocks = re.split(r'<li[^>]*class="[^"]*product[^"]*"', response.text)
        
        for block in product_blocks[1:]: # Saltamos el primero que es basura antes del primer li
            try:
                # Nombre
                name_match = re.search(r'class="woocommerce-loop-product__title">([^<]+)<', block)
                name = name_match.group(1) if name_match else "Producto sin nombre"
                
                # Precio
                price_match = re.search(r'woocommerce-Price-amount amount".*?>.*?([\d\.]+).*?<', block, re.DOTALL)
                if not price_match:
                    # Intento alternativo
                    price_match = re.search(r'\$([\d\.]+)', block)
                
                price_value = 0
                if price_match:
                    price_str = price_match.group(1).replace('.', '').replace(',', '')
                    if price_str.isdigit():
                        price_value = int(price_str)
                
                # Imagen
                img_match = re.search(r'src="([^"]+)"', block)
                image_url = img_match.group(1) if img_match else ""
                
                # Link
                link_match = re.search(r'href="([^"]+)"', block)
                prod_url = link_match.group(1) if link_match else url
                
                if price_value > 0:
                    resultados.append({
                        'nombre': name,
                        'precio': price_value,
                        'precio_formateado': f"${price_value:,.0f}".replace(',', '.'),
                        'imagen': image_url,
                        'url': prod_url,
                        'tienda': config['name']
                    })
            except: continue
            
        return resultados[:8]
    except Exception as e:
        print(f"Error scraping WP {config['name']}: {e}")
        return []
