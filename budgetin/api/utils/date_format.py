from datetime import datetime

def timestamp_to_strdateformat(timestamp, format):
    date_time_obj = datetime.fromisoformat(timestamp)
    return date_time_obj.strftime(format)