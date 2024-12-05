import boto3

dynamodb = boto3.resource('dynamodb')


def create_dynamodb_table():
    table = dynamodb.create_table(
        TableName='images-metadata-table',
        KeySchema=[
            {
                'AttributeName': 'image_id',
                'KeyType': 'HASH'  
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'image_id',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    table.meta.client.get_waiter('table_exists').wait(TableName='images-metadata-table')
    print("Tabla DynamoDB creada exitosamente.")

create_dynamodb_table()
