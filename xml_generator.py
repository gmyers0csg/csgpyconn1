from datetime import datetime, timedelta

def create_xml_string(uid, persistent_objects):
    persistent_object = persistent_objects.get(uid)
    if persistent_object:
        lon, lat = persistent_object['geometry']['coordinates']
        timestamp = persistent_object['properties']['timestamp']
        
        if not timestamp:  # Check if timestamp is empty
            print("Warning: Empty timestamp")
            return None

        # Convert timestamp to datetime object if it's a string
        if isinstance(timestamp, str):
            try:
                timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
            except ValueError:
                print(f"Invalid timestamp format: {timestamp}")
                return None

        time_str = timestamp.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        start_str = (timestamp + timedelta(seconds=8)).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        stale_str = (timestamp + timedelta(hours=2)).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        
        altitude = persistent_object['properties']['altitude']

        xml_data = f'''<?xml version="1.0" encoding="UTF-8"?>
<event version="2.0" uid="{uid}" type="a-f-A-C-H-Q" time="{time_str}" start="{start_str}" stale="{stale_str}" how="m-g">
  <point lat="{lat}" lon="{lon}" hae="{altitude}" ce="9999999.0" le="9999999.0"/>
</event>'''
        return xml_data
