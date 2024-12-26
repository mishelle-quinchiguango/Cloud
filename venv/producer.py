from confluent_kafka import Producer
import json

# Configuración del productor
conf = {
    'bootstrap.servers': 'localhost:29092'  # Puerto donde Kafka está escuchando
}

# Crear el productor
producer = Producer(conf)

# Datos a enviar
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

# Enviar el mensaje
producer.produce('wine-predictions', key="key1", value=json.dumps(data))
producer.flush()
print("Mensaje enviado al tópico 'wine-predictions'")
