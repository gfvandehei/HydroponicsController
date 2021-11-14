from hydroserver.controllers.database import DatabaseConnectionController
import hydroserver.model.model as Model
from typing import Dict
from hydroserver.physical_interfaces.camera_storage import CameraStore

class CameraStoreManager(object):

    def __init__(self, database: DatabaseConnectionController, system_id: int):
        """the controller for photo storage directories

        :param database: the object we will use to get database sessions
        :type database: DatabaseConnectionController
        :param system_id: the id of the system I am running on
        :type system_id: int
        """
        self.db = database
        self.system = system_id
        self.camera_stores_by_id: Dict[int, CameraStore]  = {}

        self.populate_from_database()

    def populate_from_database(self):
        """gets all camerastore objects related to the system, initializes each actual store from the
        config information in the database
        """
        session = self.db.get_session()
        camera_stores = session.query(Model.CameraStore).filter(Model.CameraStore.system_id==self.system).all()
        for store in camera_stores:
            # create all camera stores
            new_camera_store = CameraStore(store.fs_path, store.image_save_time)
            self.camera_stores_by_id[store.id] = new_camera_store
        session.close()

    def get_camera_store(self, id: int) -> CameraStore:
        """a function to retrieve a camera store by id, did this because i thought I was
        going to be good about making things private but decided it was easier to not

        :param id: the id of the camera store
        :type id: int
        :return: the camera store object identified by id
        :rtype: int
        """
        return self.camera_stores_by_id.get(id)