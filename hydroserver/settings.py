from pydantic import BaseModel

class HydroponicsServerSettings(BaseModel):
    host: str
    port: int
    system_id: int
    sql_uri: str

