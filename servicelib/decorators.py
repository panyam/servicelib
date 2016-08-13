
from flask import request
import errors


def ensure_param(param_name, validator=None, no_blank=True, target=None, only_if_exists=False):
    """
    Decorator applied to a request handler that ensures that if a param does not exist then
    a 400 is returned, otherwise the param is appropriately validated and converted and
    set back into the kwargs.
    """
    def ensure_param_func(request_handler_func):
        def worker_func(*args, **kwargs):
            """
            Ensures that a parameter by a given name exists, and can be applied to the validator (if provided)
            If the parameter by the name does not exist or if validator(param_value) throws an exception
            then a errors.HttpException is thrown.
            """
            if not kwargs:
                kwargs = {}
            param_value = kwargs.get(param_name, None)
            if param_value is None and request.get_json():
                param_value = request.get_json().get(param_name, "")
            if param_value is None:
                param_value = request.args.get(param_name)
            if param_value is None and no_blank and not only_if_exists:
                print "param_name, param_value = ", param_name, param_value
                print "json = ", request.get_json()
                raise errors.HttpException("Parameter '%s' is required" % param_name, 400)
            if type(param_value) in (str, unicode):
                param_value = param_value.strip()
            if validator:
                try:
                    param_value = validator(param_value)
                except Exception, exc:
                    raise errors.ValidationError("Unable to coerce parameter: '%s'" % param_name)
            kwargs[target or param_name] = param_value
            return request_handler_func(*args, **kwargs)
        worker_func.func_name = request_handler_func.func_name
        return worker_func
    return ensure_param_func

