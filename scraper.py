import requests
from bs4 import BeautifulSoup

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
        
        # Ampliamos la búsqueda a enlaces, negritas y más encabezados
        for tag in soup.find_all(['h2', 'h3', 'h4', 'h5', 'strong', 'a', 'span']):
            titulo = tag.get_text(strip=True)
            
            # Los títulos en esta web suelen estar en mayúsculas y tener más de 3 letras
            if titulo and len(titulo) > 3 and titulo.isupper():
                
                # Filtramos palabras en mayúsculas de la web que NO son películas
                palabras_ignoradas = [
                    "CARTELERA", "COMPRAENTRADAS", "CONTACTO", "POLÍTICA", 
                    "AVISO", "SESIONES", "COMPRAR", "ESTRENO", "DIGITAL", 
                    "UCC", "CONDICIONES", "PRIVACIDAD", "COOKIES", "PARTNERS",
                    "TODOS LOS PUBLICOS", "VOS"
                ]
                
                # Verificamos que el texto no contenga palabras del menú
                es_valido = True
                for palabra in palabras_ignoradas:
                    if palabra in titulo:
                        es_valido = False
                        break
                        
                if es_valido and titulo not in peliculas:
                    peliculas.append(titulo)
        
        print("🎬 CARTELERA - CINEMES AMPOSTA 11 SALES 🎬")
        print("=============================================")
        
        if not peliculas:
            print("⚠️ No se encontraron películas. Revisa el código fuente de la web.")
        else:
            for pelicula in peliculas:
                print(f"🍿 {pelicula}")
            
    except Exception as e:
        print(f"❌ Error al obtener la cartelera: {e}")

if __name__ == "__main__":
    obtener_cartelera()
