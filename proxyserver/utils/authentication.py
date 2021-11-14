import hydroserver.model.model as Model
from hydroserver.controllers.database import DatabaseConnectionController
import datetime
import jwt
from flask import Request, Response, request
from functools import wraps


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

    def decode_token(self, token: str) -> int:
        payload = jwt.decode(token, self.secret)
        return payload['sub'] # the user id

    def __call__(self, admin_required=False):
        def _request_wrapper(f):
            @wraps(f)
            def __request_wrapper(*args, **kwargs):
                if request.headers.get("auth_token") is None:
                    # jwt did not exist
                    print("NO JWT")
                    return Response(status=401)
                else:
                    # check if token is valid
                    token = request.headers['auth_token']
                    try:
                        user_id = self.decode_token(token)
                    except Exception as err:
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
                    return f(*args, **kwargs)
