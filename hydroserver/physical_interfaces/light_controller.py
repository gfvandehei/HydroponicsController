from gpiozero import LED, PWMLED

class LightController(object):

    def __init__(self, pin:int, pmw: bool=False, state: str="OFF"):
        self._state = state
        self._pin = pin
        self._pmw = pmw
        self._brightness = 0
        self._led = PWMLED(self._pin)

    def push_state_to_pin(self):
        if self._state == "ON":
            self._led.on()
            self._led.value = self._brightness
        else:
            self._led.off()
    
    def turn_on(self, brightness=1.0):
        self._state = "ON"
        self._brightness = brightness
        self.push_state_to_pin()
    
    def turn_off(self):
        self._state = "OFF"
        self.push_state_to_pin()
