
# Examnen Cloud

## Enunciado del ejercicio:

Creación de una aplicación que almacena imágenes en S3, genera thumbnails, envía mensajes a SQS, guarda metadatos en DynamoDB y ofrece una página web simple para visualizar los thumbnails, donde una función Lambda será la encargada de realizar la conversión y guardar los metadatos en la BBDD".

## Prerrequisitos
```bash
pip install pillow

```

**Nota:**  El código utilizado para cada fichero se encuentra dentro de este repositorio

## Pasos a seguir
1.	Crear el bucket de S3
1.1.	Crear ul fichero llamado buckets.py en el cual se crean dos buckets: uno para las imágenes originales y otro para los thumbnails.

1.2.	En AWS usar la opción Upload en CloudShell para cargar el archivo. Para verificar si el fichero se cargó correctamente utilizamos el comando:
```bash
 ls
 ```
1.3.	Ejecutamos el script con el siguiente comando: python “nombreDelScript”.py
```bash
python buckets.py
```
1.4.	Para verificar los buckets creados utilizamos el siguiente comando:
```bash
aws s3 ls
```
 
2.	Configurar SQS
2.1.	Crear ul fichero llamado sqs.py en el cual se crea una cola de SQS que reciba los eventos de las imágenes cargadas, lo que desencadenará la creación de thumbnails.

2.2.	En AWS usar la opción Upload en CloudShell para cargar el archivo. Para verificar si el fichero se cargó correctamente utilizamos el comando:
```bash
 ls
 ```

2.3.	Ejecutamos el script con el siguiente comando: python “nombreDelScript”.py
```bash
python sqs.py
```

3.	Configurar DynamoDB
3.1.	Crear ul fichero llamado TablaDynamoDB.py en el cual se crea una tabla de DynamoDB para almacenar los metadatos de las imágenes (nombre de archivo, URL, tamaño de imagen, etc.).

3.2.	En AWS usar la opción Upload en CloudShell para cargar el archivo. Para verificar si el fichero se cargó correctamente utilizamos el comando:
```bash
ls
```
3.3.	Ejecutamos el script con el siguiente comando: python “nombreDelScript”.py
```bash
python TablaDynamoDB.py
```
 
4.	Configurar AWS Lambda
4.1.	Crear ul fichero llamado fucionLambda.py en el cual se procesará las imágenes cargadas y generará thumbnails, guardándolos en S3. El metadato correspondiente se almacenará en DynamoDB.

4.2.	En AWS usar la opción Upload en CloudShell para cargar el archivo. Para verificar si el fichero se cargó correctamente utilizamos el comando:
```bash
ls
```
4.3.	Ejecutamos el script con el siguiente comando: python “nombreDelScript”.py
```bash
python fucionLambda.py
```
 
4.4.	 Configurar la función Lambda:
En la consola de AWS Lambda crear una nueva función Lambda con el lenguaje Python.
Completa los campos necesarios:
- Function name: Ingresa un nombre como "GenerarThumbnail".
- Runtime: Seleccionar "Python 3.9" .
 
4.5.	Creamos un evento 

5. Crear una página web simple

5.1. Crear un fichero index.html

