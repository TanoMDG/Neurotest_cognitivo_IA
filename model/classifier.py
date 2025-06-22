from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def entrenar_modelo(df):
    X = df[['Memoria', 'Atención', 'Lenguaje', 'Razonamiento']]
    y = df['riesgo']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    modelo = RandomForestClassifier(random_state=42)
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)
    print("Reporte de clasificación del modelo:")
    print(classification_report(y_test, y_pred))
    return modelo

def predecir_riesgo(modelo, puntajes):
    import pandas as pd
    df_input = pd.DataFrame([puntajes])
    pred = modelo.predict(df_input)[0]
    return pred
