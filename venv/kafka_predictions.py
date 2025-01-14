from confluent_kafka import Consumer, Producer
import joblib
import json

# Cargar el modelo
modelo = joblib.load("wine_classification_model.pkl")

# Configuración de Kafka
KAFKA_BROKER = 'localhost:29092'
TOPIC_REQUESTS = 'predictions_requests'
TOPIC_RESULTS = 'predictions_results'

# Configurar productor
producer = Producer({'bootstrap.servers': KAFKA_BROKER})

# Configurar consumidor
consumer = Consumer({
    'bootstrap.servers': KAFKA_BROKER,
    'group.id': 'prediction_group',
    'auto.offset.reset': 'earliest'
})
consumer.subscribe([TOPIC_REQUESTS])

print("Servicio de predicciones iniciado...")

while True:
    msg = consumer.poll(1.0)  # Esperar mensaje durante 1 segundo
    if msg is None:
        continue
    if msg.error():
        print("Error al consumir mensaje:", msg.error())
        continue

    try:
        # Leer datos del mensaje
        data = json.loads(msg.value().decode('utf-8'))
        print("Solicitud recibida:", data)

        # Predecir
        input_data = [[
            data['alcohol'], data['malic_acid'], data['ash'], data['alcalinity_of_ash'],
            data['magnesium'], data['total_phenols'], data['flavanoids'],
            data['nonflavanoid_phenols'], data['proanthocyanins'], data['color_intensity'],
            data['hue'], data['od280_od315'], data['proline']
        ]]
        prediction = modelo.predict(input_data)[0]
        print("Predicción:", prediction)

        # Enviar respuesta
        result = {"prediction": int(prediction), "input": data}
        producer.produce(TOPIC_RESULTS, json.dumps(result).encode('utf-8'))
        producer.flush()
        print("Resultado enviado al topic:", TOPIC_RESULTS)
    except Exception as e:
        print("Error procesando mensaje:", e)
