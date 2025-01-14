from kafka import KafkaConsumer, KafkaProducer
import joblib
import json

# Cargar el modelo guardado
modelo = joblib.load("wine_classification_model.pkl")

# Configuración de Kafka
KAFKA_BROKER = 'localhost:9092'  # Dirección del broker Kafka
TOPIC_REQUESTS = 'predictions_requests'  # Topic de entrada
TOPIC_RESULTS = 'predictions_results'  # Topic de salida

# Inicializar productor y consumidor
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serializar mensajes a JSON
)

consumer = KafkaConsumer(
    TOPIC_REQUESTS,
    bootstrap_servers=KAFKA_BROKER,
    auto_offset_reset='earliest',
    group_id='prediction_group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))  # Deserializar mensajes de JSON
)

print("Servicio de predicciones iniciado. Esperando solicitudes...")

# Procesar mensajes de Kafka
for message in consumer:
    try:
        # Leer datos del mensaje
        data = message.value
        print("Solicitud recibida:", data)
        
        # Extraer características
        input_data = [[
            data['alcohol'], data['malic_acid'], data['ash'], data['alcalinity_of_ash'],
            data['magnesium'], data['total_phenols'], data['flavanoids'],
            data['nonflavanoid_phenols'], data['proanthocyanins'], data['color_intensity'],
            data['hue'], data['od280_od315'], data['proline']
        ]]
        
        # Realizar predicción
        prediction = modelo.predict(input_data)[0]
        print("Predicción realizada:", prediction)
        
        # Enviar resultado al topic de salida
        result = {"prediction": int(prediction), "input": data}
        producer.send(TOPIC_RESULTS, value=result)
        print("Resultado enviado al topic:", TOPIC_RESULTS)
    
    except Exception as e:
        print("Error procesando el mensaje:", e)
