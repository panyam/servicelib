
import os

def is_dev_mode():
    return os.environ.get('APPLICATION_ID').startswith("dev~")

DEFAULT_DATE_FORMAT = "%Y-%m-%d"

def ensure_date(date_format = DEFAULT_DATE_FORMAT):
    import datetime
    def ensurer(strinput):
        return datetime.datetime.strptime(date_format)
