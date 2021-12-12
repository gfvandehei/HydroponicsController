from hydroserver.controllers.pump_schedule_controller import PumpScheduleController
from hydroserver.model.requests import pump_schedules
from hydroserver.views.dht_blueprint import create_dht_blueprint
from hydroserver.views.pump_schedule_blueprint import create_pump_schedule_blueprint
from hydroserver.views.servo_blueprint import create_servo_blueprint
from gpiozero.pins import Factory
from hydroserver.settings import HydroponicsServerSettings
from threading import Thread
import flask
from flask_cors import CORS
from hydroserver.controllers.database import DatabaseConnectionController
from hydroserver.controllers.camera_store_manager import CameraStoreManager
from hydroserver.controllers.camera_manager import CameraManager
from hydroserver.controllers.pump_manager import PumpManager
from hydroserver.controllers.gimbal_manager import GimbalManager
from hydroserver.controllers.servomanager import ServoManager
from hydroserver.controllers.dht_manager import DHTManager
from gpiozero.pins.pigpio import PiGPIOFactory
from hydroserver.views.camera_blueprint import create_camera_blueprint
from hydroserver.views.pump_blueprint import create_pump_blueprint
from hydroserver.utils.ip_updater import update_ip_address_in_db
from hydroserver.controllers.timed_sensor_log_controller import TimedDHTLogController
from libraries.hydroserver_redis.dht_interface import HydroDHTRedisInterface
import logging
import redis

logging.basicConfig(level=logging.DEBUG)

class HydroponicsServer(Thread):

    def __init__(self, settings: HydroponicsServerSettings):
        Thread.__init__(self)
        self.settings = settings
        self.flask_app = flask.Flask(__name__)
        CORS(self.flask_app)
        self.flask_app.url_map.strict_slashes = False
        # gpiozero conf
        pin_factory = PiGPIOFactory()
        # create controllers
        self.database_controller = DatabaseConnectionController(settings.sql_uri)
        self.camera_store_controller = CameraStoreManager(self.database_controller, settings.system_id)
        self.camera_controller = CameraManager(self.database_controller, self.camera_store_controller, settings.system_id)
        self.pump_controller = PumpManager(self.database_controller, settings.system_id)
        self.servo_controller = ServoManager(self.database_controller, settings.system_id, pin_factory)
        self.gimbal_controller = GimbalManager(self.database_controller, self.camera_controller, self.servo_controller, settings.system_id)
        self.dht_controller = DHTManager(self.database_controller, settings.system_id)
        self.pump_schedule_contrller = PumpScheduleController(self.database_controller, self.pump_controller, settings.system_id)
        
        self.redis_client = redis.Redis(settings.redis_host, settings.redis_port, settings.redis_db)
        self.redis_dht_interface = HydroDHTRedisInterface(self.redis_client)
        self.dht_logging_controller = TimedDHTLogController(self.dht_controller, 60*60, self.redis_dht_interface)

        # any tasks that need to happen do here
        # ip = update_ip_address_in_db(self.database_controller, self.settings.system_id)

        # add views
        self.flask_app.register_blueprint(
            create_camera_blueprint(
                self.camera_controller
            ),
            url_prefix="/camera"
        )
        self.flask_app.register_blueprint(
            create_servo_blueprint(
                self.servo_controller
            ),
            url_prefix="/servo"
        )
        print("/dht")
        self.flask_app.register_blueprint(
            create_dht_blueprint(self.dht_controller),
            url_prefix="/dht"
        )
        self.flask_app.register_blueprint(
            create_pump_blueprint(self.pump_controller),
            url_prefix="/pump"
        )
        self.flask_app.register_blueprint(
            create_pump_schedule_blueprint(
                self.database_controller,
                self.pump_schedule_contrller,
                self.pump_controller
            ),
            url_prefix="/pump_schedule"
        )

        # handle any threaded operations 
        self.pump_schedule_contrller.start() 
        self.dht_logging_controller.start()


    def run(self):
        """
        runs the flask app in its own thread
        """
        self.flask_app.run(
            host=self.settings.host,
            port=self.settings.port
        )
