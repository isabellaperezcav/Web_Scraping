from bs4 import BeautifulSoup
import requests
import csv

# URL de búsqueda (ejemplo con carros)
url = "https://listado.mercadolibre.com.co/store/belltec"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Encontrar todos los contenedores de productos
productos = soup.find_all("div", class_="ui-search-result__wrapper")

data = []
for prod in productos:
    try:
        titulo = prod.find("a", class_="poly-component__title").get_text(strip=True)
        link = prod.find("a", class_="poly-component__title")["href"]
        precio = prod.find("span", class_="andes-money-amount__fraction").get_text(strip=True)

        # Atributos: año y km
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

        data.append([titulo, precio, anio, km, ubicacion, vendedor, link, img_url])
    except Exception as e:
        print("Error procesando producto:", e)

# Guardar en CSV
with open("productos.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Titulo", "Precio", "Año", "Kilometraje", "Ubicacion", "Vendedor", "Link", "Imagen"])
    writer.writerows(data)

print("Scraping finalizado. Datos guardados en productos.csv")
