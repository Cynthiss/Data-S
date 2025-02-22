import requests
from bs4 import BeautifulSoup

# URL de la propiedad
url = "https://mapainmueble.com/properties/apartamento-en-alquiler-santa-ines-zona-14-amueblado-de-3-dormitorios-daa41616/"

# Simular un navegador para evitar bloqueos
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Hacer la solicitud HTTP
response = requests.get(url, headers=headers)

# Verificar si la página respondió correctamente
if response.status_code == 200:
    print("[✅] Conexión exitosa: Código 200")

    # Crear objeto BeautifulSoup con el HTML de la página
    soup = BeautifulSoup(response.text, "html.parser")

    # Intentar encontrar el contenedor del precio
    precio_container = soup.find(lambda tag: tag.name == "div" and "Precio:" in tag.text)

    # Extraer el texto del precio si se encuentra
    if precio_container:
        print("\n🔹 Contenido donde se encuentra el precio:")
        print(precio_container.prettify())

    # Intentar encontrar los detalles de la propiedad
    detalles_contenedor = soup.find(lambda tag: tag.name == "div" and "Dormitorios" in tag.text)

    if detalles_contenedor:
        print("\n🔹 Contenido donde están los detalles:")
        print(detalles_contenedor.prettify())

else:
    print(f"[❌] Error al acceder a la página. Código: {response.status_code}")
