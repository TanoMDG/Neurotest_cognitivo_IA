import requests

# Configura tu API Key y el ID del motor de búsqueda
API_KEY = "AIzaSyBOKid7RklODTET2D0jo-Nvy2KZoSb_3o4"
SEARCH_ENGINE_ID = "c7b6f8a5119744d7b"

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
