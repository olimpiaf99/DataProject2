# GLUTECH
![logo](https://github.com/olimpiaf99/DataProject2/blob/main/4%20-%20Im%C3%A1genes/Logo.svg)

# Data Project 2

## Master en Data Analytics - EDEM
### Curso 2021/2022

- Pablo Sanchez Saez
- Galo Valle
- Alfonso Monserrat
- Olimpia Fuster
- Ricardo Villalta


## Caso de uso

**En este evento presentamos vuestro producto IoT como Serverless.**

# IoT Serverless arquitectura en tiempo real

#### Descripción del caso

GLUTECH es una startup tecnológica centrada en la mejora de la calidad de vida de los pacientes con Diabetes. Esto se lleva a cabo a través de una tecnología que permite  monitorizar los niveles de glucosa en sangre sin necesidad de pinchar al paciente, haciéndolo especialmente conveniente para niños y adolescentes. Todo ello arropado por un sistema de alertas en tiempo real que permite a la persona interesada estar al corriente en todo momento de las posibles necesidades del paciente.

#### Business challenges

- Parte 01: Monitorizar el registro de las diferentes variables y mostrarlas en una aplicación.
- Parte 02: Administrar la dosis de insulina necesaria al paciente en caso de registrarse un shock hiperglucémico.

#### Data Architecture

![architecture](https://github.com/olimpiaf99/DataProject2/blob/main/5%20-%20Arquitectura%20y%20diagrama/arquitectura.png)

# Part 01: Procesamiento de datos Serverless con Dataflow

## Requisitos

- Entramos a google cloud y abrimos nuestro Cloud Shell.

- Clonamos este repositorio:

  ```
  $ git clone https://github.com/olimpiaf99/DataProject2.git
  ```

- Creamos un nuevo proyecto llamado "GlutechProject"

- Abilita APIS requeridos por el cloud:

```
gcloud config set project <id_tu_proyecto>
gcloud services enable dataflow.googleapis.com
gcloud services enable cloudiot.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

- Creando entorno Python

```
virtualenv -p python3 <glutech>
source <glutech>/bin/activate
```

- Instalando dependencias de python:

```
pip install -U -r setup_dependencies.txt
```

## PubSub

Creamos dos topics;

1. Conectará con Dataflow 
2. Conectará con CloudFunctions  

![pubsub](https://github.com/RicardoVRR/DataProject2./blob/main/DataProject2/pubsub%20topics.png)

## Cloud Storage

Go to Cloud Console [Cloud Storage](https://console.cloud.google.com/storage) page.

- Crea un bucket donde se almacenará el Flex Template usado para Dataflow, nombre del bucket: <edem-serverless-bucket10>

  ![datastorage](https://github.com/RicardoVRR/DataProject2./blob/main/DataProject2/datastorage.png?raw=true)

  

## IoT Core

Para conectar con nuestros dispositivos vamos al servicio IoT Core:

- Creamos registro IoT  eligiendo un Topic creado anteriormente

- Generamos desde el shell una clave **RSA key with self-signed X509 certificate**.  [info](https://cloud.google.com/iot/docs/how-tos/credentials/keys#generating_an_rsa_key)

  y accedemos a ella desde el explorador.

  ![key](https://github.com/RicardoVRR/DataProject2./blob/main/DataProject2/Captura%20de%20pantalla%202022-03-06%20a%20las%2020.25.40%20(2).png?raw=true)

  

  Aplicamos y creamos el dispositivo.

  ![iot_registry_device](https://github.com/RicardoVRR/DataProject2./blob/main/DataProject2/iot_registry_device.png?raw=true)

## BigQuery

- Cremos una tabla en BigQuery donde almacenaremos posteriormente los datos generados.

![bigquery](https://github.com/RicardoVRR/DataProject2./blob/main/DataProject2/bigquery.png)



## Dataflow

- Utilizaremos Dataflow con un Flex Template que actuará como cliente de pub/sub, creando el pipeline que almacene los datos en BigQuery desde el dispositivo IoT.
- Empaquetar código python en una imagen Docker y almacenar en contenedor:

```
gcloud builds submit --tag 'gcr.io/<YOUR_PROJECT_ID>/<YOUR_FOLDER_NAME>/<YOUR_IMAGE_NAME>:latest' .
```

- Crear Dataflow Flex Template a partir de la imagen:

```
gcloud dataflow flex-template build "gs://<YOUR_BUCKET_NAME/<YOUR_TEMPLATE_NAME>.json" \
  --image "gcr.io/<YOUR_PROJECT_ID>/<YOUR_FOLDER_NAME>/<YOUR_IMAGE_NAME>:latest" \
  --sdk-language "PYTHON"  
```

- Activar Dataflow Flex Template:

```
gcloud dataflow flex-template run "<YOUR_DATAFLOW_JOB_NAME>" \
    --template-file-gcs-location "gs://edem_serverless_bucket/edemTemplate.json" \
    --region "europe-west1"
```



![Dataflow](https://github.com/RicardoVRR/DataProject2./blob/main/DataProject2/Dataflow.jpeg)



**Enviar datos desde el dispositivo:**

Vamos a la carpeta de IoTCore donde se encuentra el script de python edemDeviceData.py y lo ejecutamos para empezar a generar datos.

```
python edemDeviceData.py \
    --algorithm RS256 \
    --cloud_region europe-west1 \
    --device_id <YOUR_IOT_DEVICE_NAME> \
    --private_key_file rsa_private.pem \
    --project_id <YOUR_PROJECT_ID> \
    --registry_id <YOUR_IOT_REGISTRY>
```




# Part 02: Arquitectura basada en eventos. Cloud Functions

- Vamos a Cloud Functions y creamos una función eligiendo PubSub como activador y creamos las variables del entorno de ejecución.
- Elegimos Python 3.9
- Copiamos nuestro codigo en el archivo Main.py y las dependencias en requirements.txt.
  ![cloudfunctions](https://github.com/RicardoVRR/DataProject2./blob/main/DataProject2/CloudFunctions.png)
- Click deploy
  
Si el nivel de Glucosa está por encima de los parámetros establecidos como normales, **entre 70 y 130**. El dispositivo administra una dosis, mientras que si está dentro del rango envía un mensaje de **"Glucosa OK"**.


## Visualización

Implementamos una app para que el paciente pueda ver en tiempo real sus métricas:
  
  ![img](https://github.com/RicardoVRR/DataProject2./blob/main/DataProject2/app.jpeg)



## Vídeo demo
  
  [Arquitectura en Google Cloud](https://youtu.be/Rg-ubRqPy5E)  
  [App User Experience](https://drive.google.com/file/d/1MFQW6P7tp7WUDAzMvu7rsGspI2RsN-Hq/view)

