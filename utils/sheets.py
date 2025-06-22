# utils/sheets.py
import os
import gspread
from google.oauth2.service_account import Credentials
import datetime

def conectar_google_sheets(credenciales_path, nombre_hoja):
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    try:
        creds = Credentials.from_service_account_file(credenciales_path, scopes=scopes)
        cliente = gspread.authorize(creds)
        return cliente.open(nombre_hoja).sheet1
    except Exception as e:
        print(f"Error al conectar con Google Sheets: {e}")
        raise

def escribir_en_hoja(hoja, fila):
    hoja.append_row(fila)

def guardar_resultados_test(nombre_hoja, respuestas, utilidad, datos_personales):
    credenciales_path = os.getenv("GOOGLE_SHEETS_CREDENTIALS_PATH", "credenciales.json")
    hoja = conectar_google_sheets(credenciales_path, nombre_hoja)
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    fila = [
        fecha,
        datos_personales.get("nombre", ""),
        datos_personales.get("edad", ""),
        datos_personales.get("ocupacion", ""),
        datos_personales.get("nivel_educativo", ""),
        datos_personales.get("correo", "")
        #datos_personales.get("resena", "")#
    ] + [respuestas.get(area, 0) for area in ["Memoria", "Atención", "Lenguaje", "Razonamiento"]] + [utilidad]

    escribir_en_hoja(hoja, fila)


