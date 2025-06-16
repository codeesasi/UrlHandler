from datetime import datetime, UTC

def get_current_utc_datetime() -> datetime:
    """
    Returns the current time in UTC.
    
    :return: Current time in UTC.
    """
    return datetime.now(UTC).isoformat()