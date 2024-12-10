import boto3

# Nombres de los buckets
BUCKET_ORIGINAL = "imagenes-originales-ejercicio"
BUCKET_THUMBNAILS = "imagenes-thumbnails-ejercicio"

# Crear el cliente de S3
s3 = boto3.client('s3')

# Crear los buckets
def crear_buckets():
    try:
        # Crear bucket para imágenes originales
        s3.create_bucket(Bucket=BUCKET_ORIGINAL)
        print(f"Bucket '{BUCKET_ORIGINAL}' creado exitosamente.")

        # Crear bucket para thumbnails
        s3.create_bucket(Bucket=BUCKET_THUMBNAILS)
        print(f"Bucket '{BUCKET_THUMBNAILS}' creado exitosamente.")
    
    except Exception as e:
        print(f"Error al crear los buckets: {e}")

if __name__ == "__main__":
    crear_buckets()

