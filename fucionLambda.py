import boto3
import os
from PIL import Image
from io import BytesIO

s3 = boto3.client('s3')
dynamodb = boto3.client('dynamodb')
TABLE_NAME = "MetadatosImagenes"
THUMBNAIL_BUCKET = "imagenes-thumbnails-ejercicio"

def lambda_handler(event, context):
    
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']
    
   
    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    image_data = response['Body'].read()
    
    # Abrir la imagen con PIL y generar un thumbnail
    image = Image.open(BytesIO(image_data))
    image.thumbnail((100, 100)) 
    
  
    thumbnail_key = f"thumbnails/{object_key}"
    buffer = BytesIO()
    image.save(buffer, format='JPEG')
    buffer.seek(0)
    s3.put_object(Bucket=THUMBNAIL_BUCKET, Key=thumbnail_key, Body=buffer, ContentType='image/jpeg')
    
    # Guardar metadatos en DynamoDB
    metadata = {
        'NombreArchivo': {'S': object_key},
        'URL': {'S': f"https://{THUMBNAIL_BUCKET}.s3.amazonaws.com/{thumbnail_key}"},
        'Tamano': {'N': str(len(buffer.getvalue()))} 
    }
    dynamodb.put_item(TableName=TABLE_NAME, Item=metadata)
    
    return {
        'statusCode': 200,
        'body': 'Thumbnail generado y metadatos almacenados correctamente.'
    }
