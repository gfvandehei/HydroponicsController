from jinja2.loaders import ModuleLoader
from proxyserver.utils.authentication import Authenticator
import hydroserver.model.model as Model
from hydroserver.controllers.database import DatabaseConnectionController
from proxyserver.models.auth import LoginRequest, RegisterRequest
from flask import Blueprint, request, Response
import os
import pydantic
import json
import base64


def generate_authentication_blueprint(database: DatabaseConnectionController, auth: Authenticator):

    auth_blueprint = Blueprint("auth", __name__)

    @auth_blueprint.route("/register", methods=["POST"])
    def register_user():
        try:
            body = RegisterRequest.parse_obj(request.json)
        except pydantic.ValidationError as err:
            return Response(err.json(), status=400)
        session = database.get_session()
        new_user_object = Model.User()
        new_user_object.admin = False
        new_user_object.email = body.email
        new_user_object.firstname = body.firstname
        new_user_object.lastname = body.lastname
        new_user_object.username = body.username
        session.add(new_user_object)
        session.commit()
        # generate salt
        salt = os.urandom(32)
        password_hash = auth.hash_password(salt, body.password.encode("utf-8"))
        # generate password hash
        new_user_object.salt = base64.b64encode(salt).decode("utf-8")
        new_user_object.password = base64.b64encode(password_hash).decode("utf-8")
        session.commit()
        result = {
            "token": auth.create_token(new_user_object)
        }
        session.close()
        return result

    @auth_blueprint.route("/login", methods=["POST"])
    def login_user():
        body = LoginRequest.parse_obj(request.json)
        session = database.get_session()
        user = session.query(Model.User).filter(Model.User.email == body.email).one_or_none()
        session.close()
        if user is None:
            return Response("No User was found", status=402)
        # hash password passed
        print(base64.b64decode(user.salt), base64.b64decode(user.password))
        password_hash = auth.hash_password(base64.b64decode(user.salt), body.password.encode("utf-8"))
        print(password_hash)
        if password_hash == base64.b64decode(user.password):
            # user is authenticated return token
            return {
                "token": auth.create_token(user)
            }
        else:
            return Response("Incorrect Password", status=402)

    return auth_blueprint