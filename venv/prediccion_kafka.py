from confluent_kafka import Producer, Consumer, KafkaException
import json

def prediccion_kafka(data):
    # Configurar el productor
    producer = Producer({'bootstrap.servers': 'localhost:29092'})

    # Enviar el mensaje al tópico
    producer.produce('wine-predictions', key="key1", value=json.dumps(data))
    producer.flush()
    print("Mensaje enviado a Kafka.")

    # Configurar el consumidor
    consumer = Consumer({
        'bootstrap.servers': 'localhost:29092',
        'group.id': 'wine-consumer-group',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe(['wine-predictions'])

    # Leer el mensaje del tópico
    while True:
        msg = consumer.poll(timeout=10.0)
        if msg is None:
            print("No se recibieron mensajes.")
            continue
        if msg.error():
            if msg.error().code() == KafkaException._PARTITION_EOF:
                continue
            else:
                print(f"Error en el mensaje: {msg.error()}")
                break

        # Mostrar el mensaje recibido
        print(f"Mensaje recibido: {msg.value().decode('utf-8')}")
        consumer.close()
        return json.loads(msg.value())
