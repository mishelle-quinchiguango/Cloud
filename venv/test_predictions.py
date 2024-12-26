# Asegúrate de incluir todas las funciones que hemos creado antes:
from confluent_kafka import Producer, Consumer
import json
import grpc
import wine_service_pb2
import wine_service_pb2_grpc
import joblib

# 1. Predicción con gRPC
def prediccion_grpc(data):
    # Crear canal y stub gRPC
    channel = grpc.insecure_channel('localhost:50051')  # Asegúrate de que el servidor gRPC está corriendo
    stub = wine_service_pb2_grpc.WinePredictionStub(channel)

    # Crear la solicitud gRPC
    request = wine_service_pb2.WineRequest(
        alcohol=data['alcohol'],
        malic_acid=data['malic_acid'],
        ash=data['ash'],
        alcalinity_of_ash=data['alcalinity_of_ash'],
        magnesium=data['magnesium'],
        total_phenols=data['total_phenols'],
        flavanoids=data['flavanoids'],
        nonflavanoid_phenols=data['nonflavanoid_phenols'],
        proanthocyanins=data['proanthocyanins'],
        color_intensity=data['color_intensity'],
        hue=data['hue'],
        od280_od315=data['od280_od315'],
        proline=data['proline']
    )

    # Realizar la predicción
    response = stub.Predict(request)
    return response.prediction

# 2. Predicción con Kafka
def prediccion_kafka(data):
    # Configurar el productor
    producer = Producer({'bootstrap.servers': 'localhost:29092'})

    # Enviar el mensaje al tópico
    producer.produce('wine-predictions', key="key1", value=json.dumps(data))
    producer.flush()
    print("Mensaje enviado a Kafka.")

    # Configurar el consumidor
    consumer = Consumer({
        'bootstrap.servers': 'localhost:29092',
        'group.id': 'wine-consumer-group',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe(['wine-predictions'])

    # Leer el mensaje del tópico
    while True:
        msg = consumer.poll(timeout=10.0)
        if msg is None:
            print("No se recibieron mensajes.")
            continue
        if msg.error():
            print(f"Error en el mensaje: {msg.error()}")
            break

        # Mostrar el mensaje recibido
        print(f"Mensaje recibido: {msg.value().decode('utf-8')}")
        consumer.close()
        return json.loads(msg.value())

# 3. Predicción local directa
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

# Programa de prueba
def main():
    # Datos de entrada para las predicciones
    data = {
        "alcohol": 14.0,
        "malic_acid": 1.8,
        "ash": 2.5,
        "alcalinity_of_ash": 20.0,
        "magnesium": 110.0,
        "total_phenols": 2.5,
        "flavanoids": 2.9,
        "nonflavanoid_phenols": 0.3,
        "proanthocyanins": 1.5,
        "color_intensity": 5.5,
        "hue": 1.02,
        "od280_od315": 3.0,
        "proline": 1200.0
    }

    print("Predicciones:")
    print("-------------------------------")

    # 1. Predicción con gRPC
    print("1. Predicción con gRPC:")
    pred_grpc = prediccion_grpc(data)
    print(f"Predicción gRPC: {pred_grpc}")

    # 2. Predicción con Kafka
    print("\n2. Predicción con Kafka:")
    pred_kafka = prediccion_kafka(data)
    print(f"Predicción Kafka: {pred_kafka}")

    # 3. Predicción local
    print("\n3. Predicción local:")
    pred_local = prediccion_local(data)
    print(f"Predicción local: {pred_local}")

if __name__ == "__main__":
    main()
