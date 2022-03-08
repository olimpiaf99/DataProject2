# GLUTECH
![Captura de pantalla 2022-03-08 a las 7.03.43](/Users/RicardoVReig/Desktop/Captura de pantalla 2022-03-08 a las 7.03.43.png)

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
- Parte 02: Administrar la dosis de insulina necesaria al paciente en caso de registrarse un shock hipoglucémico.

#### Data Architecture

[![img](https://github.com/jabrio/Serverless_EDEM/raw/main/00_DocAux/iot_arch.jpg)](https://github.com/jabrio/Serverless_EDEM/blob/main/00_DocAux/iot_arch.jpg)

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



![pubsub topics](/Users/RicardoVReig/Desktop/pubsub topics.png)

## Cloud Storage

Go to Cloud Console [Cloud Storage](https://console.cloud.google.com/storage) page.

- Crea un bucket donde se almacenará el Flex Template usado para Dataflow, nombre del bucket: <edem-serverless-bucket10>

  

  ![datastorage](/Users/RicardoVReig/Desktop/datastorage.png)

## IoT Core

Para conectar con nuestros dispositivos vamos al servicio IoT Core:

- Creamos registro IoT  eligiendo un Topic creado anteriormente

- Generamos desde el shell una clave **RSA key with self-signed X509 certificate**.  [info](https://cloud.google.com/iot/docs/how-tos/credentials/keys#generating_an_rsa_key)

  y accedemos a ella desde el explorador.

  ![Captura de pantalla 2022-03-06 a las 20.25.40 (2)](/Users/RicardoVReig/Desktop/Captura de pantalla 2022-03-06 a las 20.25.40 (2).png)

- Aplicamos y creamos el dispositivo.

  ![iot_registry_device](/Users/RicardoVReig/Desktop/iot_registry_device.png)



## BigQuery

- Cremos una tabla en BigQuery donde almacenaremos posteriormente los datos generados.
- ![bigquery](/Users/RicardoVReig/Desktop/bigquery.png)

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



![Dataflow](/Users/RicardoVReig/Desktop/Dataflow.jpeg)

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



## Verify data is arriving and visualize them with Data Studio

- Go to [BigQueryUI](https://console.cloud.google.com/bigquery) and you should see your bigquery table already created.

[![img](https://github.com/jabrio/Serverless_EDEM/raw/main/00_DocAux/bq_ui.PNG)](https://github.com/jabrio/Serverless_EDEM/blob/main/00_DocAux/bq_ui.PNG)

- Go to [**Data Studio**](https://datastudio.google.com/). Link your BigQuery table.
- Create a Dashboard as shown below, which represents temperature and humidity of the device.

[![img](https://github.com/jabrio/Serverless_EDEM/raw/main/00_DocAux/Dashboard.PNG)](https://github.com/jabrio/Serverless_EDEM/blob/main/00_DocAux/Dashboard.PNG)

# Part 02: Event-driven architecture with Cloud Functions

- Go to [CloudFunctions folder](https://github.com/jabrio/Serverless_EDEM/blob/main) and follow the instructions placed in edemCloudFunctions.py file.
- Go to Cloud Console [Cloud Functions](https://console.cloud.google.com/functions) page.
- Click **Create Function** (europe-west1) and choose **PubSub** as trigger type and click **save**.
- Click **Next** and choose **Python 3.9** as runtime.
- Copy your code into Main.py file and python dependencies into requirements.txt.
- when finished, Click **deploy**.
- If an aggregate temperature by minute is out-of-range, **a command will be thrown to the device and its config will be updated**. You can check that by going to *config and state* tab in IoT device page.
- Useful information: [IoT Core code samples](https://cloud.google.com/iot/docs/samples)




## Vídeo demo
