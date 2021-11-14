from hydroserver.model.model import Pump
from flask import Blueprint, request
from hydroserver.controllers.pump_manager import PumpManager

def create_pump_blueprint(pump_manager: PumpManager):

    pump_blueprint = Blueprint("pump", __name__)

    @pump_blueprint.route("/")
    def list_pumps():
        pumps_jsonified = []
        for pump in pump_manager.pumps.values():
            pumps_jsonified.append(pump.json())
            #pumps_jsonified[pump.pump.id] = pump.json()
        
        return {
            "data": pumps_jsonified,
            "messages": []
        }

    @pump_blueprint.route("/<pump_id>")
    def get_pump(pump_id): 
        return {
            "data": pump_manager.pumps[int(pump_id)].json(),
            "messages": []
        }

    @pump_blueprint.route("/<pump_id>/pump", methods=["POST"])
    def start_pump(pump_id):
        pump_manager.pumps[int(pump_id)].fill()
        return {
            "data": pump_manager.pumps[int(pump_id)].json(),
            "messages": []
        }
    
    return pump_blueprint
