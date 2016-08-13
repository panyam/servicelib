
class SLException(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)
        self.message = msg

class HttpException(SLException):
    def __init__(self, msg, status):
        SLException.__init__(self, msg)
        self.status = status

class ValidationError(SLException):
    def __init__(self, msg):
        SLException.__init__(self, msg)
