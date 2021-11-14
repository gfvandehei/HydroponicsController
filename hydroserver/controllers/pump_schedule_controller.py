from datetime import datetime
from hydroserver.physical_interfaces.pump_controller import PumpController
from hydroserver.controllers.pump_manager import PumpManager
from hydroserver.controllers.database import DatabaseConnectionController
import hydroserver.model.model as Model
from typing import Dict, Any
from threading import Thread
import logging
import time
from hydroserver.physical_interfaces.pump_schedule import PumpSchedule

log = logging.getLogger(__name__)


class PumpScheduleController(Thread):
    
    def __init__(
        self,
        database: DatabaseConnectionController, 
        pump_manager: PumpManager,
        system_id: int):
        """a class to manage and run all schedules for pumps, checks if a schedule is active twice a minute
        schedules can only be made to the minute

        :param database: an object used to get database sessions
        :type database: DatabaseConnectionController
        :param pump_manager: the class managing all pumps
        :type pump_manager: PumpManager
        :param system_id: the id of the system I am running on
        :type system_id: int
        """
        Thread.__init__(self)
        self.db = database
        self._pumps = pump_manager
        self.system = system_id
        self.pump_schedules: Dict[int, PumpSchedule] = {}
        self.populate_from_database()

    def populate_from_database(self):
        """gets all pump schedules for the system from the database, creates pump schedule objects from 
        the information, and adds all pump schedule objects to a dict by id
        """
        session = self.db.get_session()
        current_pump_ids = set(self._pumps.pumps.keys())
        pump_schedule_entries = session.query(Model.PumpScheduleEntry).filter(Model.PumpScheduleEntry.pump_id.in_(current_pump_ids)).all()
        for entry in pump_schedule_entries:
            new_pump_schedule = PumpSchedule(entry, self._pumps.pumps.get(entry.pump_id))
            self.pump_schedules[entry.id] = new_pump_schedule
        log.debug(f"Created {len(self.pump_schedules)} pumps from database")
        session.close()

    def run(self):
        """checks if we should trigger any pumps based on the schedules
        twice a minute (so we make sure we hit every minute at least once)
        """
        while True:
            current_time = datetime.now()
            # check every pump schedule is the right day and time
            for schedule in self.pump_schedules.values():
                if schedule.check_day(current_time.date()) and schedule.check(current_time.time()):
                    schedule.pump.fill()
            # setting for 30 seconds makes sure we get every single minute
            time.sleep(30)