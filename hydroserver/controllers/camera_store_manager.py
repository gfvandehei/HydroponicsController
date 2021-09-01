from hydroserver.controllers.database import DatabaseConnectionController
import hydroserver.model.model as Model
from typing import Dict
from hydroserver.physical_interfaces.camera_storage import CameraStore

class CameraStoreManager(object):

    def __init__(self, database: DatabaseConnectionController, system_id: int):
        self.db = database
        self.system = system_id
        self.camera_stores_by_id: Dict[int, CameraStore]  = {}

        self.populate_from_database()

    def populate_from_database(self):
        session = self.db.get_session()
        camera_stores = session.query(Model.CameraStore).filter(Model.CameraStore.system_id==self.system).all()
        for store in camera_stores:
            # create all camera stores
            new_camera_store = CameraStore(store.fs_path, store.image_save_time)
            self.camera_stores_by_id[store.id] = new_camera_store
        session.close()

    def get_camera_store(self, id: int):
        return self.camera_stores_by_id.get(id)