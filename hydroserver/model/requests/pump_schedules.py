import pydantic
from typing import List

class CreateNewPumpScheduleRequest(pydantic.BaseModel):
    action: str
    pump_id: int
    #system_id = Column(Integer, ForeignKey("systems.id")) # this could optimize queries but I dont think it will be a realistic use case subquery will slow enough
    days_active: List[str] #M,T,W,TH,F,S,SU
    times: List[str] # datetime iso string delimited by commas