import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# URL de ejemplo
URL = "https://listado.mercadolibre.com.co/herramientas"

# Configurar Chrome
chrome_options = Options()
chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get(URL)

# Esperar a que cargue la primera tanda de productos
time.sleep(3)

# Hacer scroll para cargar más resultados
SCROLLS = 10  # número de bajadas de scroll, ajusta si quieres más productos
for i in range(SCROLLS):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)  # espera a que cargue cada tanda

# Extraer los productos
productos = driver.find_elements(By.CSS_SELECTOR, "li.ui-search-layout__item")

data = []
for p in productos:
    try:
        nombre = p.find_element(By.CSS_SELECTOR, "h2.ui-search-item__title").text
    except:
        nombre = ""
    try:
        precio = p.find_element(By.CSS_SELECTOR, "span.price-tag-fraction").text
    except:
        precio = ""
    try:
        link = p.find_element(By.CSS_SELECTOR, "a.ui-search-item__group__element").get_attribute("href")
    except:
        link = ""
    try:
        vendidos = p.find_element(By.CSS_SELECTOR, ".ui-search-stats__highlight").text
    except:
        vendidos = ""
    try:
        envio = p.find_element(By.CSS_SELECTOR, ".ui-search-item__shipping").text
    except:
        envio = ""
    try:
        ubicacion = p.find_element(By.CSS_SELECTOR, ".ui-search-item__location").text
    except:
        ubicacion = ""
    try:
        reputacion = p.find_element(By.CSS_SELECTOR, ".ui-pb-seller__status-info").text
    except:
        reputacion = ""

    data.append([nombre, precio, link, vendidos, envio, ubicacion, reputacion])

# Guardar en CSV
with open("productos_HJ_selenium.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["nombre", "precio", "link", "vendidos", "envio", "ubicacion", "reputacion"])
    writer.writerows(data)

driver.quit()

print(f"✅ Se guardaron {len(data)} productos en productos_HJ_selenium.csv")
