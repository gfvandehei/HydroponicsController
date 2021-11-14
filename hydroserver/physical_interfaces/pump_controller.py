import logging
#import RPi.GPIO as GPIO
from threading import Timer
import gpiozero
import hydroserver.model.model as Model


class PumpController(object):
    """
    manages a one way pump controlled via 1 pin
    """
    def __init__(
        self, 
        pump: Model.Pump,
        pump_state: str="WAITING",
        logger: logging.Logger=logging.getLogger(__name__)):
        """
        constructor

        Keyword arguments:
        pump_pin -- the pin the pump is controlled through
        time_to_fill -- the amount of time in seconds it takes to fill the reservior
        pump_state -- the initial state of the pump, defaults to waiting
        """
        self.pump = pump
        self.pump_state = pump_state
        self.pump_pin = pump.pin
        self.ttf = pump.time_to_fill
        self.log = logger
        self.active_timer = None
        self.digital_device = gpiozero.LED(self.pump_pin)
        self.digital_device.off()
        #gpiozero.DigitalOutputDevice(self.pump_pin)
    
    def fill(self):
        """
        fills the reservior with water for a set amount of time
        """
        if self.pump_state == "WAITING":
            self.pump_state = "FILLING"
            self.log.info("Switched to state filling")
            self.digital_device.on()
            #GPIO.output(self.pump_pin, 1)
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
        self.digital_device.off()
        #GPIO.output(self.pump_pin, 0)
        self.active_timer = Timer(self.ttf, lambda: self.wait())
        self.active_timer.start()

    def wait(self):
        """
        sets the state to 'waiting' switches pump off if not already done so
        """
        self.pump_state = "WAITING"
        self.log.info("Switched to state waiting")
        self.digital_device.off()
        ##GPIO.output(self.pump_pin, 0)
        #GPIO.output(drain_pin, 0)
        self.active_timer = None

    def json(self):
        as_dict = self.pump.__dict__.copy()
        del as_dict["_sa_instance_state"]
        as_dict['state'] = self.pump_state
        return as_dict