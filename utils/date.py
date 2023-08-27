from datetime import datetime, timezone

def get_today_midnight_utc():
    try:
        # Get current UTC time
        current_utc_time = datetime.now(timezone.utc)
        # Get timestamp for the start of the day in UTC
        start_of_day_utc = current_utc_time.replace(hour=0, minute=0, second=0, microsecond=0)
        # Get timestamp in seconds since the Unix epoch
        timestamp_in_seconds = int(start_of_day_utc.timestamp())
        print(timestamp_in_seconds)
        return timestamp_in_seconds
    except Exception as e:
            raise e

def get_current_utc():
    try:
        # Get current UTC time
        current_utc_time = datetime.now(timezone.utc)
        # Get timestamp in seconds since the Unix epoch
        timestamp_in_seconds = int(current_utc_time.timestamp())
        print(timestamp_in_seconds)
        return timestamp_in_seconds
    except Exception as e:
        raise e