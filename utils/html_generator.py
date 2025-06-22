import re

def estrellas_html(calificacion):
    try:
        # Extrae el número entre paréntesis, por ejemplo: (3)
        match = re.search(r"\((\d+)\)", calificacion)
        cantidad = int(match.group(1)) if match else 0
    except:
        cantidad = 0

    estrella_img = '<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Plain_Yellow_Star.png/16px-Plain_Yellow_Star.png" width="18" style="margin-right:2px;" />'
    return estrella_img * cantidad




def generar_html_resultado(respuestas, recomendaciones, riesgo_predicho, utilidad, recursos, datos_personales):
    resultado_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <style>
        body {{ font-family: Arial, sans-serif; padding: 20px; }}
        h2 {{ color: #2E86C1; }}
        h3 {{ color: #117A65; margin-top: 30px; }}
        p, li {{ font-size: 14px; line-height: 1.6; }}
        a {{ color: #1A5276; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
      </style>
    </head>
    <body>
      <h2>🧠 Resultados del Test Cognitivo</h2>

      <h3>📄 Información Personal</h3>
      <ul>
        <li><b>Nombre:</b> {datos_personales.get('nombre', '')}</li>
        <li><b>Edad:</b> {datos_personales.get('edad', '')}</li>
        <li><b>Nivel educativo:</b> {datos_personales.get('nivel_educativo', '')}</li>
        <li><b>Ocupación:</b> {datos_personales.get('ocupacion', '')}</li>
        <li><b>Correo electrónico:</b> {datos_personales.get('correo', '')}</li>
        <!-- <li><b>Reseña/opinión:</b> {datos_personales.get('resena', '')}</li> -->
      </ul>

      <h3>📊 Resultados por Área</h3>
    """

    for area, pt in respuestas.items():
        resultado_html += f"<p><b>{area}:</b> {pt} puntos</p>"

    resultado_html += "<h3>✅ Clasificación y Recomendaciones</h3>"
    for area, (nivel, reco) in recomendaciones.items():
        resultado_html += f"<p><b>{area}:</b> {nivel} — {reco}</p>"

    resultado_html += f"""
      <h3>🔍 Riesgo General</h3>
      <p><b>{riesgo_predicho}</b></p>

      <h3>🔗 Recursos Educativos Recomendados</h3>
    """

    if recursos:
        resultado_html += "<ul>"
        for recurso in recursos:
            resultado_html += f"""
            <li>
              <b>{recurso['titulo']}</b><br>
              {recurso['descripcion']}<br>
              <a href="{recurso['link']}">{recurso['link']}</a>
            </li><br>
            """
        resultado_html += "</ul>"
    else:
        resultado_html += "<p>No se encontraron recursos recomendados.</p>"

    resultado_html += "<h3>¿Cómo calificarías esta evaluación?</h3>"
    resultado_html += f"<p>{estrellas_html(utilidad)}</p>"
    resultado_html += "</body></html>"

    resultado_html += """
    </body>
    </html>
    """

    return resultado_html

