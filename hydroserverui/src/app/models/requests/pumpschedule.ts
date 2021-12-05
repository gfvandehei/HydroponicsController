export interface CreateNewPumpScheduleRequest{
    action: string
    pump_id: number
    days_active: Array<string>
    times: Array<string>
}