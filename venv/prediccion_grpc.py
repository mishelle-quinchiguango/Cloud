import grpc
import wine_service_pb2
import wine_service_pb2_grpc

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
