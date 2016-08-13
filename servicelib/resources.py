
import sys
import errors
from datetime import datetime
from flask import request
from flask_restful import Resource

def ok_json(value):
    return {'message': value}


def error_json(value):
    return {'error': value}

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
        except errors.HttpException, exc:
            return error_json(exc.message), exc.status
        except Exception, exc:
            print >> sys.stderr, "HttpMethod: %s, Resource: %s, Handler: %s" % (http_method, self.__class__, method_name)
            raise

    def param_if_exists(self, param_name):
        param_value = None
        if request.get_json():
            param_value = request.get_json().get(param_name, "")
        if param_value is None:
            param_value = request.args.get(param_name)
        return param_value
