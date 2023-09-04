from datetime import datetime, timedelta

def updateDateTime(start, end):
    end = datetime.utcnow()
    start = end - timedelta(seconds=4)
    print(start, end)
    return start, end  # return updated values

def getRequestURL(fi_endPoint, api_secret, start_datetime, end_datetime, datetime_type):
    start_datetime_str = start_datetime.isoformat() + "Z"
    end_datetime_str = end_datetime.isoformat() + "Z"
    return f'{fi_endPoint}?api_secret={api_secret}&start_datetime={start_datetime_str}&end_datetime={end_datetime_str}&datetime_type={datetime_type}'
