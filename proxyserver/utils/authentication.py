import hydroserver.model.model as Model
from hydroserver.controllers.database import DatabaseConnectionController
import datetime
import jwt
from flask import Request, Response, request
from functools import wraps
import hashlib
from typing import Tuple

class Authenticator(object):

    def __init__(self, database: DatabaseConnectionController, secret: str):
        self.database = database
        self.secret = secret

    def create_token(self, user: Model.User):
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=10, seconds=0),
            'iat': datetime.datetime.utcnow(),
            'sub': user.id
        }
        return jwt.encode(
            payload,
            self.secret,
            algorithm="HS256"
        )

    def decode_token(self, token: str) -> Tuple[int, datetime.datetime]:
        print("TOKEN", token)
        payload = jwt.decode(token, self.secret, ["HS256"])
        #print(datetime.datetime.fromtimestamp(payload['exp']))
        return payload['sub'], datetime.datetime.fromtimestamp(payload['exp']) # the user id

    def hash_password(self, salt, password):
        key = hashlib.pbkdf2_hmac(
            'sha256', # The hash digest algorithm for HMAC
            password, # Convert the password to bytes
            salt, # Provide the salt
            100000 # It is recommended to use at least 100,000 iterations of SHA-256 
        )
        return key
    
    def __call__(self, admin_required=False):
        print("HEREERER")
        def _request_wrapper(f):
            @wraps(f)
            def __request_wrapper(*args, **kwargs):
                print("AUTH")
                needs_refresh = False
                if request.headers.get("auth_token") is None:
                    # jwt did not exist
                    print("NO JWT")
                    return Response(status=401)
                else:
                    # check if token is valid
                    token = request.headers['auth_token']
                    try:
                        user_id, exp_time = self.decode_token(token)
                        current_time = datetime.datetime.now()
                        if exp_time - datetime.timedelta(minutes=1) < current_time:
                            # we need to make refresh roken
                            needs_refresh = True
                    except Exception as err:
                        print(err)
                        print("Couldnt decode JWT")
                        return Response(status=401)
                    request.user_id = user_id
                    if admin_required:
                        # check if user is admin
                        session = self.database.get_session()
                        user = session.query(Model.User).filter(Model.User.id == user_id).one()
                        session.close()
                        if not user.admin:
                            print("User not admin")
                            return Response(status=401)
                    if needs_refresh:
                        print("Refreshing token")
                        session = self.database.get_session()
                        user = session.query(Model.User).filter(Model.User.id == user_id).one()
                        session.close()
                        new_token = self.create_token(user)
                        response = f(*args, **kwargs)
                        if type(response) == Response:
                            response.headers.add("refresh-token", new_token)
                            return response
                        else:
                            Response(response, headers=[("refresh-token", new_token)])
                    return f(*args, **kwargs)
            __request_wrapper.__name__ = f.__name__
            return __request_wrapper
        return _request_wrapper

    def check_has_access(self, user_id: int, system_id: int):
        session = self.database.get_session()
        user = session.query(Model.User).filter(Model.User.id == user_id).one()
        if(user.admin):
            session.close()
            return
        session.query(Model.UserPermission).filter(Model.UserPermission.user_id==user_id and Model.UserPermission.system==system_id).one()
        session.close()
        