import logging
import RPi.GPIO as GPIO
from threading import Timer

class PumpController(object):
    """
    manages a one way pump controlled via 1 pin
    """
    def __init__(
        self, 
        pump_pin:int, 
        time_to_fill:int, 
        pump_state: str="WAITING",
        logger: logging.Logger=logging.getLogger(__name__)):
        """
        constructor

        Keyword arguments:
        pump_pin -- the pin the pump is controlled through
        time_to_fill -- the amount of time in seconds it takes to fill the reservior
        pump_state -- the initial state of the pump, defaults to waiting
        """
        self.pump_state = pump_state
        self.pump_pin = pump_pin
        self.ttf = time_to_fill
        self.log = logger
        self.active_timer = None
    
    def fill(self):
        """
        fills the reservior with water for a set amount of time
        """
        if self.pump_state == "WAITING":
            self.pump_state = "FILLING"
            self.log.info("Switched to state filling")
            GPIO.output(self.pump_pin, 1)
            self.active_timer = Timer(self.ttf, lambda: self.drain())
            self.active_timer.start()
        else:
            raise(Exception("Pump is in incorrect state, to fill pump needs to be waiting"))

    def drain(self):
        """
        turns off the pump, allowing the reservior to drain (reservior auto drains)
        """
        self.pump_state = "DRAINING"
        self.log.info("Switched to state draining")
        GPIO.output(self.pump_pin, 0)
        self.active_timer = Timer(self.ttf, lambda: self.wait())
        self.active_timer.start()

    def wait(self):
        """
        sets the state to 'waiting' switches pump off if not already done so
        """
        self.pump_state = "WAITING"
        self.log.info("Switched to state waiting")
        GPIO.output(self.pump_pin, 0)
        #GPIO.output(drain_pin, 0)
        self.active_timer = None

    def json(self):
        return {
            "state": self.pump_state,
            "pin": self.pump_pin,
            "time_to_fill": self.ttf
        }