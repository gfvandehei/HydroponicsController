import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import { environment } from 'src/environments/environment';
import { APIBaseResponse } from '../models/api';
import { ServoMotor } from '../types/servo';
import {BehaviorSubject} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class ServoService {
  servoMotors: BehaviorSubject<Set<string>> = new BehaviorSubject(new Set());
  servoById: Map<string, BehaviorSubject<ServoMotor>> = new Map();

  constructor(
    private http: HttpClient
  ) { }

  private updateServoObject(servoId: number, servo: ServoMotor){
    if(!this.servoById.has(servoId.toString())){
      this.servoById.set(servoId.toString(), new BehaviorSubject(servo));
    } else{
      this.servoById.get(servoId.toString())?.next(servo);
    }
    return this.servoById.get(servoId.toString());
  }

  private updateServoList(servoSet: Set<string>){
    if(this.servoMotors.value != servoSet){
      this.servoMotors.next(servoSet);
    }
    return this.servoMotors;
  }

  async listServoMotors(){
    let response = await this.http.get<APIBaseResponse<{[id: number]: ServoMotor}>>(environment.API_URL+"/servo").toPromise();
    let servoIdSet = new Set(Object.keys(response.data));
    // add all the servo motors to map
    for(let [servoId, servo] of Object.entries(response.data)){
      this.updateServoObject(Number.parseInt(servoId), servo);
    }
    this.updateServoList(servoIdSet);
    return response.data
  }

  async incrementServo(servoID: number, stepAmount: number){
    let response = await this.http.post<APIBaseResponse<ServoMotor>>(
      environment.API_URL+`/servo/${servoID}/move`, {
        method: "ITERATE",
        value: stepAmount
      }
    ).toPromise();
    let servo = this.updateServoObject(servoID, response.data);
    return servo;
  }

  async decrementServo(servoID: number, stepAmount: number){
    let response = await this.http.post<APIBaseResponse<ServoMotor>>(
      environment.API_URL+`/servo/${servoID}/move`, {
        method: "ITERATE",
        value: 0-stepAmount
      }
    ).toPromise();
    let servo = this.updateServoObject(servoID, response.data);
    return servo;
  }

  async moveServo(servoID: number, value: number){
    let response = await this.http.post<APIBaseResponse<ServoMotor>>(
      environment.API_URL+`/servo/${servoID}/move`,
      {
        "method": "SET",
        "value": value
      }
    ).toPromise()
    let servo = this.updateServoObject(servoID, response.data);
    return servo;
  }
}
