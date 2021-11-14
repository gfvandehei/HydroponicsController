from hydroserver.physical_interfaces.servo_controller import ServoController

class CameraGimbalController(object):

    def __init__(
        self, 
        vertical_servo: ServoController, 
        horizontal_servo: ServoController
        ):
        """an object to link two servos as a x/y gimbal system

        :param vertical_servo: the servo that will control y axis
        :type vertical_servo: ServoController
        :param horizontal_servo: the servo that will control x axis
        :type horizontal_servo: ServoController
        """

        self.vert = vertical_servo
        self.horz = horizontal_servo
    
    # i dont think most of these need descriptions pretty self explanitory
    # they do what they say in the function name
    def tilt_up(self):
        self.vert.move_positive()
    
    def tilt_down(self):
        self.vert.move_negative()
    
    def tilt_right(self):
        self.horz.move_positive()
    
    def tile_left(self):
        self.horz.move_negative()

    def set_position(self, x: float, y: float):
        """sets the position of the gimal to a passed x and y value

        :param x: the value to set the x axis servo
        :type x: float
        :param y: the value to set the y axis servo
        :type y: float
        """
        try:
            self.horz.set_value(x)
        except Exception as err:
            pass
        try:
            self.vert.set_value(y)
        except Exception as err:
            pass

    def json(self) -> dict:
        """serialize this object in a way that can be passed to a web based client

        :return: a dict containing information about the gimbal
        :rtype: dict
        """
        return {
            "vertical": self.vert._servo.value,
            "horizontal": self.vert._servo.value
        }
        

