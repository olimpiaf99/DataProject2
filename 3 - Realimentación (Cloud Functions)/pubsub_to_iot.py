#Cloud Function triggered by PubSub Event

#Import libraries
import base64, json, sys, os
from google.cloud import iot_v1
import random

#Read from PubSub
def pubsub_to_iot(event, context):
    #Read message from Pubsub (decode from Base64)
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')

    #Load json
    message = json.loads(pubsub_message)

    #Dealing with environment variables
    project_id = os.environ['PROJECT_ID']
    cloud_region = os.environ['REGION_ID']
    registry_id = os.environ['REGISTRY_ID']
    device_id = os.environ['DEVICE_ID']

    #Logic for incoming data
    room_glucosa = range(70,140)

    if message['aggGlucosa'] in room_glucosa:
        print("Glucosa OK")
        pass
    else:

        #IoT Client
        client = iot_v1.DeviceManagerClient()
        
        #Execute IoT Command
        '''https://cloud.google.com/iot/docs/how-tos/commands#iot-core-send-command-python'''
        device_path = client.device_path(project_id, cloud_region, registry_id, device_id)

        command = "Administrando dosis"
        data = command.encode('utf-8')

        client.send_command_to_device(request={"name": device_path, "binary_data": data})

        #Check for last version updated
        '''https://cloud.google.com/iot/docs/how-tos/config/configuring-devices#iot-core-get-config-python'''
        configs = client.list_device_config_versions(request={"name": device_path})
        configs_list = []

        for item in configs.device_configs:
            configs_list.append(item.version)
        
        last_version = max(configs_list)

        #Update device configuration
        '''https://cloud.google.com/iot/docs/how-tos/config/configuring-devices#iot-core-update-config-python'''
        config = "Dosis administrada"
        config_data = config.encode('utf-8')

        client.modify_cloud_to_device_config(request={"name": device_path, "binary_data": config_data, "version_to_update": last_version})
