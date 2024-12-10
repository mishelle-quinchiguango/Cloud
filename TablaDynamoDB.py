import boto3

TABLE_NAME = "MetadatosImagenes"

dynamodb = boto3.client('dynamodb', region_name='us-east-1')

# Crear la tabla
def crear_tabla_dynamodb():
    try:
        response = dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {
                    'AttributeName': 'NombreArchivo',
                    'KeyType': 'HASH'  
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'NombreArchivo',
                    'AttributeType': 'S' 
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        print(f"Tabla '{TABLE_NAME}' creada exitosamente.")
        print(response)
    except Exception as e:
        print(f"Error al crear la tabla: {e}")

if __name__ == "__main__":
    crear_tabla_dynamodb()

