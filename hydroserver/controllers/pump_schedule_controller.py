from datetime import datetime
from hydroserver.physical_interfaces.pump_controller import PumpController
from hydroserver.controllers.pump_manager import PumpManager
from hydroserver.controllers.database import DatabaseConnectionController
import hydroserver.model.model as Model
from typing import Dict, Any
from threading import Thread
import logging
import time

log = logging.getLogger(__name__)


class PumpScheduleController(Thread):
    
    def __init__(
        self,
        database: DatabaseConnectionController, 
        pump_manager: PumpManager,
        system_id: int):

        self.db = database
        self._pumps = pump_manager
        self.system = system_id
        self.pump_schedules: Dict[int, Any] = {}

    def populate_from_database(self):
        session = self.db.get_session()
        current_pump_ids = set(self._pumps.pumps.keys())
        pump_schedule_entries = session.query(Model.PumpScheduleEntry).filter(Model.PumpScheduleEntry.pump_id.in_(current_pump_ids)).all()
        for entry in pump_schedule_entries:
            new_pump_schedule = None
            self.pump_schedules[entry.id] = new_pump_schedule
        log.debug(f"Created {len(self.pumps)} pumps from database")
        session.close()

    def run(self):
        while True:
            current_time = datetime.now()
            for 
            time.sleep(30)