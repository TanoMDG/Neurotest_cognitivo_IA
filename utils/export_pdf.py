import os
import pdfkit
import streamlit as st


def exportar_pdf(desde_html: str, salida_pdf: str = "reporte.pdf") -> bool:
    """
    Exporta un archivo HTML a PDF utilizando wkhtmltopdf.
    - desde_html: contenido HTML como string
    - salida_pdf: nombre del archivo de salida
    - Devuelve True si fue exitoso, False si hubo error
    """

    wkhtmltopdf_path = os.getenv("WKHTMLTOPDF_PATH") or r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"

    if not os.path.isfile(wkhtmltopdf_path):
        st.error(f"No se encontró wkhtmltopdf en la ruta especificada: {wkhtmltopdf_path}")
        return False

    try:
        config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

        # Guardar HTML temporal
        with open("temp_reporte.html", "w", encoding="utf-8") as f:
            f.write(desde_html)

        # Generar PDF
        pdfkit.from_file("temp_reporte.html", salida_pdf, configuration=config)
        return True

    except Exception as e:
        st.error(f"Error al generar el PDF: {e}")
        return False