from gpiozero import Servo
from gpiozero import Device
from gpiozero.pins.pigpio import PiGPIOFactory
import hydroserver.model.model as Model

class ServoController(object):
    def __init__(self, servo_db_object: Model.Servo, factory=None):
        self._pin = servo_db_object.pin
        self._servo = Servo(self._pin, -1, pin_factory=factory)
        self._servo_model = servo_db_object

    def set_value(self, value: float):
        if value > 1 or value < -1:
            raise Exception("Servo value is not valid")
        
        self._servo.value = value
        return self._servo.value

    def move_positive(self, iteration_step: float=.1):
        if self._servo.value + iteration_step > 1:
            raise Exception("Servo can not move positively further")
        else:
            self._servo.value += iteration_step
        return self._servo.value
    
    def move_negative(self, iteration_step: float=.1):
        if self._servo.value - iteration_step < -1:
            raise Exception("Servo has reached negative limit")

        else:
            self._servo.value -= iteration_step
        return self._servo.value

    def json(self):
        as_dict = self._servo_model.__dict__.copy()
        as_dict['value'] = self._servo.value
        del as_dict["_sa_instance_state"]
        print(as_dict)
        return as_dict