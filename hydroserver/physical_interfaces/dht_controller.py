from typing import Tuple
import hydroserver.model.model as Model
import Adafruit_DHT


class DHTController(object):

    def __init__(self, DHTSensorObject: Model.DHTSensor):
        """a class to control a physical DHT11 or DHT22 sensor

        :param dht_object: The database object used to create this controller
        :dtype Model.DHTSensor
        """
        self.database_object = DHTSensorObject
        self.dht = None
        self.previous_temp = 0.0
        self.previous_hum = 0.0
        """if self.database_object.dht_type == "DHT11":
            self.dht = adafruit_dht.DHT11(board.pin.Pin(int(self.database_object.pin)))
        elif self.database_object.dht_type == "DHT22":
            self.dht = adafruit_dht.DHT22(board.pin.Pin(int(self.database_object.pin)))
        else:
            raise(Exception(f"DHT type {self.database_object.dht_type} does not exist"))
        """
    def get_values(self) -> Tuple[float, float]:
        """retrieves the values from DHT sensor, if there is
        an error retrieving values returns previous value

        :raises error: Any random error dht throws outside of normal bounds
        :return: a tuple where the first value is temperature in farenheit, and
        second is humidity in %/100
        :rtype: Tuple[float, float]
        """
        humidity, temperature = Adafruit_DHT.read_retry(11, self.database_object.pin)

        
        return (temperature, humidity)

    def json(self):
        (temp, hum) = self.get_values()
        return {
            "label": self.database_object.label,
            "pin": self.database_object.pin,
            "temperature": temp*(9/5)+32,
            "humidity": hum,
            "id": self.database_object.id
        }