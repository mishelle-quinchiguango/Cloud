import boto3

# Crear un cliente de SQS
sqs = boto3.client('sqs')

QUEUE_NAME = 'imagen-cargada-queue'

def crear_cola_sqs():
    try:
        # Crear la cola de SQS
        response = sqs.create_queue(
            QueueName=QUEUE_NAME,
            Attributes={
                'DelaySeconds': '0',
                'MessageRetentionPeriod': '345600',  
            }
        )
        print(f"Cola '{QUEUE_NAME}' creada exitosamente.")
        print(f"URL de la cola: {response['QueueUrl']}")
        return response['QueueUrl']
    except Exception as e:
        print(f"Error al crear la cola de SQS: {e}")

if __name__ == "__main__":
    crear_cola_sqs()
