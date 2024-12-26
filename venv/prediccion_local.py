import joblib

def prediccion_local(data):
    # Cargar el modelo guardado
    modelo = joblib.load('wine_classification_model.pkl')

    # Formatear los datos para la predicción
    input_data = [[
        data['alcohol'], data['malic_acid'], data['ash'], data['alcalinity_of_ash'],
        data['magnesium'], data['total_phenols'], data['flavanoids'],
        data['nonflavanoid_phenols'], data['proanthocyanins'], data['color_intensity'],
        data['hue'], data['od280_od315'], data['proline']
    ]]

    # Realizar la predicción
    prediction = modelo.predict(input_data)
    return prediction[0]
