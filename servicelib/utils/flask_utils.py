
from flask import json
from werkzeug.routing import BaseConverter

class LongConverter(BaseConverter):
    def to_python(self, value):
        return long(value)

    def to_url(self, value):
        return str(value)

class NEJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        from google.appengine.ext import ndb
        if isinstance(obj, datetime.datetime):
            return (obj - DATE_ZERO).total_seconds()
        elif isinstance(obj, ndb.Key):
            return obj.id()
        elif hasattr(obj, "to_json"):
            return obj.to_json()
        return super(NEJsonEncoder, self).default(obj)

class FlaskRequestParamsDict(object):
    def __init__(self, flask_request):
        self.request = flask_request
        self.request_json = self.request.get_json()

    def __contains__(self, key):
        if self.request.values and key in self.request.values:
            return True

        if self.request_json and key in self.request_json:
            return True

        if self.request.args and key in self.request.args:
            return True

        return False

    def get(self, param_name):
        if param_name in self.request.values:
            param_value = self.request.values.get(param_name)
        else:
            rj = self.request_json
            if rj and param_name in rj:
                param_value = rj.get(param_name)
            else:
                # Try query params
                param_value = self.request.args.get(param_name)
        return param_value
