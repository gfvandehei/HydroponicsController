from hydroserver.controllers.database import DatabaseConnectionController
import hydroserver.model.model as Model
import socket
import logging

log = logging.getLogger(__name__)

def update_ip_address_in_db(
    database_manager: DatabaseConnectionController,
    system_id: int):

    my_hostname = socket.gethostname()
    my_ip_address = socket.gethostbyname(my_hostname)
    log.info(f"IP Address: {my_ip_address}")

    session = database_manager.get_session()
    system_obj = session.query(Model.System).filter(Model.System.id == system_id).one()
    if system_obj.address != my_ip_address:
        # we need to update the ip
        system_obj.address = my_ip_address
        session.commit()
        log.info(f"Updated IP in database to {my_ip_address}")
    session.close()
    return my_ip_address


