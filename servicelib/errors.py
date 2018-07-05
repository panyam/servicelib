
class SLException(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)
        self.message = msg

class Unauthorized(SLException): pass
class NotFound(SLException): pass
class NotAllowed(SLException): pass
class ValidationError(SLException): pass
