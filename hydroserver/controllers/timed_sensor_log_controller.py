from threading import Thread
from typing import List
from hydroserver.controllers.dht_manager import DHTManager
import time
from libraries.hydroserver_redis.dht_interface import HydroDHTRedisInterface

class TimedDHTLogController(Thread):

    def __init__(self, sensors_manager: DHTManager, interval: int, dht_log: HydroDHTRedisInterface):
        Thread.__init__(self)
        self.sensor_manager = sensors_manager
        self.interval = interval
        self.dht_log = dht_log
    
    def run(self):
        while True:
            self.tick()
            time.sleep(self.interval)
    
    def tick(self):
        """perform a dump of all the data to redis
        """
        for sensor in self.sensor_manager._dht_sensors.values():
            temperature, humidity = sensor.get_values()
            self.dht_log.store_dht_sensor_data(
                sensor.database_object.system_id, 
                sensor.database_object.id,
                temperature,
                humidity
            )
            