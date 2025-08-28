import requests
from bs4 import BeautifulSoup
import pandas as pd

# 1. Hacer la solicitud a la página web
url = "https://www.mercadolibre.com.co/tienda/belltec?item_id=MCO1149811466&category_id=MCO167012&official_store_id=515&client=recoview-selleritems&recos_listing=true#origin=pdp&component=sellerData&typeSeller=official_store"

response = requests.get(url)
data = response.json()

productos = []
for item in data["results"]:
    productos.append({
        "id": item["id"],
        "nombre": item["title"],
        "precio": item["price"],
        "link": item["permalink"],
        "vendidos": item.get("sold_quantity", "No disponible"),
        "envio_gratis": item["shipping"]["free_shipping"],
        "tipo_envio": item["shipping"].get("logistic_type", "N/A"),
    })

df = pd.DataFrame(productos)
df.to_csv("productos_belltec.csv", index=False, encoding="utf-8-sig")

print(df.head())
