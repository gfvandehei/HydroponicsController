from flask.wrappers import Response
from pydantic.error_wrappers import ValidationError
import hydroserver.model.model as Model
from hydroserver.model.requests.pump_schedules import CreateNewPumpScheduleRequest, UpdatePumpScheduleRequest
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

    @pump_schedule_blueprint.route("/<pump_id>", methods=["GET"])
    def get_schedules_for_pump(pump_id: str):
        print("getting schedules for pump")
        pump_id = int(pump_id)
        pump_schedule_controller.populate_from_database()
        print(pump_schedule_controller.pump_schedules.values())
        for_pump = filter(lambda sched_obj: sched_obj.pump_schedule.pump_id == pump_id, pump_schedule_controller.pump_schedules.values())
        print(for_pump)
        serialized = list(map(lambda x: x.json(), for_pump))
        return {
            "status": 200,
            "data": serialized
        }
    
    @pump_schedule_blueprint.route("/<pump_id>", methods=["DELETE"])
    def delete_all_schedules_for_pump(pump_id: str):
        pump_id = int(pump_id)
        session = database.get_session()
        pump_schedules = session.query(Model.PumpScheduleEntry).filter(Model.PumpScheduleEntry.pump_id == pump_id).all()
        for sched in pump_schedules:
            session.delete(sched)
        session.commit()
        session.close()
        return get_schedules_for_pump(pump_id)
    
    @pump_schedule_blueprint.route("/<pump_id>/<schedule_id>", methods=["DELETE"])
    def delete_schedule_for_pump(pump_id, schedule_id):
        pump_id = int(pump_id)
        schedule_id = int(schedule_id)
        session = database.get_session()
        pump_schedule = session.query(Model.PumpScheduleEntry).filter(Model.PumpScheduleEntry.id == schedule_id).one()
        session.delete(pump_schedule)
        session.commit()
        session.close()
        return get_schedules_for_pump(pump_id)
    
    @pump_schedule_blueprint.route("/<pump_id>/<schedule_id>", methods=["POST"])
    def update_schedule(pump_id, schedule_id):
        schedule_id = int(schedule_id)
        pump_id = int(pump_id)
        body = UpdatePumpScheduleRequest.parse_obj(request.json)
        session = database.get_session()
        schedule = session.query(Model.PumpScheduleEntry).filter(Model.PumpScheduleEntry.id == schedule_id).one()
        schedule.action = body.action
        schedule.days_active = ",".join(body.days_active)
        schedule.times = ",".join(body.times)
        session.commit()
        session.close()
        return get_schedules_for_pump(pump_id)

    return pump_schedule_blueprint