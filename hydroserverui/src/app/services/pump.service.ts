import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { APIBaseResponse } from '../models/api';
import {Pump} from "../types/pump";

@Injectable({
  providedIn: 'root'
})
export class PumpService {
  pumps: BehaviorSubject<Set<number>> = new BehaviorSubject(new Set());
  pumpByIdMap: Map<number, BehaviorSubject<Pump>> = new Map();
  
  constructor(
    private http: HttpClient
  ) { }

  updatePump(pumpId: number, pump: Pump, batch:boolean=false){
    let pumpBehaviorSubject = null;
    if(this.pumpByIdMap.has(pumpId)){
      pumpBehaviorSubject = this.pumpByIdMap.get(pumpId);
      pumpBehaviorSubject?.next(pump);
    } else{
      this.pumpByIdMap.set(pumpId, new BehaviorSubject(pump));
      pumpBehaviorSubject = this.pumpByIdMap.get(pumpId);
    }
    if(!batch){
      if(!this.pumps.value.has(pumpId)){
        let oldSet = this.pumps.getValue()
        oldSet.add(pumpId);
        this.pumps.next(oldSet);
      }
    }
    return pumpBehaviorSubject;
  }

  async listAllPumps(){
    let response = await this.http.get<APIBaseResponse<Pump[]>>(`${environment.API_URL}/pump/`).toPromise();
    console.log(response);
    for(let pump of response.data){
      this.updatePump(pump.id, pump)
    }
    return this.pumps;
  }

  async getPumpInformation(pumpId: number){
    if(this.pumpByIdMap.has(pumpId)){
      this.http.get<APIBaseResponse<Pump>>(`${environment.API_URL}/pump/${pumpId}`).subscribe((result) => {
        this.updatePump(result.data.id, result.data);
      });
      return this.pumpByIdMap.get(pumpId);
    } else{
      let response = await this.http.get<APIBaseResponse<Pump>>(`${environment.API_URL}/pump/${pumpId}`).toPromise();
      return this.updatePump(response.data.id, response.data);
    }
  }

  async runPump(pumpId: number){
    let response = await this.http.post<APIBaseResponse<Pump>>(`${environment.API_URL}/pump/${pumpId}/pump`, {}).toPromise();
    return this.updatePump(response.data.id, response.data);
  }
}
