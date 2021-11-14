import hydroserver.model.model as Model
from hydroserver.controllers.database import DatabaseConnectionController
from proxyserver.utils.authentication import Authenticator

from flask import Blueprint, request

def generate_user_blueprint(database: DatabaseConnectionController, auth: Authenticator):

    user_blueprint = Blueprint("user", __name__)

    @user_blueprint.route("/")
    @auth(admin_required=True)
    def list_users():
        # YOU MUST BE AN ADMIN TO DO THIS
        return {
            "users": []
        }