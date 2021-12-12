from hydroserver.server import HydroponicsServer, HydroponicsServerSettings

from dotenv import load_dotenv
load_dotenv()
import os

settings = HydroponicsServerSettings.construct()
settings.system_id = os.getenv("SYSTEM_ID")
settings.port = os.getenv("PORT")
settings.host = os.getenv("HOST")
settings.sql_uri = os.getenv("SQL_URI")
settings.redis_host = os.getenv("REDIS_HOST")
settings.redis_port = int(os.getenv("REDIS_PORT", 6379))
settings.redis_db = int(os.getenv("REDIS_DB", 0))

HydroponicsServerSettings.validate(settings)
print(settings)
server = HydroponicsServer(settings)
server.start()