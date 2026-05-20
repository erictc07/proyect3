import requests
from bs4 import BeautifulSoup

def obtener_cartelera():
    url = "https://www.compraentradas.com/Cine/55/cinemes-amposta-11-sales"
    # Añadimos un User-Agent para simular que somos un navegador web normal y evitar bloqueos
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    
    try:
        print("Obteniendo datos de la taquilla...\n")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Parseamos el HTML de la página
        soup = BeautifulSoup(response.text, 'html.parser')
        
        peliculas = []
        
        # En la web de CompraEntradas, los títulos de las películas suelen estar en etiquetas <h3> o <h4>
        for tag in soup.find_all(['h3', 'h4']):
            titulo = tag.get_text(strip=True)
            # Filtramos textos vacíos y palabras que no son películas
            if titulo and len(titulo) > 2 and titulo not in peliculas:
                if "ESTRENO" not in titulo and "COMPRAR" not in titulo:
                    peliculas.append(titulo)
        
        # Palabras comunes de la web que queremos ignorar
        palabras_ignoradas = ["Cartelera", "Compraentradas", "Contacto", "Política", "Aviso", "Condiciones", "UCC"]
        peliculas_filtradas = [p for p in peliculas if not any(palabra in p for palabra in palabras_ignoradas)]
        
        print("🎬 CARTELERA - CINEMES AMPOSTA 11 SALES 🎬")
        print("=" * 45)
        for pelicula in peliculas_filtradas:
            print(f"🍿 {pelicula}")
            
    except Exception as e:
        print(f"❌ Error al obtener la cartelera: {e}")

if __name__ == "__main__":
    obtener_cartelera()
