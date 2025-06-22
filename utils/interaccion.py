def respuestas_interactivas(test):
    puntajes = {"memoria": 0, "atencion": 0, "lenguaje": 0, "razonamiento": 0}
    mapeo = {"Memoria": "Memoria", "Atención": "Atención", "Lenguaje": "Lenguaje", "Razonamiento": "Razonamiento"}

    for categoria, preguntas in test.items():
        print(f"\nCategoría: {categoria}\n")
        for i, pregunta in enumerate(preguntas, 1):
            print(f"{i}. {pregunta['pregunta']}")
            for key, (texto, _) in pregunta["opciones"].items():
                print(f"   {key}) {texto}")

            while True:
                opcion = input("Tu respuesta (a, b, c, d): ").lower()
                if opcion in pregunta["opciones"]:
                    break
                else:
                    print("Opción inválida, ingresa a, b, c o d.")

            puntaje = pregunta["opciones"][opcion][1]
            puntajes[mapeo[categoria]] += puntaje
    return puntajes

def clasificar_y_recomendar(puntajes):
    recomendaciones = {
        "Memoria": "Practicar ejercicios de memoria como juegos de recordar objetos o secuencias.",
        "Atención": "Realizar actividades que mejoren la concentración, como rompecabezas o mindfulness.",
        "Lenguaje": "Ejercitar el vocabulario y comprensión lectora con lectura diaria y juegos de palabras.",
        "Razonamiento": "Resolver problemas lógicos y matemáticos para fortalecer el razonamiento.",
    }
    niveles = {}
    for area, puntaje in puntajes.items():
        if puntaje < 6:
            niveles[area] = ("Alto riesgo", recomendaciones[area])
        elif puntaje < 9:
            niveles[area] = ("Moderado riesgo", recomendaciones[area])
        elif puntaje < 12:
            niveles[area] = ("Leve riesgo", recomendaciones[area])
        else:
            niveles[area] = ("Sin riesgo", "Excelente desempeño en esta área.")
    return niveles
