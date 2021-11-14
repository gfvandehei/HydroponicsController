from proxyserver.utils.authentication import Authenticator
from flask import Blueprint

def generate_test_routes(auth: Authenticator):
    bp =  Blueprint("tester", __name__)

    @bp.route("/admin")
    @auth(admin_required=True)
    def admin_test_route():
        return {}

    @bp.route("/")
    @auth()
    def admin_test_route():
        return {}
    
    return bp