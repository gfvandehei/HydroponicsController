from typing import Dict
from hydroserver.controllers.database import DatabaseConnectionController
from hydroserver.physical_interfaces.pump_controller import PumpController
import hydroserver.model.model as Model
import logging

log = logging.getLogger(__name__)

class PumpManager(object):

    def __init__(self, database: DatabaseConnectionController, system_id: int):
        """a class to manage pumps (like for liquid)

        :param database: an object used to get sessions from the database
        :type database: DatabaseConnectionController
        :param system_id: the id of the system I am running on
        :type system_id: int
        """
        self.db = database
        self.system = system_id
        self.pumps: Dict[int, PumpController] = {}
        self.populate_from_db()

    def populate_from_db(self):
        """get all pump configuration for the system from the database, create individual pump
        controllers, and add them to a queryable data structure Dict
        """
        session = self.db.get_session()
        pumps = session.query(Model.Pump).filter(Model.Pump.system_id == self.system).all()
        for pump in pumps:
            new_pump_controller = PumpController(
                pump
            )
            self.pumps[pump.id] = new_pump_controller
        log.debug(f"Created {len(self.pumps)} pumps from database")
        session.close()