import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import { environment } from 'src/environments/environment';
import { APIBaseResponse } from '../models/api';
import { DHTSensor } from '../types/dht';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DhtsensorService {
  dhtSensors: BehaviorSubject<Set<string>> = new BehaviorSubject(new Set());
  dhtSensorMap: Map<string, BehaviorSubject<DHTSensor>> = new Map();

  constructor(
    private http: HttpClient
  ) { }

  updateSensorValue(sensorId: string, sensor: DHTSensor){
    if(this.dhtSensorMap.has(sensorId)){
      this.dhtSensorMap.get(sensorId)?.next(sensor);
    } else{
      this.dhtSensorMap.set(sensorId, new BehaviorSubject(sensor));
    }
    return this.dhtSensorMap.get(sensorId) as BehaviorSubject<DHTSensor>;
  }

  async getDHTSensorData(){
    let response = await this.http.get<APIBaseResponse<{[name: string]: DHTSensor}>>(environment.API_URL+"/dht").toPromise();
    console.log("response");
    let sensorIDs = new Set<string>();
    for(let [sensorId, sensor] of Object.entries(response.data)){
      sensorIDs.add(sensorId);
      this.updateSensorValue(sensorId, sensor);
    }
    this.dhtSensors.next(sensorIDs);
    return response.data;
  }
}
