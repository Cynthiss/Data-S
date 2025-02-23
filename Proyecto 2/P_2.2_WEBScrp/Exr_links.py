import requests
from bs4 import BeautifulSoup

# URL del listado de propiedades
listado_url = "https://mapainmueble.com/apartamentos-en-alquiler-zona-14/"

# Simular un navegador para evitar bloqueos
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Hacer la solicitud HTTP
response = requests.get(listado_url, headers=headers)

# Verificar si la página respondió correctamente
if response.status_code == 200:
    print("[✅] Conexión exitosa con la página de listado.")

    # Crear objeto BeautifulSoup con el HTML de la página
    soup = BeautifulSoup(response.text, "html.parser")

    # Encontrar todos los contenedores de propiedades
    propiedad_links = []
    contenedores = soup.find_all("div", class_="col-md-4 has_prop_slider listing_wrapper")

    for contenedor in contenedores:
        url = contenedor.get("data-modal-link")  # Extraer la URL desde el atributo data-modal-link
        if url:
            propiedad_links.append(url)

    # 📌 Mostrar los enlaces encontrados
    print("\n🔹 **Propiedades encontradas:**")
    for i, link in enumerate(propiedad_links, 1):
        print(f"{i}. {link}")

    # 📌 Número total de propiedades encontradas
    print(f"\n[✅] Total de propiedades encontradas: {len(propiedad_links)}")

else:
    print(f"[❌] Error al acceder a la página. Código: {response.status_code}")
