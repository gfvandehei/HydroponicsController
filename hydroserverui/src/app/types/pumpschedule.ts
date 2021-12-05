export const DayCodes = ["M", "T", "W", "TH", "F", "S", "SU"]

export interface IPumpSchedule{
    id: number
    action: string
    pump_id: number
    //system_id = Column(Integer, ForeignKey("systems.id")) # this could optimize queries but I dont think it will be a realistic use case subquery will slow enough
    days_active: Array<string> //M,T,W,TH,F,S,SU
    times: Array<string>// datetime.time iso string delimited by commas
}