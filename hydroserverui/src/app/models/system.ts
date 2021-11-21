import { HttpClient } from "@angular/common/http";
import {BehaviorSubject} from "rxjs"
import { APIBaseResponse } from "./api";
import {Pump} from "../types/pump";
import {DHTSensor} from "../types/dht";
import {environment} from "src/environments/environment";
import { CameraListResponse, CameraSerialized } from "../types/camera";

export interface System {
    id: number
    name: string
    address: string
}

export class SystemObject{
    system: System;
    system_url: String;
    http: HttpClient;
    pumps = new BehaviorSubject<Array<Pump>>(new Array<Pump>());
    dhtsensors = new BehaviorSubject<Array<DHTSensor>>(new Array());
    servos = new BehaviorSubject<Set<number>>(new Set());
    cameras = new BehaviorSubject<Array<CameraSerialized>>(new Array());

    constructor(
        system: System,
        http: HttpClient
    ){
        this.system = system;
        this.http = http;
        this.system_url = `${environment.API_URL}/system/${this.system.id}`;
        this.populateSystemInformation();
    }

    getPumpInformation(){
        this.http.get<APIBaseResponse<Array<Pump>>>(`${this.system_url}/pump`).subscribe((result) => {
            this.pumps.next(result.data);
        });
    }

    getDHTInformation(){
        this.http.get<APIBaseResponse<Array<DHTSensor>>>(`${this.system_url}/dht`).subscribe((result) => {
            this.dhtsensors.next(result.data);
        });
    }

    getCameraInformation(){
        this.http.get<APIBaseResponse<Array<CameraSerialized>>>(`${this.system_url}/camera`).subscribe((result) => {
            this.cameras.next(result.data);
        });
    }

    populateSystemInformation(){
        this.getPumpInformation();
        this.getDHTInformation();
        this.getCameraInformation();
    }



}