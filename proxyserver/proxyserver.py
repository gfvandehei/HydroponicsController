from flask import Flask
from flask_cors import CORS
from hydroserver.controllers.database import DatabaseConnectionController
from proxyserver.routes.system import create_system_route

class ProxyServer(object):

    def __init__(self, sql_uri: str):
        self.flask_app = Flask(__name__)
        CORS(self.flask_app)

        self.database_connection = DatabaseConnectionController(sql_uri)

        self.flask_app.register_blueprint(
            create_system_route(self.database_connection),
            url_prefix="/system"
        )

    def run(self):
        print("HydroServer proxy server running on 0.0.0.0:4290")
        self.flask_app.run(
            host="0.0.0.0",
            port="4290"
        )

