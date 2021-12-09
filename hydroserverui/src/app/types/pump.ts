import { HttpClient } from "@angular/common/http";
import { environment } from "src/environments/environment";
import { APIBaseResponse } from "../models/api";
import { SystemObject } from "../models/system";
import {IPumpSchedule} from "../types/pumpschedule";

export interface Pump{
    id: number
    label: string
    system_id: number
    state: string
    pin: number
    time_to_fill: number
}

export class PumpWrapper{
    pump: Pump;
    system: SystemObject;
    http: HttpClient;
    schedules: Array<IPumpSchedule> = [];

    constructor(pumpInterface: Pump, system: SystemObject, http: HttpClient){
        this.system = system;
        this.pump = pumpInterface;
        this.http = http;
        this.refreshPumpInformation();
    }

    refreshPumpInformation(){
        this.http.get<APIBaseResponse<Pump>>(`${environment.API_URL}/system/${this.system.system.id}/pump/${this.pump.id}`)
        .subscribe((result) => {
            this.pump = result.data;
        })
        this.getSchedulesForPump();
    }

    startPump(){
        this.http.post<APIBaseResponse<Pump>>(`${environment.API_URL}/system/${this.system.system.id}/pump/${this.pump.id}/pump`, {})
        .subscribe((result) => {
            this.pump = result.data;
        });
    }

    modifyScheduleForPump(scheduleUpdate: IPumpSchedule){
        console.log(scheduleUpdate);
        this.http.post<APIBaseResponse<Array<IPumpSchedule>>>(`${environment.API_URL}/system/${this.system.system.id}/pump_schedule/${this.pump.id}/${scheduleUpdate.id}`, scheduleUpdate)
        .subscribe((result) => {
            this.schedules = result.data;
        });
    }

    getSchedulesForPump(){
        console.log("Getting schedules for pump");
        this.http.get<APIBaseResponse<Array<IPumpSchedule>>>(`${environment.API_URL}/system/${this.system.system.id}/pump_schedule/${this.pump.id}`)
        .subscribe((result) => {
            this.schedules = result.data;
            console.log("Schedules", this.schedules);
        });
    }

    deleteScheduleForPump(scheduleId: number=-1){
        if(scheduleId == -1){
            //we are trying to delete all
            this.http.delete<APIBaseResponse<Array<IPumpSchedule>>>(`${environment.API_URL}/system/${this.system.system.id}/pump_schedule/${this.pump.id}`)
            .subscribe((result) => {
                this.schedules = result.data;
            })
        } else{
            this.http.delete<APIBaseResponse<Array<IPumpSchedule>>>(`${environment.API_URL}/system/${this.system.system.id}/pump_schedule/${this.pump.id}/${scheduleId}`)
            .subscribe((result) => {
                this.schedules = result.data;
            });
        }

    }

}