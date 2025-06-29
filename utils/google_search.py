# google_search.py

import os
import requests
from dotenv import load_dotenv
# Cargar variables del archivo .env
load_dotenv()

# Leer las claves de entorno
API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")


def buscar_recursos(consulta, num_resultados=5):
    """Realiza una búsqueda en Google y devuelve una lista de recursos educativos."""
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "q": consulta,
        "num": num_resultados
    }

    respuesta = requests.get(url, params=params)
    resultados = []

    if respuesta.status_code == 200:
        datos = respuesta.json()
        for item in datos.get("items", []):
            resultados.append({
                "titulo": item["title"],
                "link": item["link"],
                "descripcion": item.get("snippet", "")
            })
    else:
        print("Error en la búsqueda:", respuesta.text)
    
    return resultados
