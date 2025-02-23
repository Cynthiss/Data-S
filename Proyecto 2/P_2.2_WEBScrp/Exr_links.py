import requests
from bs4 import BeautifulSoup

# URL base del listado de propiedades
url_base = "https://mapainmueble.com/apartamentos-en-alquiler-zona-14/"

# Simular un navegador para evitar bloqueos
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# 📌 FUNCION PARA OBTENER TODAS LAS PROPIEDADES DE TODAS LAS PÁGINAS
def obtener_links_propiedades():
    propiedad_links = []
    pagina_actual = 1

    while True:
        # Construir la URL de la página actual
        url_pagina = f"{url_base}page/{pagina_actual}/" if pagina_actual > 1 else url_base
        print(f"[🔍] Extrayendo propiedades de: {url_pagina}")

        # Hacer la solicitud HTTP
        response = requests.get(url_pagina, headers=headers)

        # Verificar si la página responde correctamente
        if response.status_code != 200:
            print(f"[❌] No se pudo acceder a la página {pagina_actual}. Código: {response.status_code}")
            break

        # Crear objeto BeautifulSoup con el HTML de la página
        soup = BeautifulSoup(response.text, "html.parser")

        # Buscar todos los contenedores de propiedades
        contenedores = soup.find_all("div", class_="col-md-4 has_prop_slider listing_wrapper")
        if not contenedores:
            print(f"[🚫] No se encontraron propiedades en la página {pagina_actual}. Deteniendo búsqueda.")
            break

        # Extraer los links desde `data-modal-link`
        for contenedor in contenedores:
            url = contenedor.get("data-modal-link")
            if url:
                propiedad_links.append(url)

        # Buscar la paginación
        paginacion = soup.find("ul", class_="pagination")
        if not paginacion or not soup.find("a", text=str(pagina_actual + 1)):
            print(f"[✅] No hay más páginas después de la {pagina_actual}. Finalizando extracción.")
            break

        # Pasar a la siguiente página
        pagina_actual += 1

    print(f"\n[✅] Total de propiedades encontradas: {len(propiedad_links)}")
    return propiedad_links

# 📌 Ejecutar el scraper y obtener los links de todas las propiedades
links = obtener_links_propiedades()

# 📌 Mostrar los links extraídos
print("\n🔹 **Propiedades encontradas:**")
for i, link in enumerate(links, 1):
    print(f"{i}. {link}")
