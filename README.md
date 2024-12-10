# Cloud
Los pasos a seguir fueron los siguentes:
1. Crear el bucket de S3

    Se crearán dos buckets: uno para las imágenes originales y otro para los thumbnails.

2. Configurar SQS

    Crear una cola de SQS que reciba los eventos de las imágenes cargadas, lo que desencadenará la creación de thumbnails.

3. Configurar DynamoDB

    Crear una tabla de DynamoDB para almacenar los metadatos de las imágenes (nombre de archivo, URL, tamaño de imagen, etc.).

4. Configurar AWS Lambda

    Lambda procesará las imágenes cargadas y generará thumbnails, guardándolos en S3. El metadato correspondiente se almacenará en DynamoDB.

5. Crear una página web simple

    Usaremos un servicio de hosting estático como S3 o Amplify para alojar una página web sencilla que permitirá a los usuarios ver los thumbnails generados.
