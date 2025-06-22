from pathlib import Path
import pandas as pd

def leer_datos_reales():
    """
    Lee un archivo CSV con datos reales y devuelve un DataFrame
    con las columnas necesarias para entrenamiento del modelo.
    """
    ruta_csv = Path(__file__).parent / "datos_reales.csv"
    df = pd.read_csv(ruta_csv)

    # Seleccionar columnas clave
    columnas = ["Memoria", "Atención", "Lenguaje", "Razonamiento", "riesgo"]
    data = df[columnas]

    return pd.DataFrame(data, columns=columnas)





"""
import pandas as pd

def leer_datos_reales(csv_path="datos_reales.csv"):
    
    #Lee un archivo CSV con datos reales y devuelve un DataFrame
    #con las columnas necesarias para entrenamiento del modelo.
    
    df = pd.read_csv(csv_path)

    # Seleccionar columnas clave
    data = df[["Memoria", "Atención", "Lenguaje", "Razonamiento", "riesgo"]]

    return pd.DataFrame(data, columns=["Memoria", "Atención", "Lenguaje", "Razonamiento", "riesgo"])

"""
