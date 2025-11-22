import requests

stores = [
    {"name": "Imperial", "url": "https://www.imperial.cl/buscar?q=melamina"},
    {"name": "CHC", "url": "https://www.chc.cl/catalogsearch/result/?q=lavamanos"}, # CHC es baños/cocinas
    {"name": "Provelcar", "url": "https://provelcar.cl/?s=melamina&post_type=product"}, # Probable WordPress
    {"name": "Hbt", "url": "https://www.hbt.cl/search?q=bisagra"},
    {"name": "Dph", "url": "https://dph.cl/?s=tirador&post_type=product"}, # Probable WordPress
    {"name": "Led Studio", "url": "https://ledstudio.cl/?s=cinta&post_type=product"}, # Probable WordPress
    {"name": "Masisa", "url": "https://www.masisa.com/cl/buscar?q=melamina"}, # A veces es solo catalogo
    {"name": "Stone Center", "url": "https://stonecenter.cl/?s=cuarzo&post_type=product"}, # Probable WordPress
    {"name": "Casa Mura", "url": "https://casamura.cl/?s=papel&post_type=product"}, # Probable WordPress
    {"name": "Cubiertas", "url": "https://cubiertas.cl/search?q=cubierta"}, # Adivinando
    {"name": "Forpec", "url": "https://forpec.cl/?s=canto&post_type=product"} # Probable WordPress
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

for store in stores:
    try:
        print(f"Testing {store['name']}...")
        response = requests.get(store['url'], headers=headers, timeout=5)
        print(f"  Status: {response.status_code}")
        print(f"  Length: {len(response.text)}")
        if response.status_code == 200:
            if "product" in response.text.lower() or "resultado" in response.text.lower() or "encontrado" in response.text.lower():
                 print("  ✅ Seems valid")
            else:
                 print("  ⚠️ Content might be empty or different structure")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    print("-" * 20)
