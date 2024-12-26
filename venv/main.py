from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import uvicorn

# 1. Crear la aplicación FastAPI
app = FastAPI()

# 2. Cargar el modelo guardado
modelo = joblib.load("wine_classification_model.pkl")

# 3. Definir la estructura de los datos de entrada
class WineFeatures(BaseModel):
    alcohol: float
    malic_acid: float
    ash: float
    alcalinity_of_ash: float
    magnesium: float
    total_phenols: float
    flavanoids: float
    nonflavanoid_phenols: float
    proanthocyanins: float
    color_intensity: float
    hue: float
    od280_od315: float
    proline: float

# 4. Definir el endpoint GET para predicciones
@app.get("/predict/")
def predict(
    alcohol: float,
    malic_acid: float,
    ash: float,
    alcalinity_of_ash: float,
    magnesium: float,
    total_phenols: float,
    flavanoids: float,
    nonflavanoid_phenols: float,
    proanthocyanins: float,
    color_intensity: float,
    hue: float,
    od280_od315: float,
    proline: float
):
    # Convertir las características en una lista para el modelo
    input_data = [[
        alcohol, malic_acid, ash, alcalinity_of_ash,
        magnesium, total_phenols, flavanoids,
        nonflavanoid_phenols, proanthocyanins, color_intensity,
        hue, od280_od315, proline
    ]]
    
    # Realizar la predicción
    prediction = modelo.predict(input_data)
    return {"prediction": int(prediction[0])}
