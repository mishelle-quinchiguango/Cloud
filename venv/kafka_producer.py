from confluent_kafka import Producer
import json

# Configurar productor
producer = Producer({'bootstrap.servers': 'localhost:29092'})

# Solicitud de ejemplo
data = {
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

# Enviar solicitud al topic de entrada
producer.produce('predictions_requests', json.dumps(data).encode('utf-8'))
producer.flush()
print("Solicitud enviada:", data)
