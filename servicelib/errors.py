

class HttpException(Exception):
    def __init__(self, msg, status):
        Exception.__init__(self, msg)
        self.message = msg
        self.status = status
