
import os

def is_dev_mode():
    return os.environ.get('APPLICATION_ID').startswith("dev~")
