import { HttpClient } from "@angular/common/http";
import { environment } from "src/environments/environment";
import { APIBaseResponse } from "../models/api";
import { SystemObject } from "../models/system";

export interface DHTSensor{
    label: string
    pin: number
    temperature: number
    humidity: number
    id: number
}

export class DhtSensorWrapper{
    public dht: DHTSensor;
    private system: SystemObject;
    private http: HttpClient;
    private baseUrl: string;

    public data: {temperature: number, humidity: number} = {
        temperature: 0.0,
        humidity: 0.0
    }
    
    constructor(dht: DHTSensor, system: SystemObject, http: HttpClient){
        this.dht = dht;
        this.system = system;
        this.http = http;
        this.baseUrl = `${environment.API_URL}/system/${this.system.system.id}/dht/${dht.id}`;
    }

    getSensorData(){
        this.http.get<APIBaseResponse<DHTSensor>>(this.baseUrl).subscribe((result) => {
            this.data.humidity = result.data.humidity;
            this.data.temperature = result.data.temperature;
        });
    }
}