from hydroserver.controllers.dht_manager import DHTManager
from flask import Blueprint, request

def create_dht_blueprint(dht_controller: DHTManager):
    dht_blueprint = Blueprint("dht", __name__)

    @dht_blueprint.route("/")
    def list_dht_sensors():
        dht_controller._dht_sensors
        dht_sensors_serialized = {}
        for (key, value) in dht_controller._dht_sensors.items():
            dht_sensors_serialized[key] = value.json()
        print(dht_sensors_serialized)
        return {
            "data": dht_sensors_serialized,
            "messages": []
        }
    
    return dht_blueprint