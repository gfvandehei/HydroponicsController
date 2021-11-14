from typing import Dict
from hydroserver.controllers.database import DatabaseConnectionController
import hydroserver.model.model as Model
from hydroserver.physical_interfaces.servo_controller import ServoController
import logging

log = logging.getLogger(__name__)

class ServoManager(object):
    def __init__(self, database: DatabaseConnectionController, system_id: int, pin_factory=None):
        """an object to initialize and store a map of system servo objects

        :param database: the object used to get database sessions
        :type database: DatabaseConnectionController
        :param system_id: the id of the system we are in
        :type system_id: int
        :param pin_factory: the factory used to interface with servos, i think right now i use pigpio, defaults to None
        :type pin_factory: raspberry pi pin factory, optional
        """
        self.db = database
        self.system = system_id
        self.pin_factory = pin_factory
        self.servo_by_id: Dict[int, ServoController] = {}

        self.populate_from_database()

    def populate_from_database(self):
        session = self.db.get_session()
        servos = session.query(Model.Servo).filter(Model.Servo.system_id==self.system).all()
        for servo in servos:
            new_servo_controller = ServoController(servo, factory=self.pin_factory)
            self.servo_by_id[servo.id] = new_servo_controller
        session.close()
        log.debug(f'Created {len(self.servo_by_id)} servos from the database')