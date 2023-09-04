import requests
import json
from data_preprocessor import extract_uid
from config import fi_endPoint, av_endPoint, api_secret, datetime_type, xml_server_ip, xml_server_port
import xml_generator
import api_client
import utils
from datetime import datetime, timedelta

server_ip = xml_server_ip
server_port = xml_server_port

persistent_objects = {}

def processFIInputJSON(fiInputJSON, persistent_objects):
    if not fiInputJSON.get('data'):
        return

    for data_object in fiInputJSON['data']:
        if not isinstance(data_object, dict):
            continue

        serial_number = data_object.get('serial_number', None)
        if serial_number is None:
            continue

        if serial_number not in persistent_objects:
            persistent_objects[serial_number] = {}

        for sensor_data in data_object.get('data', []):
            sensor_name = sensor_data.get('sensor', {}).get('name', None)
            if sensor_name is None:
                continue

            unique_key = f"{serial_number}_{sensor_name}"

            if unique_key not in persistent_objects[serial_number]:
                persistent_objects[serial_number][unique_key] = {
                    'geometry': {'coordinates': [0, 0], 'type': 'Point'},
                    'properties': {'altitude': 0, 'sourceId': '', 'name': '', 'timestamp': ''}
                }

            persistent_obj = persistent_objects[serial_number][unique_key]
            if sensor_name == 'Location':
                persistent_obj['geometry']['coordinates'] = sensor_data['geolocation']['coordinates']
                persistent_obj['properties']['timestamp'] = sensor_data['recorded_at']
            elif sensor_name == 'Baro Altitude':
                altitude_in_feet = sensor_data['value']
                altitude_in_meters = altitude_in_feet * 0.3048
                persistent_obj['properties']['altitude'] = altitude_in_meters

            persistent_obj['properties']['sourceId'] = serial_number
            persistent_obj['properties']['name'] = unique_key

def main():
    global start_datetime, end_datetime
    
    start_datetime = datetime.utcnow() - timedelta(seconds=4)
    end_datetime = datetime.utcnow()

    from api_server import should_run
    
    try:
        while True:
            fiInputJSON = api_client.fetchActiveDeviceData(api_secret, start_datetime, end_datetime, fi_endPoint, datetime_type)
            utils.updateDateTime(start_datetime, end_datetime)

            if fiInputJSON:
                processFIInputJSON(fiInputJSON, persistent_objects)

            update_all_persistent_objects_and_xml()

            # Send each persistent object as a separate JSON to av_endpoint
            for serial_number, persistent_object in persistent_objects.items():
                api_client.send_json_to_av_endPoint(persistent_object, av_endPoint)

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

            # --- Start of the new code snippet ---
            # Your existing code to prepare data for POST request
            headers = {'Content-Type': 'application/json'}  # Replace with your actual headers
            payload = json.dumps(persistent_objects)  # Replace with your actual payload

            # Make the POST request
            response = requests.post(av_endPoint, data=payload, headers=headers)

            if response.status_code == 200:
                print("Status Code: 200")

                # Parse the JSON response
                parsed_json = json.loads(response.text)

                # Your code to handle the parsed JSON data
                for data_entry in parsed_json['data']['data']:
                    # Extract and process individual fields
                    sensor_name = data_entry['sensor']['name']
                    sensor_value = data_entry['value']
                    # Perform your logic here
                    # ...

            else:
                print(f"Status Code: {response.status_code}")
            # --- End of the new code snippet ---

            try:
            while True:
                print("Main loop running")  # Debugging line
                fiInputJSON = api_client.fetchActiveDeviceData(api_secret, start_datetime, end_datetime, fi_endPoint, datetime_type)
                utils.updateDateTime(start_datetime, end_datetime)

                if fiInputJSON:
                    processFIInputJSON(fiInputJSON)

                update_all_persistent_objects_and_xml()

                # Send each persistent object as a separate JSON to av_endpoint
                for serial_number, persistent_object in persistent_objects.items():
                    api_client.send_json_to_av_endPoint(persistent_object, av_endPoint)

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

            # --- Start of the new code snippet ---
            # Your existing code to prepare data for POST request
            headers = {'Content-Type': 'application/json'}  # Replace with your actual headers
            payload = json.dumps(persistent_objects)  # Replace with your actual payload

            # Make the POST request
            response = requests.post(av_endPoint, data=payload, headers=headers)

            if response.status_code == 200:
                print("Status Code: 200")

                # Parse the JSON response
                parsed_json = json.loads(response.text)

                # Your code to handle the parsed JSON data
                for data_entry in parsed_json['data']['data']:
                    # Extract and process individual fields
                    sensor_name = data_entry['sensor']['name']
                    sensor_value = data_entry['value']
                    # Perform your logic here
                    # ...

            else:
                print(f"Status Code: {response.status_code}")
            # --- End of the new code snippet ---

    except KeyboardInterrupt:
        print("KeyboardInterrupt received. Cleaning up...")
        should_run = False
        print("Cleanup complete. Exiting...")

