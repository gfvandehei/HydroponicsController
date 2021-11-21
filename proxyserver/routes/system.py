from flask.wrappers import Response
import sqlalchemy
from sqlalchemy.sql.expression import false
from hydroserver.controllers.database import DatabaseConnectionController
import hydroserver.model.model as Model
from flask import Blueprint, request
from proxyserver.utils.authentication import Authenticator
from proxyserver.utils.sqlalchemy_funcs import sqlobj_to_json
import requests

def create_system_route(database_manager: DatabaseConnectionController, auth: Authenticator):
    
    system_blueprint = Blueprint("system", __name__)

    @system_blueprint.route("/")
    @auth()
    def list_systems():
        print("SYSTEMS")
        session = database_manager.get_session()
        # get the systems user has access to
        # get system information
        user = session.query(Model.User).filter(Model.User.id==request.user_id).one()
        if user.admin:
            systems = session.query(Model.System).all()
        else:
            systems = session.query(Model.UserPermission)\
                .join(Model.System)\
                    .filter(Model.UserPermission.user_id == request.user_id).all()

        systems_to_json = list(map(lambda x: sqlobj_to_json(x.__dict__), systems))
        session.close()
        return {
            "status": 200,
            "data": systems_to_json
        }
    
    @system_blueprint.route("/<system_id>", methods=["GET"])
    @auth()
    def get_system_information(system_id):
        print("GETTING SYSTEM")
        try:
            auth.check_has_access(request.user_id, int(system_id))
        except Exception as err:
            return Response("User does not have permission to view resource", status=401)
        session = database_manager.get_session()
        # make sure user is authenticated and has access
        system = session.query(Model.System).filter(Model.System.id == int(system_id)).one()
        session.close()
        return {
            "status": 200,
            "data": sqlobj_to_json(system.__dict__)
        }
    
    @system_blueprint.route("/<system_id>/<path:url>", methods=["GET", "POST"])
    @auth()
    def proxy_to_system(system_id, url):
        print("HERE")
        try:
            auth.check_has_access(request.user_id, int(system_id))
        except Exception as err:
            return Response("User does not have permission to view resource", status=401)
        session = database_manager.get_session()
        # check if user can access system
        system = session.query(Model.System).filter(Model.System.id == int(system_id)).one_or_none()
        session.close()
        if system is None:
            return Response("No system found", status=404)
        # make request to system
        print("http://"+system.address+":5000"+"/"+url)
        proxy_response = requests.request(
            method=request.method,
            url=f"http://{system.address}:5000/{url}",
            headers={key: value for (key, value) in request.headers if key != "Host"},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False
        )

        print(proxy_response)

        # send system respose back
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection', "access-control-allow-origin"]
        headers = [(name, value) for (name, value) in proxy_response.raw.headers.items()\
            if name.lower() not in excluded_headers]
        """for i in range(len(headers)):
            if headers[i][0] == "Access-Control-Allow-Origin":
                headers[i] = ("Access-Control-Allow-Origin", "*")
            if headers[i][0] == "Access-Control-Allow-Methods":
                headers[i] = ("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")"""
        print(headers)
        #headers.append(("Access-Control-Allow-Origin","*"))
        #headers.append(("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE"))
        response = Response(proxy_response.content, proxy_response.status_code, headers)
        return response
    
    return system_blueprint