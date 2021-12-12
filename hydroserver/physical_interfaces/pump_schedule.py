import hydroserver.model.model as Model
from hydroserver.physical_interfaces.pump_controller import PumpController
import datetime

days = ["M", "T", "W", "TH", "F", "S", "SU"]

class PumpSchedule(object):

    def __init__(
        self, 
        pump_schedule: Model.PumpScheduleEntry, 
        pump_controller: PumpController):

        self.pump_schedule = pump_schedule
        self.pump = pump_controller

        # determine datetimes i should run
        self.run_days = set(self.pump_schedule.days_active.split(","))
        # determin days I should run
        def to_time(isostring: str) -> datetime.time:
            try:
                iso = datetime.time.fromisoformat(isostring)
                return iso
            except Exception as err:
                return datetime.time(hour=0, minute=0)
            return datetime.time.fromisoformat(isostring)
        
        if len(self.pump_schedule.times) == 0:
            self.times_to_run = []
        else:
            print(self.pump_schedule.times)
            isostrings_to_run = self.pump_schedule.times.split(",")
            self.times_to_run = list(map(to_time, isostrings_to_run))


    
    def check(self, current_time: datetime.time=None):
        if current_time is None:
            current_time = datetime.datetime.now().time()
        
        if self.pump.pump_state == "WAITING":
            # check if time is good
            for i in self.times_to_run:
                if i.hour == current_time.hour and i.minute == current_time.minute:
                    return True
        return False

    def check_day(self, current_day: datetime.date=None):
        
        if current_day is None:
            current_day = datetime.datetime.now().date()
        
        day_code = days[current_day.weekday()]

        return day_code in self.run_days

    def json(self):
        as_dict = self.pump_schedule.__dict__.copy()
        del as_dict["_sa_instance_state"]
        time_to_array = self.pump_schedule.times.split(",")
        day_to_array = self.pump_schedule.days_active.split(",")
        as_dict['times'] = time_to_array
        as_dict["days_active"] = day_to_array
        return as_dict