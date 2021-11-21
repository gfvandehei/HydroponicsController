from flask import Flask
from flask_cors import CORS
from hydroserver.controllers.database import DatabaseConnectionController
from proxyserver.routes.authentication import generate_authentication_blueprint

from proxyserver.utils.authentication import Authenticator
from proxyserver.routes.system import create_system_route
from proxyserver.routes.test_routes import generate_test_routes

import hydroserver.model.model as Model

class ProxyServer(object):

    def __init__(self, sql_uri: str):
        self.flask_app = Flask(__name__)
        CORS(self.flask_app)
        self.flask_app.url_map.strict_slashes = False

        self.database_connection = DatabaseConnectionController(sql_uri)
        self.auth = Authenticator(self.database_connection, "MYSECRET")

        self.flask_app.register_blueprint(
            create_system_route(self.database_connection, self.auth),
            url_prefix="/system"
        )
        self.flask_app.register_blueprint(
            generate_authentication_blueprint(self.database_connection, self.auth),
            url_prefix="/auth"
        )

    def run(self):
        print("HydroServer proxy server running on 0.0.0.0:4290")
        self.flask_app.run(
            host="0.0.0.0",
            port="4290"
        )

    

