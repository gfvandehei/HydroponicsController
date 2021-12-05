import pydantic
from typing import List


class CreateNewPumpScheduleRequest(pydantic.BaseModel):
    """Object to describe a request to create a new pump schedule object
    used to validate http request body
    """
    action: str
    pump_id: int
    #system_id = Column(Integer, ForeignKey("systems.id")) # this could optimize queries but I dont think it will be a realistic use case subquery will slow enough
    days_active: List[str] #M,T,W,TH,F,S,SU
    times: List[str] # datetime iso string delimited by commas

class UpdatePumpScheduleRequest(pydantic.BaseModel):
    id: int
    action: str
    days_active: List[str]
    times: List[str]