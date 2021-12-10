import redis

class HydroDHTRedisInterface(object):

    def __init__(self, redis_client: redis.Redis):
        self.client = redis_client
    
    def store_dht_sensor_data(self, system_id, sensor_id, temperature: float, humidity: float):
        key = f"system:{system_id}:sensor:dhtsensor:{sensor_id}"
        self.client.xadd(key, {
            "temperature": temperature,
            "humidity": humidity
        })
    
    def get_dht_sensor_data(self, system_id: int, sensor_id: int, count=10):
        key = f"system:{system_id}:sensor:dhtsensor:{sensor_id}"
        data = self.client.xrange(key, min="+", max="-")
        return data