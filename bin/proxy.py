from proxyserver.proxyserver import ProxyServer
from dotenv import load_dotenv
import os
load_dotenv()

sql_uri = os.getenv("SQL_URI")

proxy_server = ProxyServer(sql_uri)
proxy_server.run()