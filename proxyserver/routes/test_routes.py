from proxyserver.utils.authentication import Authenticator
from flask import Blueprint, abort, g
from functools import wraps

def restricted(access_level):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(access_level)
            return func(*args, **kwargs)
        return wrapper
    return decorator


def generate_test_routes(auth: Authenticator):
    bp =  Blueprint("tester", __name__)

    @bp.route("/admin")
    @auth(admin_required=True)
    def admin_test_route():
        return {}

    @bp.route("/")
    @auth(admin_required=False)
    def admin_test_route():
        return {}
    
    return bp