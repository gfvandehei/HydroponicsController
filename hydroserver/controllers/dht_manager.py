from hydroserver.controllers.database import DatabaseConnectionController
from hydroserver.physical_interfaces.dht_controller import DHTController
from typing import Dict
import hydroserver.model.model as Model
import logging

log = logging.getLogger(__name__)

class DHTManager(object):

    def __init__(self,
        database_manager: DatabaseConnectionController, 
        system_id: int):
        self._system = system_id
        self._database = database_manager
        self._dht_sensors: Dict[int, DHTController] = {}
        self.populate_from_database()
        
    def populate_from_database(self):
        session = self._database.get_session()
        dht_sensors = session.query(Model.DHTSensor).filter(Model.DHTSensor.system_id==self._system).all()
        for sensor in dht_sensors:
            new_sensor_object = DHTController(sensor)
            self._dht_sensors[sensor.id] = new_sensor_object
        log.debug(f"Loaded {len(dht_sensors)} dht sensors")
        session.close()
