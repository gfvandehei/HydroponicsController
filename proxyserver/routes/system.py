from flask.wrappers import Response
from sqlalchemy.sql.expression import false
from hydroserver.controllers.database import DatabaseConnectionController
import hydroserver.model.model as Model
from flask import Blueprint, request
from utils.sqlalchemy_funcs import sqlobj_to_json
import requests

def create_system_route(database_manager: DatabaseConnectionController):
    
    system_blueprint = Blueprint("system", __name__)

    @system_blueprint.route("/")
    def list_systems():
        session = database_manager.get_session()
        # get the systems user has access to
        # get system information
        systems = session.query(Model.System).all()
        systems_to_json = list(map(lambda x: sqlobj_to_json(x.__dict__), systems))
        session.close()
        return {
            "status": 200,
            "data": systems_to_json
        }
    
    @system_blueprint.route("/<system_id>")
    def get_system_information(system_id):
        session = database_manager.get_session()
        # make sure user is authenticated and has access
        system = session.query(Model.System).filter(Model.System.id == int(system_id)).one()
        session.close()
        return {
            "status": 200,
            "data": sqlobj_to_json(system.__dict__)
        }
    
    @system_blueprint.route("/<system_id>/<path:url>")
    def proxy_to_system(system_id, url):
        session = database_manager.get_session()
        # check if user can access system
        system = session.query(Model.System).filter(Model.System.id == int(system_id)).one()
        session.close()
        # make request to system
        proxy_response = requests.request(
            method=request.method,
            url=system.address+"/"+url,
            headers={key: value for (key, value) in request.headers if key != "Host"},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False
        )

        # send system respose back
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in proxy_response.raw.headers.items()\
            if name.lower() not in excluded_headers]
        
        response = Response(proxy_response.content, proxy_response.status_code, headers)
        return response