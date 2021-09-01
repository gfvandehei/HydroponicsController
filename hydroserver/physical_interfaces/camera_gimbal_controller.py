from hydroserver.physical_interfaces.servo_controller import ServoController

class CameraGimbalController(object):

    def __init__(
        self, 
        vertical_servo: ServoController, 
        horizontal_servo: ServoController
        ):

        self.vert = vertical_servo
        self.horz = horizontal_servo
    
    def tilt_up(self):
        self.vert.move_positive()
    
    def tilt_down(self):
        self.vert.move_negative()
    
    def tilt_right(self):
        self.horz.move_positive()
    
    def tile_left(self):
        self.horz.move_negative()

    def set_position(self, x: float, y: float):
        try:
            self.horz.set_value(x)
        except Exception as err:
            pass
        try:
            self.vert.set_value(y)
        except Exception as err:
            pass

    def json(self) -> dict:
        return {
            "vertical": self.vert._servo.value,
            "horizontal": self.vert._servo.value
        }
        

