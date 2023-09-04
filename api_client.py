import requests
import socket

failed_requests = []  # Queue to hold failed requests



def fetchActiveDeviceData(api_secret, start_datetime, end_datetime, fi_endPoint, datetime_type):
    end_datetime_str = end_datetime.isoformat()
    start_datetime_str = start_datetime.isoformat()
    request_url = f"{fi_endPoint}?start_datetime={start_datetime_str}&end_datetime={end_datetime_str}&datetime_type={datetime_type}&api_secret={api_secret}"
    
    try:
        response = requests.post(request_url, timeout=10)
        print("Status Code:", response.status_code)
        print("Response Text:", response.text)
        
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
        failed_requests.append({
            'api_secret': api_secret,
            'start_datetime': start_datetime,
            'end_datetime': end_datetime,
            'fi_endPoint': fi_endPoint,
            'datetime_type': datetime_type
        })
        return None

def send_xml_data(xml_data, server_ip, server_port):
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # Send the XML data to the server
        sock.sendto(xml_data.encode(), (server_ip, server_port))
        print("XML data sent successfully!")
    except socket.error as e:
        print("Error sending XML data:", e)
    finally:
        # Close the socket
        sock.close()

def send_json_to_av_endPoint(json_data, av_endPoint):
    try:
        response = requests.post(av_endPoint, json=json_data, timeout=10)
        if response.status_code == 200:
            print("Successfully sent JSON to av_endPoint")
        else:
            print(f"Failed to send JSON, status code: {response.status_code}")
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
        print(f"Failed to send JSON due to {e}")



# Add more API client functions as needed
