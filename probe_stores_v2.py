import requests

stores = [
    # Imperial: Intentando otra ruta común
    {"name": "Imperial", "url": "https://www.imperial.cl/buscador/productos?texto=melamina"},
    
    # Tiendas que parecen WooCommerce (clases típicas: .product, .price)
    {"name": "Provelcar", "url": "https://provelcar.cl/?s=melamina&post_type=product"},
    {"name": "Dph", "url": "https://dph.cl/?s=tirador&post_type=product"},
    {"name": "Led Studio", "url": "https://ledstudio.cl/?s=cinta&post_type=product"},
    {"name": "Stone Center", "url": "https://stonecenter.cl/?s=cuarzo&post_type=product"},
    {"name": "Casa Mura", "url": "https://casamura.cl/?s=papel&post_type=product"},
    {"name": "Forpec", "url": "https://forpec.cl/?s=canto&post_type=product"}
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

for store in stores:
    try:
        print(f"Testing {store['name']}...")
        response = requests.get(store['url'], headers=headers, timeout=10)
        print(f"  Status: {response.status_code}")
        
        if response.status_code == 200:
            # Verificar si es WooCommerce buscando clases típicas
            if "woocommerce" in response.text.lower() or "type-product" in response.text.lower():
                print("  ✅ Detected WooCommerce structure")
            elif "imperial" in store['name']:
                print("  ✅ Imperial responded (check content manually)")
            else:
                print("  ⚠️ Response OK but structure unknown")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    print("-" * 20)