if __name__ == '__main__':
    main()




#******************************
#******************************
'''
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
    print("Received fiInputJSON:", fiInputJSON)  # Debugging line

    if not fiInputJSON.get('data'):
        return

    for data_object in fiInputJSON['data']:
        if not isinstance(data_object, dict):
            continue  # Skip if not a dictionary

        serial_number = data_object.get('serial_number', None)
        print("Extracted serial_number:", serial_number)  # Debugging line

    global persistent_objects

    # Check if 'data' key exists and it's not empty
    if not fiInputJSON.get('data'):
        return

    # Loop through each data object
    for data_object in fiInputJSON['data']:

        if not isinstance(data_object, dict):
            continue  # Skip if not a dictionary

        serial_number = data_object.get('serial_number', None)
        if serial_number is None:
            continue  # Skip this object if no serial_number

        # Initialize if this serial_number is new
        if serial_number not in persistent_objects:
            persistent_objects[serial_number] = {}

        # Loop through each sensor data in 'data' key
        for sensor_data in data_object.get('data', []):
            sensor_name = sensor_data.get('sensor', {}).get('name', None)
            if sensor_name is None:
                continue  # Skip this data if no sensor_name

            # Create a unique key for this serial_number and sensor_name pair
            unique_key = f"{serial_number}_{sensor_name}"

            # Initialize if this unique_key is new
            if unique_key not in persistent_objects[serial_number]:
                persistent_objects[serial_number][unique_key] = {
                    'geometry': {'coordinates': [0, 0], 'type': 'Point'},
                    'properties': {'altitude': 0, 'sourceId': '', 'name': '', 'timestamp': ''}
                }

            # Update the persistent object with new data
            persistent_obj = persistent_objects[serial_number][unique_key]
            if sensor_name == 'Location':
                persistent_obj['geometry']['coordinates'] = sensor_data['geolocation']['coordinates']
                persistent_obj['properties']['timestamp'] = sensor_data['recorded_at']
            elif sensor_name == 'Baro Altitude':
                altitude_in_feet = sensor_data['value']
                altitude_in_meters = altitude_in_feet * 0.3048
                persistent_obj['properties']['altitude'] = altitude_in_meters

            persistent_obj['properties']['sourceId'] = serial_number
            persistent_obj['properties']['name'] = unique_key  # Or any other name logic you have

            print("Updated persistent_objects:", persistent_objects)  # Debugging line
                # Send each persistent object as a separate JSON to av_endpoint
    for serial_number, persistent_object in persistent_objects.items():
        response = api_client.send_json_to_av_endPoint(persistent_object, av_endPoint)
        if response.status_code != 200:
            print(f"Failed to send data for serial_number {serial_number} to av_endpoint. Status code: {response.status_code}")



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

            # Send each persistent object as a separate JSON to av_endpoint
            for serial_number, persistent_object in persistent_objects.items():
                api_client.send_json_to_av_endPoint(persistent_object, av_endPoint)

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

            time.sleep(1)  # Sleep for a short period to allow for KeyboardInterrupt

            # --- Start of the new code snippet ---
            # Your existing code to prepare data for POST request
            headers = {'Content-Type': 'application/json'}  # Replace with your actual headers
            payload = json.dumps(persistent_objects)  # Replace with your actual payload

            # Make the POST request
            response = requests.post(av_endPoint, data=payload, headers=headers)

            if response.status_code == 200:
                print("Status Code: 200")

                # Parse the JSON response
                parsed_json = json.loads(response.text)

                # Your code to handle the parsed JSON data
                for data_entry in parsed_json['data']['data']:
                    # Extract and process individual fields
                    sensor_name = data_entry['sensor']['name']
                    sensor_value = data_entry['value']
                    # Perform your logic here
                    # ...

            else:
                print(f"Status Code: {response.status_code}")
            # --- End of the new code snippet ---

    except KeyboardInterrupt:
        print("KeyboardInterrupt received. Cleaning up...")

        #set flag to stop flask in api_server.py
        should_run = False


        print("Cleanup complete. Exiting...")




if __name__ == '__main__':
    main()



