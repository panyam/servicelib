
import logging
import os, datetime
import errors
from itertools import izip
from flask import json

class RequestParamSource(object):
    def __init__(self, request):
        self.request = request
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
