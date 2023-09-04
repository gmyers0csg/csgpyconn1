import logging
import json
from xml.etree import ElementTree as ET

def extract_uid(data, data_format='json'):
    """
    Extracts the UID from the incoming data.
    Handles both JSON and XML data formats.
    """
    uid = None
    try:
        if data_format == 'json':
            uid = data.get('data', {}).get('uid', None)
        elif data_format == 'xml':
            root = ET.fromstring(data)
            uid_element = root.find(".//uid")
            if uid_element is not None:
                uid = uid_element.text
        else:
            raise ValueError("Unsupported data format")
    except Exception as e:
        logging.error(f"An error occurred while extracting UID: {e}")
    return uid


# Add more data preprocessing functions as needed
