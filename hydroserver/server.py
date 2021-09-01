from hydroserver.settings import HydroponicsServerSettings
from threading import Thread
import flask
from hydroserver.controllers.database import DatabaseConnectionController
from hydroserver.controllers.camera_store_manager import CameraStoreManager
from hydroserver.controllers.camera_manager import CameraManager
from hydroserver.controllers.pump_manager import PumpManager
from hydroserver.controllers.gimbal_manager import GimbalManager
from hydroserver.controllers.servomanager import ServoManager

from hydroserver.views.camera_blueprint import create_camera_blueprint
import logging
logging.basicConfig(level=logging.DEBUG)

class HydroponicsServer(Thread):

    def __init__(self, settings: HydroponicsServerSettings):
        Thread.__init__(self)
        self.settings = settings
        self.flask_app = flask.Flask(__name__)
        
        # create controllers
        self.database_controller = DatabaseConnectionController(settings.sql_uri)
        self.camera_store_controller = CameraStoreManager(self.database_controller, settings.system_id)
        self.camera_controller = CameraManager(self.database_controller, self.camera_store_controller, settings.system_id)
        self.pump_controller = PumpManager(self.database_controller, settings.system_id)
        self.servo_controller = ServoManager(self.database_controller, settings.system_id)
        self.gimbal_controller = GimbalManager(self.database_controller, self.camera_controller, self.servo_controller, settings.system_id)
        
        # add views
        self.flask_app.register_blueprint(
            create_camera_blueprint(
                self.camera_controller
            ),
            url_prefix="/camera"
        )


    def run(self):
        """
        runs the flask app in its own thread
        """
        self.flask_app.run(
            host=self.settings.host,
            port=self.settings.port
        )
