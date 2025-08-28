"""
Qué podemos extraer con este enfoque
- Nombre del producto
- Precio
- Código del producto (MCO...)
- Link del producto
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.mercadolibre.com.co/tienda/almacenes-hj?item_id=MCO1947417292&category_id=MCO430153&official_store_id=1960&client=recoview-selleritems&recos_listing=true"

# 1. Hacer la petición
headers = {"User-Agent": "Mozilla/5.0"}  
response = requests.get(url, headers=headers)

# Lista donde guardaremos los resultados
data = []

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    # Buscar productos
    productos = soup.find_all("div", class_="ui-search-result__content-wrapper")

    for p in productos:
        # Nombre producto
        nombre = p.find("h2", class_="ui-search-item__title")
        nombre = nombre.text.strip() if nombre else "No disponible"

        # Precio
        precio = p.find("span", class_="andes-money-amount__fraction")
        precio = precio.text.strip() if precio else "No disponible"

        # Enlace
        enlace = p.find("a", class_="ui-search-link")
        enlace = enlace["href"] if enlace else "No disponible"

        # Cod
        cod_producto = None
        if enlace and "MCO" in enlace:
            cod_producto = [part for part in enlace.split("/") if "MCO" in part]
            cod_producto = cod_producto[0] if cod_producto else "No disponible"

        # Agregar a la lista
        data.append({
            "nombre": nombre,
            "precio": precio,
            "link": enlace,
            "codigo": cod_producto
        })

    # Guardar en CSV 
    df = pd.DataFrame(data)
    df.to_csv("productos_Almacenes_HJ.csv", index=False, encoding="utf-8-sig")

    print("✅ Datos guardados en productos_Almacenes_HJ.csv")

else:
    print("Error al acceder:", response.status_code)

