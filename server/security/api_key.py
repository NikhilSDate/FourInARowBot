import functools

from flask import request, abort
import hashlib

from server.app import check_api_key


def require_api_key(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = request.headers.get('Authorization')
        if key and check_api_key(key):
            return func(*args, **kwargs)
        else:
            abort(401)
    return wrapper
