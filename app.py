import streamlit as st
import plotly.graph_objects as go
import os
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
from utils.html_generator import generar_html_resultado
from utils.visualizacion import graficar_radar
from utils.export_pdf import exportar_pdf
from utils.test_data import test_cognitivo
from utils.sheets import guardar_resultados_test
from utils.interaccion import respuestas_interactivas, clasificar_y_recomendar
from data.generador import leer_datos_reales
from model.classifier import entrenar_modelo, predecir_riesgo
from utils.google_search import buscar_recursos

# === Configuración inicial ===
st.set_page_config(page_title="Test Cognitivo IA", layout="centered")
st.markdown("<h1 style='text-align: center;'>🧠 Test Cognitivo con IA 🤖 Recomendaciones Educativas</h1>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center;'>Completá el siguiente test con las respuestas disponibles, luego presioná <b>Enviar respuestas</b>.</div>", unsafe_allow_html=True)

# === Carga de claves de entorno ===
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

SHEET_URL = os.getenv("SHEET_PUBLIC_URL")
VISUALIZAR_DATOS_PASSWORD1 = os.getenv("VISUALIZAR_DATOS_PASSWORD1")

if not GOOGLE_API_KEY or not SEARCH_ENGINE_ID:
    st.warning("Faltan las claves de Google Search en el archivo .env")

# === Inicialización de estado ===
if "puntajes" not in st.session_state:
    st.session_state.puntajes = {}
if "formulario_enviado" not in st.session_state:
    st.session_state.formulario_enviado = False

# === Formulario con mejoras estéticas ===
with st.form("form_test"):
    st.markdown("""
        <div style='background-color: #f0f8ff; padding: 20px; border-radius: 10px;'>
            <h3 style='text-align: center; color: #1f4e79;'>📏 Datos personales</h3>
    """, unsafe_allow_html=True)

    nombre = st.text_input("Nombre completo")
    edad = st.number_input("Edad", min_value=0, max_value=120, step=1)
    ocupacion = st.text_input("Ocupación")
    nivel_educativo = st.selectbox("Nivel educativo", ["Primaria", "Secundaria", "Terciario", "Universitario", "Posgrado"])
    correo = st.text_input("Correo electrónico")

    st.markdown("</div><hr>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    respuestas = {}
    areas_col1 = ["Memoria", "Atención"]
    areas_col2 = ["Lenguaje", "Razonamiento"]

    def render_areas(col, areas):
        total_puntaje_area = 0
        for area in areas:
            col.markdown(f"""
                <div style='background-color: #f9f9f9; padding: 10px; border-radius: 8px; margin-bottom: 15px;'>
                    <h4 style='color: #2c3e50;'>{area}</h4>
            """, unsafe_allow_html=True)
            preguntas = test_cognitivo[area]
            for i, pregunta in enumerate(preguntas):
                opciones = pregunta["opciones"]
                mapa_opciones = {f"{k}) {v[0]}": k for k, v in opciones.items()}
                seleccion_etiqueta = col.radio(
                    f"{pregunta['pregunta']}",
                    options=list(mapa_opciones.keys()),
                    key=f"{area}_{i}"
                )
                seleccion = mapa_opciones[seleccion_etiqueta]
                total_puntaje_area += opciones[seleccion][1]
            respuestas[area] = total_puntaje_area
            col.markdown("</div>", unsafe_allow_html=True)

    render_areas(col1, areas_col1)
    render_areas(col2, areas_col2)

    enviado = st.form_submit_button("Enviar respuestas")

# === Procesamiento y persistencia ===
if enviado:
    st.session_state.formulario_enviado = True
    st.session_state.puntajes = respuestas
    st.session_state.datos_personales = {
        "nombre": nombre,
        "edad": edad,
        "ocupacion": ocupacion,
        "nivel_educativo": nivel_educativo,
        "correo": correo
    }

# === Mostrar resultados si se envió el formulario ===
if st.session_state.formulario_enviado:
    respuestas = st.session_state.puntajes
    datos_personales = st.session_state.datos_personales

    st.subheader("📊 Resultados por Área")
    for area, pt in respuestas.items():
        st.markdown(f"<div style='margin-bottom: 10px;'><strong>{area.capitalize()}</strong>: {pt} puntos</div>", unsafe_allow_html=True)

    st.plotly_chart(graficar_radar(respuestas))

    recomendaciones = clasificar_y_recomendar(respuestas)
    st.subheader("✅ Clasificación y Recomendaciones")
    for area, (nivel, reco) in recomendaciones.items():
        st.markdown(f"- **{area.capitalize()}**: {nivel} — {reco}")

    st.info("Entrenando modelo para predecir riesgo general...")
    df_sintetico = leer_datos_reales()
    modelo = entrenar_modelo(df_sintetico)
    riesgo_predicho = predecir_riesgo(modelo, respuestas)
    st.success(f"🔍 Riesgo general predicho: **{riesgo_predicho}**")

    st.subheader("🔗 Recursos Educativos Recomendados")
    recursos = buscar_recursos(f"recursos educativos para {riesgo_predicho}")
    if recursos:
        for recurso in recursos:
            st.markdown(f"**{recurso['titulo']}**  <br>{recurso['descripcion']}  <br>[Ver recurso]({recurso['link']})", unsafe_allow_html=True)
    else:
        st.warning("No se encontraron recursos para esta búsqueda.")

    opciones_estrellas = [
        "⭐☆☆☆☆ (1)",
        "⭐⭐☆☆☆ (2)",
        "⭐⭐⭐☆☆ (3)",
        "⭐⭐⭐⭐☆ (4)",
        "⭐⭐⭐⭐⭐ (5)"
    ]

    utilidad = st.radio(
        "¿Cómo calificarías esta evaluación?",
        opciones_estrellas,
        index=None,
        key="utilidad"
    )

    if utilidad:
        st.session_state['utilidad_seleccionada'] = utilidad
        resultado_html = generar_html_resultado(respuestas, recomendaciones, riesgo_predicho, utilidad, recursos, datos_personales)
        pdf_generado = exportar_pdf(resultado_html)

        if pdf_generado:
            with open("reporte.pdf", "rb") as f:
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.download_button("📄 Descargar reporte en PDF", f, file_name="reporte.pdf"):
                        guardar_resultados_test("Datos_Cognitivos", respuestas, utilidad, datos_personales)
                        st.session_state.pdf_descargado = True

            if st.session_state.get("pdf_descargado", False):
                st.markdown("---")
                st.header("🔒 Visualizar Datos")

                if not st.session_state.get("clave_valida", False):
                    with st.form("form_visualizar_datos"):
                        clave_ingresada = st.text_input("Ingresá la clave para visualizar los datos:", type="password", key="clave_visualizar_datos")
                        enviar = st.form_submit_button("Visualizar Datos")

                        if enviar:
                            if clave_ingresada.strip() == VISUALIZAR_DATOS_PASSWORD1.strip():
                                st.session_state["clave_valida"] = True
                                st.success("✅ Clave correcta. Abrí la hoja de cálculo en una nueva pestaña 👇")
                                st.markdown(f"[Abrir Hoja de Datos]({SHEET_URL})", unsafe_allow_html=True)
                            else:
                                st.error("❌ Clave incorrecta. Intentalo de nuevo.")
                else:
                    st.success("✅ Clave ya validada. Abrí la hoja de cálculo en una nueva pestaña 👇")
                    st.markdown(f"[Abrir Hoja de Datos]({SHEET_URL})", unsafe_allow_html=True)





