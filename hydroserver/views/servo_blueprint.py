from hydroserver.controllers.servomanager import ServoManager
from flask import Blueprint, request

def create_servo_blueprint(servo_controller: ServoManager):
    servo_blueprint = Blueprint("servo", __name__)

    @servo_blueprint.route("/", methods=["GET"])
    def list_servos():
        servos_serialized = map(lambda x: x.json(), servo_controller.servo_by_id.values())
        servos_serialized = {}
        for i in servo_controller.servo_by_id:
            servos_serialized[i] = servo_controller.servo_by_id[i].json()
        return {
            "data": servos_serialized,
            "messages": []
        }

    @servo_blueprint.route("/<servo_id>/move", methods=["POST"])
    def move_servo(servo_id):
        body = request.json
        servo = servo_controller.servo_by_id.get(int(servo_id))
        method = body['method']
        value = body["value"]
        if method == "SET":
            servo.set_value(float(value))
        elif method == "ITERATE":
            if float(value) > 0:
                servo.move_positive(float(value))
            else:
                servo.move_positive(float(value))
        return {
            "data": servo.json(),
            "messages": []
        }

    return servo_blueprint