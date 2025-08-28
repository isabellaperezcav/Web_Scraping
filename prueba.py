from bs4 import BeautifulSoup
import requests
import csv
import time

url = "https://listado.mercadolibre.com.co/store/belltec"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

productos = soup.find_all("div", class_="ui-search-result__wrapper")

data = []

for prod in productos:
    try:
        titulo = prod.find("a", class_="poly-component__title").get_text(strip=True)
        link = prod.find("a", class_="poly-component__title")["href"]
        precio = prod.find("span", class_="andes-money-amount__fraction").get_text(strip=True)

        atributos = prod.find("ul", class_="poly-attributes_list")
        if atributos:
            detalles = [li.get_text(strip=True) for li in atributos.find_all("li")]
            anio = detalles[0] if len(detalles) > 0 else None
            km = detalles[1] if len(detalles) > 1 else None
        else:
            anio, km = None, None

        ubicacion = prod.find("span", class_="poly-component__location")
        ubicacion = ubicacion.get_text(strip=True) if ubicacion else None

        vendedor = prod.find("span", class_="poly-component__seller")
        vendedor = vendedor.get_text(strip=True) if vendedor else None

        img = prod.find("img", class_="poly-component__picture")
        img_url = img.get("data-src") if img else None

        # Ahora: entrar a la página del producto para sacar más info
        r_detalle = requests.get(link, headers=headers)
        s_detalle = BeautifulSoup(r_detalle.text, "html.parser")

        # Ejemplos de datos adicionales
        descripcion = s_detalle.find("p", class_="ui-pdp-description__content")
        descripcion = descripcion.get_text(strip=True) if descripcion else None

        detalles_extra = {}
        for li in s_detalle.find_all("tr", class_="ui-pdp-specs__table__row"):
            key = li.find("th").get_text(strip=True)
            val = li.find("td").get_text(strip=True)
            detalles_extra[key] = val

        combustible = detalles_extra.get("Combustible")
        transmision = detalles_extra.get("Transmisión")
        color = detalles_extra.get("Color")
        puertas = detalles_extra.get("Puertas")

        data.append([
            titulo, precio, anio, km, ubicacion, vendedor, link, img_url,
            combustible, transmision, color, puertas, descripcion
        ])

        time.sleep(1)  # evitar baneos
    except Exception as e:
        print("Error procesando producto:", e)

# Guardar en CSV extendido
with open("productos_detallados.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "Titulo", "Precio", "Año", "Kilometraje", "Ubicacion", "Vendedor", "Link", "Imagen",
        "Combustible", "Transmision", "Color", "Puertas", "Descripcion"
    ])
    writer.writerows(data)

print("Scraping extendido listo 🚀 -> productos_detallados.csv")
