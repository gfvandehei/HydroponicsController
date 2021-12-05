import { HttpClient } from "@angular/common/http";
import {BehaviorSubject} from "rxjs"
import { APIBaseResponse } from "./api";
import {Pump, PumpWrapper} from "../types/pump";
import {DHTSensor, DhtSensorWrapper} from "../types/dht";
import {environment} from "src/environments/environment";
import { CameraListResponse, CameraSerialized, CameraWrapper} from "../types/camera";

export interface System {
    id: number
    name: string
    address: string
}

export class SystemObject{
    system: System;
    system_url: String;
    http: HttpClient;
    pumps = new BehaviorSubject<Array<PumpWrapper>>(new Array());
    dhtsensors = new BehaviorSubject<Array<DhtSensorWrapper>>(new Array());
    servos = new BehaviorSubject<Set<number>>(new Set());
    cameras = new BehaviorSubject<Array<CameraWrapper>>(new Array());

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
            //create pump wrappers
            let pumpWrappers: PumpWrapper[] = []
            result.data.forEach((pump) => {
                let newPumpWrapper = new PumpWrapper(pump, this, this.http);
                pumpWrappers.push(newPumpWrapper);
            });
            this.pumps.next(pumpWrappers);
        });
    }

    getDHTInformation(){
        this.http.get<APIBaseResponse<{[key: number]: DHTSensor}>>(`${this.system_url}/dht`).subscribe((result) => {
            let dhtSensors: Array<DhtSensorWrapper> = [];
            console.log(result);
            Object.values(result.data).forEach(sensor => {
                console.log(sensor)
                let dhtSensorWrapper = new DhtSensorWrapper(sensor, this, this.http);
                dhtSensors.push(dhtSensorWrapper);
            });
            this.dhtsensors.next(dhtSensors);
        });
    }

    getCameraInformation(){
        this.http.get<APIBaseResponse<Array<CameraSerialized>>>(`${this.system_url}/camera`).subscribe((result) => {
            //this.cameras.next(result.data);
            let cameraList: Array<CameraWrapper> = [];
            result.data.forEach((camera) => {
                let camObject = new CameraWrapper(camera, this.system, this.http);
                cameraList.push(camObject);
            });
            this.cameras.next(cameraList);
        });
    }

    populateSystemInformation(){
        this.getPumpInformation();
        this.getDHTInformation();
        this.getCameraInformation();
    }



}