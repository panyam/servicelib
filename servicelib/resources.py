
from __future__ import unicode_literals, absolute_import
import json
import traceback, sys
from functools import wraps
from flask import request
from flask_restplus import Resource, fields
import utils
import errors

def handle_api_errors(handler):
    @wraps(handler)
    def decorated_handler(*args, **kwargs):
        try:
            return handler(*args, **kwargs)
        except errors.NotFound, error:
            traceback.print_exc()
            return utils.error_json(error.message), 404
        except errors.NotAllowed, error:
            traceback.print_exc()
            return utils.error_json(error.message), 403
        except errors.NotAllowed, error:
            traceback.print_exc()
            return utils.error_json(error.message), 403
        except errors.Unauthorized, error:
            traceback.print_exc()
            from google.appengine.api import users
            return utils.error_json(error.message), 401, {'Location': users.create_login_url('/mysession/')}
        except errors.ValidationError, error:
            traceback.print_exc()
            return utils.error_json(error.message), 400
        except Exception, exc:
            # exc_type, exc_value, tb = sys.exc_info()
            traceback.print_exc()
            raise exc
    return decorated_handler

class BaseResource(Resource):
    method_decorators = [ handle_api_errors ]
    def __init__(self, *args, **kwargs):
        self._request_member = None
        self._params = None

    @property
    def params(self):
        if self._params is None:
            self._params = utils.RequestParamSource(request)
        return self._params

    @property
    def request_member(self):
        if self._request_member is None:
            # CYCLE DEPENDANCY ALERT!!!
            from nesteggs.auth.engine import get_request_member
            _, self._request_member = get_request_member(request)
        return self._request_member
