from gpiozero import Servo
from gpiozero import Device
from gpiozero.pins.pigpio import PiGPIOFactory

class ServoController(object):
    def __init__(self, servo_pin: int, factory=None):
        self._pin = servo_pin
        self._servo = Servo(self._pin, -1, pin_factory=factory)

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
        return {
            "pin": self._pin,
            "value": self._servo.value
        }