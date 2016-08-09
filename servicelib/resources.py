
import sys
from datetime import datetime
from flask import request
from flask_restful import Resource

def ok_json(value):
    return {'message': value}


def error_json(value):
    return {'error': value}

class HttpException(Exception):
    def __init__(self, msg, status):
        Exception.__init__(self, msg)
        self.message = msg
        self.status = status

class BaseResource(Resource):
    """
    A wrapper to work with restful calls on restli formatted resources.
    """
    def get_routes(cls):
        return []

    def get(self, **kwargs):
        method_name = "do_get"
        if request.args.get("q", "").strip():
            method_name = "do_finder_by_%s" % request.args.get("q", "").strip()
        elif request.args.get("ids", "").strip():
            method_name = "do_batch_get"
        elif len(kwargs.keys()) == 0:
            method_name = "do_finder"
        return self.find_and_invoke_method("GET", method_name, **kwargs)

    def post(self, **kwargs):
        method_name = "do_create"
        # see if we have a partial update
        if request.headers.get("X-RestLi-Method", "").strip():
            method_name = "do_post_%s" % request.headers.get("X-RestLi-Method", "").strip()
        elif request.args.get("action", "").strip():
            method_name = "do_action_%s" % request.args.get("action", "").strip()
        return self.find_and_invoke_method("POST", method_name, **kwargs)

    def put(self, **kwargs):
        method_name = "do_put"
        if request.headers.get("X-RestLi-Method", "").strip():
            method_name = "do_put_%s" % request.headers.get("X-RestLi-Method", "").strip()
        return self.find_and_invoke_method("PUT", method_name, **kwargs)

    def delete(self, **kwargs):
        method_name = "do_delete"
        return self.find_and_invoke_method("DELETE", method_name, **kwargs)

    def find_and_invoke_method(self,http_method, method_name, **kwargs):
        if not hasattr(self, method_name):
            return error_json("%s handler (%s) not found" % (http_method, method_name)), 405
        try:
            return getattr(self, method_name)(**kwargs)
        except HttpException, exc:
            return error_json(exc.message), exc.status
        except Exception, exc:
            print >> sys.stderr, "HttpMethod: %s, Resource: %s, Handler: %s" % (http_method, self.__class__, method_name)
            raise

    def ensure_param(self, param_name, converter = None, no_blank = True):
        """
        Ensures that a parameter by a given name exists, and can be applied to the converter (if provided)
        If the parameter by the name does not exist or if converter(param_value) throws an exception
        then a HttpException is thrown.
        """
        param_value = None
        if request.get_json():
            param_value = request.get_json().get(param_name, "")
        if param_value is None:
            param_value = request.args.get(param_name)
        if param_value is None and no_blank:
            print "param_name, param_value = ", param_name, param_value
            print "json = ", request.get_json()
            raise HttpException("Parameter '%s' is required" % param_name, 400)
        if type(param_value) in (str, unicode):
            param_value = param_value.strip()
        if converter:
            try:
                return converter(param_value)
            except Exception, exc:
                raise HttpException("Unable to coerce parameter: '%s'" % param_name, 400)
        return param_value
