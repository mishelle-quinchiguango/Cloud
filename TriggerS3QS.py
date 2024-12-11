import boto3

# Crear el cliente de S3 y SQS
s3 = boto3.client('s3')
sqs = boto3.client('sqs')


def configure_s3_notification():
    bucket_name = 'images-bucket'    

    notification_configuration = {
        'QueueConfigurations': [
            {
                'QueueUrl': https://sqs.us-east-1.amazonaws.com/758159251915/imagen-cargada-queue,
                'Event': 's3:ObjectCreated:*',
                'Filter': {'Key': {'FilterRules': [{'Name': 'suffix', 'Value': '.jpg'}]}}  
            }
        ]
    }

    s3.put_bucket_notification_configuration(
        Bucket=bucket_name,
        NotificationConfiguration=notification_configuration
    )
    print(f"Notificación configurada para el bucket {bucket_name}.")

configure_s3_notification()
