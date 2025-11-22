import requests
import json
import re

url = "https://sodimac.falabella.com/sodimac-cl/search?Ntt=melamina"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

try:
    response = requests.get(url, headers=headers, timeout=10)
    content = response.text
    
    print(f"Status Code: {response.status_code}")
    print(f"Content Length: {len(content)}")
    
    # Buscar __NEXT_DATA__
    if "__NEXT_DATA__" in content:
        print("✅ FOUND __NEXT_DATA__")
        # Extraer el JSON
        match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', content)
        if match:
            json_data = match.group(1)
            data = json.loads(json_data)
            print("✅ JSON Parsed Successfully")
            
            # Intentar encontrar productos
            try:
                # La estructura suele variar, pero buscamos 'results' o 'products'
                props = data.get('props', {}).get('pageProps', {})
                print(f"Keys in pageProps: {list(props.keys())}")
                
                # Navegar por la estructura común de Falabella/Sodimac
                results = props.get('results', [])
                if not results:
                     # A veces está en 'searchData' -> 'results'
                    results = props.get('searchData', {}).get('results', [])
                
                print(f"Found {len(results)} products (if list)")
                
                if results and isinstance(results, list):
                    first = results[0]
                    print(f"First Product Sample: {json.dumps(first, indent=2)[:500]}")
            except Exception as e:
                print(f"Error navigating JSON: {e}")
    else:
        print("❌ __NEXT_DATA__ NOT FOUND")
        
except Exception as e:
    print(f"Error: {e}")
