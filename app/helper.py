from functools import wraps
from flask import current_app
from flask_jwt_extended import jwt_required


def jwt_optional_for_tests(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_app.config.get('SKIP_AUTH', False):  # if I am testing
            return func(*args, **kwargs)
        else:
            return jwt_required()(func)(*args, **kwargs)
    return wrapper
