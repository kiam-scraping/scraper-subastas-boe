import requests
from bs4 import BeautifulSoup
import random
from urllib.parse import urljoin
import csv  

USER_AGENTS = [
    # Chrome
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    
    # Firefox
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12.6; rv:110.0) Gecko/20100101 Firefox/110.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0",
    
    # Edge
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.0.0",
    
    # Safari (MacOS y iOS)
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_3) AppleWebKit/537.36 (KHTML, like Gecko) Version/16.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/537.36",
    
    # Android
    "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36"
]

def get_random_header():
    return {"User-Agent": random.choice(USER_AGENTS)}

url = "https://subastas.boe.es/subastas_ava.php?accion=Mas&id_busqueda=c2o1TU5OTzhlaFRsT1hSYSs0bW41UnNWVHpkL1RYaXZ3QUR0ek5PdGZUanFtS3drRDNpOEtjNFIwV3l1YzVGUHVyRlJoOVNlVzJPNXVGTjY1V1Zmd1FvZ0UxbXZVckxaWk1Vb1ljNjI4MFd2RVQ3STJ5Y3ZHdkdKVGl0MkRkT0tLQ3B5SkZWLysxTzZLbEUzckUzTUZaRUpUOFJBRUJlSTRzRDdQZUo5Skg0djZHVEdUTTlGQnhSYTEvWm9PSjQ2MGJydCt0ajJpOUViOWxCTVF2bS9uYjFEMlBlMjZLRWFGWG4rMC9Oc2dVbTdqMW9mUVJPeldOZXpxVDh5blZRYXZZdEtCSEwveElDd0pRR3VyUVVBeTUySzcyc2t1cjdoYTdqSngyR1FyVnZVUWlaZlhHUE85NTY3Y01rdWc3NmoxZXFISjZlZ0h3RWh3ZVRTd1locnZBPT0,-0-50-0-50"
peticion = requests.get(url, headers=get_random_header())
soup = BeautifulSoup(peticion.text, "html.parser")
listado_enlaces_subastas = set()

# 🔹 Scraping de enlaces de subastas
while True:
    enlace_subastas = soup.find_all("a", class_="resultado-busqueda-link-defecto")
    
    for enlace in enlace_subastas:
        url_absoluta_subasta = urljoin(url, enlace["href"])
        listado_enlaces_subastas.add(url_absoluta_subasta)
    
    boton_siguiente = soup.select_one(".paginar2 li:last-child a")
    
    if boton_siguiente and boton_siguiente.find("abbr", {"title": "Página"}):
        url = urljoin(url, boton_siguiente["href"])
        peticion = requests.get(url, headers=get_random_header())
        soup = BeautifulSoup(peticion.text, "html.parser")
    else:
        break

print(f"Subastas totales encontradas: {len(listado_enlaces_subastas)}")

contador = 0
archivo_csv = "13. subastas_basico.csv"

# 🔹 Abrimos el archivo CSV antes de empezar el scraping
with open(archivo_csv, mode="w", newline="", encoding="utf-8") as archivo:
    escritor = None  # 🔹 Se define aquí para configurarlo después
    columnas = set()  # 🔹 NUEVO: Conjunto para almacenar todas las columnas dinámicamente

    for i in listado_enlaces_subastas:
        peticion = requests.get(i, headers=get_random_header())
        soup = BeautifulSoup(peticion.text, "html.parser")
        contador += 1
        tabla = soup.find("table")
        datos_subasta = {}

        for tr in tabla.find_all("tr"):
            th = tr.find("th")
            td = tr.find("td")
            if th and td:
                datos_subasta[th.text.strip()] = td.text.strip()  

        # 🔹 Actualizar columnas dinámicamente
        nuevas_columnas = list(datos_subasta.keys())
        if not columnas.issuperset(nuevas_columnas):  # Si hay nuevas columnas...
            columnas.update(nuevas_columnas)  # Agregar nuevas columnas

            # 🔹 Reescribir el archivo con las nuevas columnas
            archivo.seek(0)  # Volver al inicio del archivo para sobrescribir
            escritor = csv.DictWriter(archivo, fieldnames=sorted(columnas))
            archivo.truncate()  # Borrar contenido anterior
            escritor.writeheader()  # Escribir nueva cabecera

            # 🔹 Volver a escribir subastas anteriores (si existen)
            subastas_lista = []  # 🔹 NUEVO: Lista para almacenar subastas previamente scrapeadas

            for subasta in subastas_lista:
                escritor.writerow(subasta)

        escritor.writerow(datos_subasta)  # 🔹 Escribir la subasta en el CSV

        print(f"Subasta {contador}/{len(listado_enlaces_subastas)} guardada en CSV.")

print(f"Subastas guardadas en {archivo_csv}")  # Mensaje final
