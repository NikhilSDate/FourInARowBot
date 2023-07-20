import functools

from flask import request, abort
import hashlib

from server.db.db import get_api_key_details


def check_api_key(key):
    docs = list(get_api_key_details(hashlib.sha256(key.encode('utf-8')).hexdigest()))
    return len(docs) == 1


def require_api_key(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = request.headers.get('Authorization')
        if key and check_api_key(key):
            return func(*args, **kwargs)
        else:
            abort(401)
    return wrapper

