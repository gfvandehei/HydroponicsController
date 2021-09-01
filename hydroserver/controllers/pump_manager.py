from hydroserver.controllers.database import DatabaseConnectionController
from hydroserver.physical_interfaces.pump_controller import PumpController
import hydroserver.model.model as Model

class PumpManager(object):

    def __init__(self, database: DatabaseConnectionController, system_id: int):
        self.db = database
        self.system = system_id
        self.pumps = {}
        self.populate_from_db()

    def populate_from_db(self):
        session = self.db.get_session()
        pumps = session.query(Model.Pump).filter(Model.Pump.system_id == self.system).all()
        for pump in pumps:
            new_pump_controller = PumpController(
                pump.pin,
                pump.time_to_fill
            )
            self.pumps[pump.id] = new_pump_controller
        
        session.close()