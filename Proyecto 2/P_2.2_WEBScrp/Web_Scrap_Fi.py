import requests
from bs4 import BeautifulSoup
import csv
import time

# Simular un navegador para evitar bloqueos
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# 📌 FUNCIÓN PARA EXTRAER DATOS DE UNA PROPIEDAD
def extraer_datos_propiedad(url):
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None  # No guardamos propiedades que no respondan correctamente

    soup = BeautifulSoup(response.text, "html.parser")

    # 🏡 EXTRAER DATOS DE LA PROPIEDAD
    detalles_contenedor = soup.find("div", id="collapseOne")
    datos_extraidos = {}

    if detalles_contenedor:
        detalles = detalles_contenedor.find_all("div", class_="listing_detail col-md-4")
        for detalle in detalles:
            label = detalle.find("strong")  # Buscar etiqueta con título (ej: "Precio:")
            if label:
                value = label.next_sibling  # Obtener el valor exacto
                if value and isinstance(value, str):  # Verificar que sea texto
                    datos_extraidos[label.text.strip()] = value.strip()
                else:
                    datos_extraidos[label.text.strip()] = "No disponible"

    # 📍 EXTRAER UBICACIÓN
    ubicacion_contenedor = soup.find("div", class_="panel-body")
    ubicacion_datos = {}

    if ubicacion_contenedor:
        ubicaciones = ubicacion_contenedor.find_all("div", class_="listing_detail col-md-4")
        for ubicacion in ubicaciones:
            label = ubicacion.find("strong")
            if label:
                value = (
                    ubicacion.find("a").text.strip()
                    if ubicacion.find("a")
                    else label.next_sibling if label.next_sibling else "No disponible"
                )
                if value and isinstance(value, str):  # Verificar que sea texto
                    ubicacion_datos[label.text.strip()] = value.strip()
                else:
                    ubicacion_datos[label.text.strip()] = "No disponible"

    # 📌 EXTRAER LINK DE GOOGLE MAPS
    google_maps_link = soup.find("a", class_="acc_google_maps")["href"] if soup.find("a", class_="acc_google_maps") else "No disponible"

    # 🏠 EXTRAER TIPO DE PROPIEDAD Y ESTADO DESDE EL HTML
    tipo_propiedad = "No disponible"
    estado_propiedad = "No disponible"

    tipo_estado_container = soup.find("div", class_="cat_n_type")

    if tipo_estado_container:
        labels = tipo_estado_container.find_all("div", class_="property_title_label")
        if len(labels) >= 2:
            estado_propiedad = labels[0].text.strip()  # Alquiler o Venta
            tipo_propiedad = labels[1].text.strip()  # Apartamento o Casa
        elif len(labels) == 1:
            estado_propiedad = labels[0].text.strip()  # En caso de que solo haya uno

    # 📌 ORGANIZAR LOS DATOS EXTRAÍDOS Y FORMATEAR EL TAMAÑO EN m²
    tamaño_propiedad = datos_extraidos.get("Tamaño de la propiedad:", "No disponible")
    if tamaño_propiedad != "No disponible" and "m" in tamaño_propiedad:
        tamaño_propiedad = tamaño_propiedad.replace("m", "m²")

    datos_propiedad = {
        "URL": url,
        "Estado": estado_propiedad,
        "Tipo de Propiedad": tipo_propiedad,
        "Precio": datos_extraidos.get("Precio:", "No disponible"),
        "Tamaño de la propiedad": tamaño_propiedad,
        "Parqueos": datos_extraidos.get("Parqueos:", "No disponible"),
        "Dormitorios": datos_extraidos.get("Dormitorios:", "No disponible"),
        "Baños": datos_extraidos.get("Baños:", "No disponible"),
        "ID de la propiedad": datos_extraidos.get("ID de la propiedad:", "No disponible"),
        "Ciudad": ubicacion_datos.get("Ciudad:", "No disponible"),
        "Área": ubicacion_datos.get("Área:", "No disponible"),
        "Sub-Sector/Proyecto": ubicacion_datos.get("Sub-Sector/Proyecto:", "No disponible"),
        "Google Maps": google_maps_link,
    }

    return datos_propiedad

# 📌 FUNCIÓN PARA LEER CSV DE LINKS Y EXTRAER DATOS
def procesar_propiedades():
    datos_completos = []
    errores = []

    # 📌 LEER CSV DE LINKS
    with open("propiedades_links.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # Saltar encabezado
        for i, row in enumerate(reader, 1):
            url = row[0]

            # Intentar extraer datos con reintentos si hay fallos de conexión
            for intento in range(3):
                datos = extraer_datos_propiedad(url)
                if datos:
                    datos_completos.append(datos)
                    break  # Si extrae bien, no reintentar
                else:
                    time.sleep(5)  # Esperar 5 segundos antes de reintentar

            if not datos:
                errores.append([url])  # Guardamos los links con error

    # 📌 GUARDAR LOS DATOS EN CSV
    if datos_completos:
        with open("propiedades_completas.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=datos_completos[0].keys())
            writer.writeheader()
            writer.writerows(datos_completos)

    # 📌 GUARDAR ERRORES EN CSV
    if errores:
        with open("propiedades_errores.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["URL"])  # Encabezado
            writer.writerows(errores)

    # 📌 MOSTRAR SOLO RESULTADO FINAL
    print(f"\n[✅] Se procesaron {len(datos_completos)} propiedades correctamente.")
    if errores:
        print(f"[⚠️] {len(errores)} propiedades tuvieron errores y se guardaron en 'propiedades_errores.csv'.")

# 📌 Ejecutar extracción de datos
procesar_propiedades()
