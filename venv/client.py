import grpc
import wine_service_pb2
import wine_service_pb2_grpc

# Función para probar el servicio
def run():
    # Crear un canal y cliente gRPC
    channel = grpc.insecure_channel('localhost:50051')
    stub = wine_service_pb2_grpc.WinePredictionStub(channel)

    # Crear una solicitud
    request = wine_service_pb2.WineRequest(
        alcohol=13.2,
        malic_acid=2.0,
        ash=2.3,
        alcalinity_of_ash=18.5,
        magnesium=98.0,
        total_phenols=2.8,
        flavanoids=3.0,
        nonflavanoid_phenols=0.26,
        proanthocyanins=1.6,
        color_intensity=5.0,
        hue=1.04,
        od280_od315=3.4,
        proline=1050.0
    )

    # Enviar la solicitud al servidor
    response = stub.Predict(request)
    print(f"Predicción recibida: {response.prediction}")

if __name__ == "__main__":
    run()

