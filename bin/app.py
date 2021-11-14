from hydroserver.server import HydroponicsServer, HydroponicsServerSettings

from dotenv import load_dotenv
load_dotenv()
import os

settings = HydroponicsServerSettings.construct()
settings.system_id = os.getenv("SYSTEM_ID")
settings.port = os.getenv("PORT")
settings.host = os.getenv("HOST")
settings.sql_uri = os.getenv("SQL_URI")
HydroponicsServerSettings.validate(settings)
print(settings)
server = HydroponicsServer(settings)
server.start()