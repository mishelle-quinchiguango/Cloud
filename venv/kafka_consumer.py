from confluent_kafka import Consumer
import json

# Configurar consumidor
consumer = Consumer({
    'bootstrap.servers': 'localhost:29092',
    'group.id': 'result_group',
    'auto.offset.reset': 'earliest'
})

consumer.subscribe(['predictions_results'])

print("Esperando resultados...")

while True:
    msg = consumer.poll(1.0)  # Esperar mensaje durante 1 segundo
    if msg is None:
        continue
    if msg.error():
        print("Error al consumir mensaje:", msg.error())
        continue

    # Leer mensaje recibido
    result = json.loads(msg.value().decode('utf-8'))
    print("Resultado recibido:", result)
