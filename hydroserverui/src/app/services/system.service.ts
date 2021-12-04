import { Injectable } from '@angular/core';
import {BehaviorSubject} from "rxjs";
import {System} from "../models/system";
import {APIBaseResponse} from "../models/api";
import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment';
import {SystemObject} from "../models/system";
import {DhtSensorWrapper} from "../types/dht";

@Injectable({
  providedIn: 'root'
})
export class SystemService {
  systems: BehaviorSubject<Set<number>> = new BehaviorSubject(new Set());
  individual_systems: Map<number, BehaviorSubject<System>> = new Map();

  systemObjects: Map<number, SystemObject> = new Map();

  constructor(
    private http: HttpClient
  ) {}

  async getSystems(){
    try{
      let response = await this.http.get<APIBaseResponse<Array<System>>>(`${environment.API_URL}/system`).toPromise();
      response.data.forEach((system) => {
        let systemObject = new SystemObject(system, this.http);
        this.systemObjects.set(system.id, systemObject);
      });
      return Array.from(this.systemObjects.values());
    } catch(err){
      console.error(err);
      return [];
    }
  }

  private async updateSystem(system: System, batch=false){
    let existing_system = this.individual_systems.get(system.id)
    if(existing_system != undefined && existing_system.value != system){
      existing_system.next(system)
    } else if(existing_system == undefined){
      this.individual_systems.set(system.id, new BehaviorSubject(system));
    }
    return this.individual_systems.get(system.id) as BehaviorSubject<System>;
  }

  async loadAllSystems(){
    let response = await this.http.get<APIBaseResponse<Array<System>>>(`${environment.API_URL}/system`).toPromise();
    const systemIDs = new Set(response.data.map((value, index, arr) => value.id));
    console.log(response);
    //const systems = response.data;
    //const systemIDs = new Set([1]);
    //const systems = [{id: 1, name: "system", address: "192.168.1.13"}]
    // check to see if a new system was added
    let lastSet = this.systems.value;
    if(lastSet != systemIDs){
      this.systems.next(systemIDs);
    }

    for(let system of response.data){
      this.updateSystem(system, true);
    }
    return this.systems;
  }

  async getSystem(systemID: number){
    /*let response = await this.http.get<APIBaseResponse<System>>(`${environment.API_URL}/system/${systemID}`).toPromise();
    const systemData = response.data;
    if(!this.systems.value.has(systemData.id)){
      let lastSystemSet = this.systems.value;
      lastSystemSet.add(systemData.id);
      this.systems.next(lastSystemSet);
    }*/
    const systemData = {id: 1, name: "system", address: "192.168.1.13"};
    return this.updateSystem(systemData, false);
  }
}
