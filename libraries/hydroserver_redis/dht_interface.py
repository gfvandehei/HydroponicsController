import redis
from typing import Any, Dict

def dht_redis_dict_to_json(redis_dict: Dict[bytes, Any]):
    new_dict = {}
    for key in redis_dict:
        str_key = key.decode("utf-8")
        new_dict[str_key] = float(redis_dict[key].decode("utf-8"))
    return new_dict

class HydroDHTRedisInterface(object):

    def __init__(self, redis_client: redis.Redis):
        self.client = redis_client
    
    def store_dht_sensor_data(self, system_id, sensor_id, temperature: float, humidity: float):
        key = f"system:{system_id}:sensor:dhtsensor:{sensor_id}"
        self.client.xadd(key, {
            "temperature": temperature,
            "humidity": humidity
        })
    
    def get_dht_sensor_data(self, system_id: int, sensor_id: int, count=10, reversed=False):
        key = f"system:{system_id}:sensor:dhtsensor:{sensor_id}"
        if reversed:
            data = self.client.xrevrange(key, count=count)
        else:
            data = self.client.xrange(key, count=count)
        # take all the keys out of the data
        values = map(lambda x: dht_redis_dict_to_json(x[1]), data)
        return values