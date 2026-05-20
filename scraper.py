import requests
from bs4 import BeautifulSoup
import re

def obtener_cartelera():
    url = "https://www.compraentradas.com/Cine/55/cinemes-amposta-11-sales"
    # Cabeceras avanzadas para evitar bloqueos del servidor
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3",
        "Connection": "keep-alive"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        peliculas = []
        
        # ESTRATEGIA A: Extraer títulos de los enlaces que apuntan a "/Pelicula/" o de los carteles
        enlaces = soup.find_all('a')
        for a in enlaces:
            href = a.get('href', '')
            # Buscamos enlaces que lleven a la ficha de una película
            if '/Pelicula/' in href or '/pelicula/' in href:
                titulo = a.get_text(strip=True)
                
                # Si el enlace no tiene texto, miramos si dentro hay una imagen y sacamos su atributo 'alt'
                if not titulo:
                    img = a.find('img')
                    if img:
                        titulo = img.get('alt') or img.get('title')
                        
                if titulo:
                    # Limpiamos el texto de basura comercial
                    texto_limpio = titulo.replace("COMPRAR", "").replace("DIGITAL", "").replace("CAT", "").replace("VOS", "")
                    texto_limpio = re.sub(r'(?i)ESTRENO.*', '', texto_limpio)
                    texto_limpio = re.sub(r'\d{2}:\d{2}', '', texto_limpio)
                    texto_limpio = texto_limpio.replace("-", "").strip()
                    
                    # Filtro de validez
                    if len(texto_limpio) > 3 and texto_limpio.upper() not in [p.upper() for p in peliculas]:
                         basura = ["CARTELERA", "COMPRAENTRADAS", "POLÍTICA", "AVISO", "SESIONES", "UCC"]
                         if not any(b in texto_limpio.upper() for b in basura):
                             peliculas.append(texto_limpio.upper())
        
        # ESTRATEGIA B: Si la web no usa enlaces directos, leemos cualquier encabezado que esté cerca de "ESTRENO" o "Digital"
        if not peliculas:
            for tag in soup.find_all(['h3', 'h4', 'h5', 'h6', 'strong']):
                texto = tag.get_text(strip=True)
                # Buscamos textos en mayúsculas que NO sean fechas ni horas
                if not re.search(r'\d{2}/\d{2}/\d{4}', texto) and not re.search(r'\d{2}:\d{2}', texto):
                    if len(texto) > 3 and texto.isupper() and texto not in peliculas:
                        basura = ["CARTELERA", "COMPRAENTRADAS", "POLÍTICA", "AVISO", "SESIONES", "UCC", "COMPRAR", "DIGITAL", "ESTRENO"]
                        if not any(b in texto for b in basura):
                            peliculas.append(texto)

        # GUARDADO DEL RESULTADO
        with open("cartelera.txt", "w", encoding="utf-8") as f:
            f.write("🎬 CARTELERA - CINEMES AMPOSTA 11 SALES 🎬\n")
            f.write("=============================================\n")
            
            if not peliculas:
                msg = "⚠️ No se encontraron películas. Es posible que el cine esté bloqueando conexiones automatizadas."
                f.write(msg + "\n")
                print(msg)
            else:
                for pelicula in peliculas:
                    print(f"🍿 {pelicula}")
                    f.write(f"🍿 {pelicula}\n")
                    
        print("\n💾 ¡Archivo 'cartelera.txt' generado correctamente!")
            
    except Exception as e:
        print(f"❌ Error al conectar o procesar la web: {e}")

if __name__ == "__main__":
    obtener_cartelera()
