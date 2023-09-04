import requests
from data_preprocessor import extract_uid
from config import fi_endPoint, av_endPoint, api_secret, datetime_type, xml_server_ip, xml_server_port
import xml_generator
import api_client
import utils
from datetime import datetime, timedelta
import time


server_ip = xml_server_ip
server_port = xml_server_port

persistent_objects = {}

def processFIInputJSON(fiInputJSON):
    global persistent_objects

    if not fiInputJSON.get('data') or not fiInputJSON['data'].get('data'):
        return

    # Use the serial_number as the uid
    uid = fiInputJSON['data'].get('serial_number', 'default')

    for data in fiInputJSON['data']['data']:
        if isinstance(data, str) or not data.get('sensor'):
            continue

        sensor = data['sensor']
        recorded_at = data['recorded_at']

        if uid not in persistent_objects:
            persistent_objects[uid] = {
                'geometry': {'coordinates': [0, 0], 'type': 'Point'},
                'properties': {'altitude': 0, 'sourceId': '', 'name': '', 'timestamp': ''}
            }

        persistent_object = persistent_objects[uid]

        if sensor['name'] == 'Location':
            persistent_object['geometry']['coordinates'] = data['geolocation']['coordinates']
            persistent_object['properties']['timestamp'] = recorded_at

        elif sensor['name'] == 'Baro Altitude':
            altitude_in_feet = data['value']
            altitude_in_meters = altitude_in_feet * 0.3048
            persistent_object['properties']['altitude'] = altitude_in_meters

        persistent_object['properties']['sourceId'] = uid
        persistent_object['properties']['name'] = uid



'''
def processFIInputJSON(fiInputJSON):
    global persistent_objects

    if not fiInputJSON.get('data') or not fiInputJSON['data'].get('data'):
        return

    for data in fiInputJSON['data']['data']:
        if isinstance(data, str) or not data.get('sensor'):
            continue

        sensor = data['sensor']
        recorded_at = data['recorded_at']
        uid = data.get('uid', 'default')  # Replace 'default' with how you get the UID

        if uid not in persistent_objects:
            persistent_objects[uid] = {
                'geometry': {'coordinates': [0, 0], 'type': 'Point'},
                'properties': {'altitude': 0, 'sourceId': '', 'name': '', 'timestamp': ''}
            }

        persistent_object = persistent_objects[uid]

        if sensor['name'] == 'Location':
            persistent_object['geometry']['coordinates'] = data['geolocation']['coordinates']
            persistent_object['properties']['timestamp'] = recorded_at

        elif sensor['name'] == 'Baro Altitude':
            altitude_in_feet = data['value']
            altitude_in_meters = altitude_in_feet * 0.3048
            persistent_object['properties']['altitude'] = altitude_in_meters

        persistent_object['properties']['sourceId'] = uid
        persistent_object['properties']['name'] = uid

        '''

def update_all_persistent_objects_and_xml():
    for uid, persistent_object in persistent_objects.items():
        # Generate XML string for this persistent_object
        xml_string = xml_generator.create_xml_string(uid, persistent_objects)
        
        if xml_string is None:
            print(f"Skipping UID {uid} due to invalid or missing data.")
            continue

        # Send XML data
        api_client.send_xml_data(xml_string, server_ip, server_port)


from threading import Thread
import time

def main():
    global start_datetime, end_datetime
    
    start_datetime = datetime.utcnow() - timedelta(seconds=4)
    end_datetime = datetime.utcnow()

    from api_server import should_run
    
    try:
        while True:
            print("Main loop running")  # Debugging line
            fiInputJSON = api_client.fetchActiveDeviceData(api_secret, start_datetime, end_datetime, fi_endPoint, datetime_type)
            utils.updateDateTime(start_datetime, end_datetime)

            if fiInputJSON:
                processFIInputJSON(fiInputJSON)

            update_all_persistent_objects_and_xml()

            #sends JSON to endpoint
            api_client.send_json_to_av_endPoint(persistent_objects, av_endPoint)

            # Retry failed requests
            for data in api_client.failed_requests:
                try:
                    response = api_client.fetchActiveDeviceData(
                        data['api_secret'], 
                        data['start_datetime'], 
                        data['end_datetime'], 
                        data['fi_endPoint'], 
                        data['datetime_type']
                    )
                    if response:
                        api_client.failed_requests.remove(data)
                except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                    continue

            time.sleep(1)  # Sleep for a short period to allow for KeyboardInterrupt

    except KeyboardInterrupt:
        print("KeyboardInterrupt received. Cleaning up...")

        #set flag to stop flask in api_server.py
        should_run = False


        print("Cleanup complete. Exiting...")




if __name__ == '__main__':
    main()



