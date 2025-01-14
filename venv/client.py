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
        alcohol=13.16, malic_acid=3.57, ash=2.15,
    alcalinity_of_ash=21, magnesium=102,
    total_phenols=1.5, flavanoids=0.55,
    nonflavanoid_phenols=0.43, proanthocyanins=1.3,
    color_intensity=4, hue=0.6,
    od280_od315=1.68, proline=830
    )

    # Enviar la solicitud al servidor
    response = stub.Predict(request)
    print(f"Predicción recibida: {response.prediction}")

if __name__ == "__main__":
    run()

