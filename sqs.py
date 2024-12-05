import boto3

sqs = boto3.client('sqs')


def create_sqs_queue():
    response = sqs.create_queue(QueueName='thumbnail-queue')
    print(f"Cola creada: {response['QueueUrl']}")

create_sqs_queue()
