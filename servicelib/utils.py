
import os

def is_dev_mode():
    return os.environ.get('APPLICATION_ID').startswith("dev~")

DEFAULT_DATE_FORMAT = "%Y-%m-%d"

def ensure_date(date_format = DEFAULT_DATE_FORMAT):
    import datetime
    def ensurer(strinput):
        return datetime.datetime.strptime(strinput, date_format)
    return ensurer

def get_custom_id(kwargs):
    id = None
    if is_dev_mode() and "id" in kwargs:
        id = kwargs["id"]
    return id
