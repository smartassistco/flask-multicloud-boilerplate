from functools import wraps

from flask import request

from .responses import error_envelope
from .config import config


def require_api_key():
    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            try:
                api_key = request.headers.get('X-Api-Key')
                if not config.DEBUG:
                    assert api_key == config.API_KEY
                return func(*args, **kwargs)
            except AssertionError:
                return error_envelope('ACCESS DENIED', 'Invalid API Key')

        return inner

    return decorator
