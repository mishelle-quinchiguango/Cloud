import json
import boto3
from PIL import Image
import io


s3 = boto3.client('s3')
dynamodb = boto3.client('dynamodb')

thumbnails_bucket = 'thumbnails-bucket'
table_name = 'images-metadata-table'

def lambda_handler(event, context):
    # Procesar los registros de la cola SQS
    for record in event['Records']:
        
        s3_bucket = record['s3']['bucket']['name']
        s3_key = record['s3']['object']['key']
        
        image_object = s3.get_object(Bucket=s3_bucket, Key=s3_key)
        image_data = image_object['Body'].read()

        image = Image.open(io.BytesIO(image_data))
        image.thumbnail((128, 128))  
        
        thumbnail_key = f'thumbnails/{s3_key}'
        buffer = io.BytesIO()
        image.save(buffer, 'JPEG')
        buffer.seek(0)
        
        s3.put_object(Bucket=thumbnails_bucket, Key=thumbnail_key, Body=buffer)
        
        # Guardar los metadatos en DynamoDB
        image_size = len(image_data)
        dynamodb.put_item(
            TableName=table_name,
            Item={
                'image_id': {'S': s3_key},
                'image_url': {'S': f'https://{s3_bucket}.s3.amazonaws.com/{s3_key}'},
                'thumbnail_url': {'S': f'https://{thumbnails_bucket}.s3.amazonaws.com/{thumbnail_key}'},
                'size': {'N': str(image_size)}
            }
        )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Thumbnail generado y metadatos guardados.')
    }
