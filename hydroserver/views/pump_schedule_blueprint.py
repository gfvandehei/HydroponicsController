from flask.wrappers import Response
from pydantic.error_wrappers import ValidationError
import hydroserver.model.model as Model
from hydroserver.model.requests.pump_schedules import CreateNewPumpScheduleRequest
from hydroserver.controllers.database import DatabaseConnectionController
from hydroserver.physical_interfaces.pump_controller import PumpController
from hydroserver.physical_interfaces.pump_schedule import PumpSchedule
from hydroserver.controllers.pump_schedule_controller import PumpScheduleController
from hydroserver.controllers.pump_manager import PumpManager
from flask import Blueprint, request

def create_pump_schedule_blueprint(
    database: DatabaseConnectionController,
    pump_schedule_controller: PumpScheduleController,
    pump_manager: PumpManager):
    # create blueprint
    pump_schedule_blueprint = Blueprint("pump_schedule", __name__)
    # create routes
    @pump_schedule_blueprint.route("/")
    def list_pump_schedules():
        pump_schedules = list(map(lambda x: x.json(), pump_schedule_controller.pump_schedules.values()))
        return {
            "status": 200,
            "data": pump_schedules
        }

    @pump_schedule_blueprint.route("/", methods=["POST"])
    def create_new_schedule():
        try:
            req = CreateNewPumpScheduleRequest.parse_obj(request.json)
        except ValidationError as err:
            return Response(err.json(), status=500)
        # create new object if request was valid
        session = database.get_session()
        new_schedule_entry = Model.PumpScheduleEntry()
        new_schedule_entry.pump_id = req.pump_id
        new_schedule_entry.action = req.action
        new_schedule_entry.days_active = ",".join(req.days_active)
        new_schedule_entry.times = ",".join(req.times)
        try:
            session.add(new_schedule_entry)
            session.commit()
        except Exception as err:
            return Response(err, status=500)
        session.close()
        # refresh the pump schedule controller
        pump_schedule_controller.populate_from_database()
        return list_pump_schedules()


    return pump_schedule_blueprint