from typing import Dict
from hydroserver.physical_interfaces.camera_streamer import CameraStreamer
from hydroserver.physical_interfaces.camera_storage import CameraStore
from hydroserver.controllers.database import DatabaseConnectionController
import hydroserver.model.model as Model
from hydroserver.physical_interfaces.camera_controller import CameraController
from hydroserver.controllers.camera_store_manager import CameraStoreManager
import logging

log = logging.getLogger(__name__)

class CameraManager(object):

    def __init__(
        self, 
        database: DatabaseConnectionController, 
        camera_stores: CameraStoreManager,
        system_id: int):
        """an object used to provide an interface for views to query physical cameras,
        as well as initialize cameras from the database

        :param database: the object we will be using to create database sessions
        :type database: DatabaseConnectionController
        :param camera_stores: the controller object for photo storage operations
        :type camera_stores: CameraStoreManager
        :param system_id: the numeric ID of the system I am running on
        :type system_id: int
        """
        self.db = database
        self.system_id = system_id
        self.camera_store_manager = camera_stores

        self.cameras: Dict[int, CameraController] = {}
        self.populate_from_database()

    def populate_from_database(self):
        """get all information about cameras for the system, create physical camera objects
        and place them into a dict so I can access them by id
        """
        session = self.db.get_session()
        cameras = session.query(Model.Camera).filter(Model.Camera.system_id == self.system_id).all()
        for camera in cameras:
            # create actual camera object and start operation
            camera_store = self.camera_store_manager.get_camera_store(camera.camera_store_id)
            camera_stream = CameraStreamer()
            new_camera_controller = CameraController(
                camera_store,
                camera_stream,
                camera
            )
            self.cameras[camera.id] = new_camera_controller
            new_camera_controller.start()
        log.debug(f"Created {len(self.cameras)} cameras from the database")
        session.close()
