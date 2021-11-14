from hydroserver.controllers.servomanager import ServoManager
from hydroserver.controllers.database import DatabaseConnectionController
import hydroserver.model.model as Model
from hydroserver.controllers.camera_manager import CameraManager
from hydroserver.physical_interfaces.camera_gimbal_controller import CameraGimbalController
from typing import Dict

class GimbalManager(object):

    def __init__(
        self,
        database_manager: DatabaseConnectionController, 
        camera_manager: CameraManager,
        servo_manager: ServoManager,
        system_id: int):
        """a manager for camera gimbals, camera gimbals are made of 2 servos

        :param database_manager: the object used to get database sessions
        :type database_manager: DatabaseConnectionController
        :param camera_manager: the controller for camera objects
        :type camera_manager: CameraManager
        :param servo_manager: the controller for servo objects
        :type servo_manager: ServoManager
        :param system_id: the system i am running on's id
        :type system_id: int
        """

        self._system = system_id
        self.db = database_manager
        self.camera_manager = camera_manager
        self.servo_manager = servo_manager

        self.gimbals_by_id: Dict[int, CameraGimbalController] = {}

        self.populate_from_database()
        
    def populate_from_database(self):
        """
        get all gimbals from the database, create gimbal objects, and keep track of them
        """
        session = self.db.get_session()
        camera_manager_ids = list(self.camera_manager.cameras.keys())
        gimbals = session.query(Model.CameraGimbal).filter(Model.CameraGimbal.camera_id.in_(camera_manager_ids))
        for gimbal in gimbals:
            servo_x = self.servo_manager.servo_by_id[gimbal.x_servo_id]
            servo_y = self.servo_manager.servo_by_id[gimbal.y_servo_id]
            new_camera_gimbal = CameraGimbalController(servo_y, servo_x)
            self.gimbals_by_id[gimbal.id] = new_camera_gimbal
        session.close()