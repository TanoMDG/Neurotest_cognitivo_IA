# utils/visualizacion.py
import plotly.graph_objects as go

def graficar_radar(respuestas):
    categorias = list(respuestas.keys())
    valores = list(respuestas.values())
    valores.append(valores[0])
    categorias.append(categorias[0])

    fig = go.Figure(
        data=[
            go.Scatterpolar(
                r=valores,
                theta=categorias,
                fill='toself',
                name='Puntaje por área',
                line=dict(color='#1f77b4', width=3),
                marker=dict(symbol='circle', size=8)
            )
        ],
        layout=go.Layout(
            polar=dict(
                bgcolor="#fafafa",
                radialaxis=dict(visible=True, range=[0, 25], showline=True, linewidth=1, gridcolor="lightgrey")
            ),
            showlegend=False,
            margin=dict(t=20, b=20)
        )
    )
    return fig