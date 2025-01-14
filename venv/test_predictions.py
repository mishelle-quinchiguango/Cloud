import requests
import json
import grpc
from confluent_kafka import Producer, Consumer
import wine_service_pb2
import wine_service_pb2_grpc

# Configuración
FASTAPI_URL = "http://localhost:8000/predict/"  # Cambia el puerto si es necesario
GRPC_SERVER = "localhost:50051"  # Cambia el puerto si es necesario
KAFKA_BROKER = "localhost:29092"
TOPIC_REQUESTS = "predictions_requests"
TOPIC_RESULTS = "predictions_results"

# Datos de ejemplo
sample_data = {
    "alcohol": 13.16,
    "malic_acid": 3.57,
    "ash": 2.15,
    "alcalinity_of_ash": 21,
    "magnesium": 102,
    "total_phenols": 1.5,
    "flavanoids": 0.55,
    "nonflavanoid_phenols": 0.43,
    "proanthocyanins": 1.3,
    "color_intensity": 4,
    "hue": 0.6,
    "od280_od315": 1.68,
    "proline": 830
}

# Función 1: Predicción usando el API REST (FastAPI)
def predict_rest(data):
    response = requests.get(FASTAPI_URL, params=data)
    if response.status_code == 200:
        print(f"Predicción REST: {response.json()['prediction']}")
    else:
        print(f"Error en predicción REST: {response.status_code}, {response.text}")

# Función 2: Predicción usando gRPC
def predict_grpc(data):
    # Crear un canal y stub de gRPC
    channel = grpc.insecure_channel(GRPC_SERVER)
    stub = wine_service_pb2_grpc.WinePredictionStub(channel)

    # Crear solicitud
    request = wine_service_pb2.WineRequest(
        alcohol=data["alcohol"],
        malic_acid=data["malic_acid"],
        ash=data["ash"],
        alcalinity_of_ash=data["alcalinity_of_ash"],
        magnesium=data["magnesium"],
        total_phenols=data["total_phenols"],
        flavanoids=data["flavanoids"],
        nonflavanoid_phenols=data["nonflavanoid_phenols"],
        proanthocyanins=data["proanthocyanins"],
        color_intensity=data["color_intensity"],
        hue=data["hue"],
        od280_od315=data["od280_od315"],
        proline=data["proline"]
    )

    # Realizar predicción
    response = stub.Predict(request)
    print(f"Predicción gRPC: {response.prediction}")

# Función 3: Predicción usando Kafka
def predict_kafka(data):
    # Configurar productor
    producer = Producer({'bootstrap.servers': KAFKA_BROKER})
    producer.produce(TOPIC_REQUESTS, json.dumps(data).encode('utf-8'))
    producer.flush()
    print("Solicitud enviada a Kafka...")

    # Configurar consumidor
    consumer = Consumer({
        'bootstrap.servers': KAFKA_BROKER,
        'group.id': 'test_group',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([TOPIC_RESULTS])

    print("Esperando resultado de Kafka...")
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Error en Kafka: {msg.error()}")
            break
        result = json.loads(msg.value().decode('utf-8'))
        print(f"Predicción Kafka: {result['prediction']}")
        consumer.close()
        break

# Menú para probar las 3 implementaciones
def main():
    while True:
        print("\nSelecciona el método de predicción:")
        print("1. Predicción usando REST API")
        print("2. Predicción usando gRPC")
        print("3. Predicción usando Kafka")
        print("4. Salir")

        choice = input("Selecciona una opción: ")

        if choice == "1":
            predict_rest(sample_data)
        elif choice == "2":
            predict_grpc(sample_data)
        elif choice == "3":
            predict_kafka(sample_data)
        elif choice == "4":
            print("Saliendo...")
            break
        else:
            print("Opción inválida. Intenta de nuevo.")

if __name__ == "__main__":
    main()
