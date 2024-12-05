import boto3
from botocore.exceptions import NoCredentialsError



# Crear un cliente de S3 con la sesión personalizada
s3 = session.client('s3')

try:
    s3.create_bucket(Bucket='images-bucket', CreateBucketConfiguration={'LocationConstraint': 'us-east-1'})
    print("Bucket creado exitosamente.")
except NoCredentialsError:
    print("Error: No se encontraron las credenciales de AWS.")
except Exception as e:
    print(f"Ocurrió un error: {e}")

