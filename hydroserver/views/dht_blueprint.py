from hydroserver.controllers.dht_manager import DHTManager
from flask import Blueprint, request
from libraries.hydroserver_redis.dht_interface import HydroDHTRedisInterface

def create_dht_blueprint(
    dht_controller: DHTManager,
    dht_redis_interface: HydroDHTRedisInterface):
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

    @dht_blueprint.route("/<dht_id>")
    def dht_sensor(dht_id):
        dht_id = int(dht_id)
        sensor = dht_controller._dht_sensors[dht_id]
        
        return {
            "data": sensor.json(),
            "messages": []
        }
    
    @dht_blueprint.route("/<dht_id>/log", methods=["GET"])
    def get_sensor_log(dht_id: str):
        dht_id = int(dht_id)
        dht_sensor = dht_controller._dht_sensors.get(dht_id)
        system_id = dht_sensor.database_object.system_id
        dht_sensor_log = dht_redis_interface.get_dht_sensor_data(system_id, dht_sensor.database_object.id, 100)
        return {
            "data": list(dht_sensor_log),
            "messages": []
        }
    
    return dht_blueprint