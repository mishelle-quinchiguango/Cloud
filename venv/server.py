import grpc
from concurrent import futures
import time
import joblib
import wine_service_pb2
import wine_service_pb2_grpc

# Cargar el modelo guardado
modelo = joblib.load("wine_classification_model.pkl")

# Implementar el servicio
class WinePredictionService(wine_service_pb2_grpc.WinePredictionServicer):
    def Predict(self, request, context):
        # Convertir los datos de entrada a un formato de lista
        input_data = [[
            request.alcohol, request.malic_acid, request.ash, request.alcalinity_of_ash,
            request.magnesium, request.total_phenols, request.flavanoids,
            request.nonflavanoid_phenols, request.proanthocyanins, request.color_intensity,
            request.hue, request.od280_od315, request.proline
        ]]
        # Realizar predicción con el modelo
        prediction = modelo.predict(input_data)
        return wine_service_pb2.WineResponse(prediction=int(prediction[0]))

# Función para iniciar el servidor
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    wine_service_pb2_grpc.add_WinePredictionServicer_to_server(WinePredictionService(), server)
    server.add_insecure_port('[::]:50051')  # Puerto 50051
    print("Servidor gRPC corriendo en el puerto 50051...")
    server.start()
    try:
        while True:
            time.sleep(86400)  # Mantener el servidor corriendo
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == "__main__":
    serve()

