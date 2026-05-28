import os
from PIL import Image

def compress_images():
    img_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Buscando imágenes en: {img_dir}")
    
    # Listar todas las imágenes en el directorio
    files = os.listdir(img_dir)
    carousel_files = [f for f in files if f.split('.')[0].isdigit() and f.split('.')[-1].lower() in ['jpg', 'jpeg', 'png']]
    
    # Asegurar que se procesan todas las imágenes del 1 al 13
    print(f"Archivos encontrados para procesar: {carousel_files}")
    
    for filename in carousel_files:
        filepath = os.path.join(img_dir, filename)
        name, ext = os.path.splitext(filename)
        output_filename = f"{name}.webp"
        output_filepath = os.path.join(img_dir, output_filename)
        
        try:
            print(f"Procesando: {filename} ({os.path.getsize(filepath) / 1024:.1f} KB)...")
            with Image.open(filepath) as img:
                # Redimensionar si es mayor a 1920px en ancho/alto
                max_size = 1920
                if img.width > max_size or img.height > max_size:
                    img.thumbnail((max_size, max_size))
                    print(f"   -> Redimensionado a {img.width}x{img.height}")
                    
                # Guardar en formato WEBP
                img.save(output_filepath, 'WEBP', quality=80)
            
            new_size = os.path.getsize(output_filepath)
            print(f"   -> Guardado como {output_filename} ({new_size / 1024:.1f} KB)")
            
            # Eliminar original si se guardó con éxito
            if os.path.exists(output_filepath) and new_size > 0:
                os.remove(filepath)
                print(f"   -> Eliminado original: {filename}")
                
        except Exception as e:
            print(f"   [Error] procesando {filename}: {e}")

if __name__ == "__main__":
    compress_images()
