from confluent_kafka import Consumer, KafkaException

# Configuración del consumidor
conf = {
    'bootstrap.servers': 'localhost:29092',  # Puerto donde Kafka está escuchando
    'group.id': 'wine-consumer-group',
    'auto.offset.reset': 'earliest'  # Leer desde el inicio
}

# Crear el consumidor
consumer = Consumer(conf)
consumer.subscribe(['wine-predictions'])  # Tópico a escuchar

print("Esperando mensajes del tópico 'wine-predictions'...")

try:
    while True:
        msg = consumer.poll(timeout=10.0)
        if msg is None:  # No hay mensajes nuevos
            print("No se recibieron mensajes.")
            continue
        if msg.error():
            print(f"Error en el mensaje: {msg.error()}")
            continue

        # Imprimir el mensaje recibido
        print(f"Mensaje recibido: {msg.value().decode('utf-8')}")
        consumer.close()
        return json.loads(msg.value())

except KeyboardInterrupt:
    print("Consumo interrumpido por el usuario")

finally:
    # Cerrar el consumidor
    consumer.close()
