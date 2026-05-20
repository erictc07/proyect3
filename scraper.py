import requests
from bs4 import BeautifulSoup
import re

def obtener_cartelera():
    url = "https://www.compraentradas.com/Cine/55/cinemes-amposta-11-sales"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        peliculas = []
        
        # Buscamos en las etiquetas habituales de títulos
        for tag in soup.find_all(['h3', 'h4', 'h5', 'strong']):
            texto = tag.get_text(strip=True)
            
            # Limpieza del texto extraído
            texto_limpio = re.sub(r'ESTRENO: \d{2}/\d{2}/\d{4}', '', texto)
            texto_limpio = texto_limpio.replace("COMPRAR", "").replace("DIGITAL", "").replace("CAT", "").replace("VOS", "")
            texto_limpio = re.sub(r'\d{2}:\d{2}', '', texto_limpio)
            texto_limpio = texto_limpio.replace("-", "").strip()
            
            if texto_limpio and len(texto_limpio) > 3 and texto_limpio.isupper() and texto_limpio not in peliculas:
                palabras_ignoradas = [
                    "CARTELERA", "COMPRAENTRADAS", "CONTACTO", "POLÍTICA", 
                    "AVISO", "SESIONES", "UCC", "CONDICIONES", "PRIVACIDAD", 
                    "COOKIES", "PARTNERS", "TODOS LOS PUBLICOS", "CINE"
                ]
                
                es_valido = True
                for palabra in palabras_ignoradas:
                    if palabra in texto_limpio:
                        es_valido = False
                        break
                        
                if es_valido:
                    peliculas.append(texto_limpio)
        
        # --- NUEVO: Guardar el resultado en un archivo de texto ---
        with open("cartelera.txt", "w", encoding="utf-8") as f:
            f.write("🎬 CARTELERA - CINEMES AMPOSTA 11 SALES 🎬\n")
            f.write("=============================================\n")
            
            if not peliculas:
                f.write("⚠️ No se pudieron extraer los títulos con las reglas actuales.\n")
                # Si falla, dejamos pistas en el log de la consola
                print("⚠️ No se encontraron películas. Revisando estructura interna:")
                for tag in soup.find_all(['h3', 'h4', 'h5'])[:15]:
                     print(f"[{tag.name}] -> {tag.get_text(strip=True)}")
            else:
                for pelicula in peliculas:
                    print(f"🍿 {pelicula}") # Se muestra en los logs de GitHub
                    f.write(f"🍿 {pelicula}\n") # Se guarda en el archivo txt
                    
        print("\n💾 ¡Archivo 'cartelera.txt' generado correctamente!")
            
    except Exception as e:
        print(f"❌ Error al conectar o procesar: {e}")

if __name__ == "__main__":
    obtener_cartelera()
