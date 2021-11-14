from gpiozero.pins.pigpio import PiGPIOFactory
from hydroserver.physical_interfaces.servo_controller import ServoController

factory = PiGPIOFactory()
servo = ServoController(27, factory)

while True:
    print(servo._servo.value)
    value = float(input("value:"))
    servo.set_value(value)