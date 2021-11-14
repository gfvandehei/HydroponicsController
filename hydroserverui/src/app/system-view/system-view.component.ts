import { Component, Input, OnInit } from '@angular/core';
import { System } from '../models/system';
import {SystemService} from "../services/system.service";
import { BehaviorSubject } from 'rxjs';
import { ServoService } from '../services/servo.service';
import { CameraService } from '../services/camera.service';
import { CameraSerialized } from '../types/camera';
import { DhtsensorService } from '../services/dhtsensor.service';
import { PumpService } from '../services/pump.service';

@Component({
  selector: 'app-system-view',
  templateUrl: './system-view.component.html',
  styleUrls: ['./system-view.component.scss']
})
export class SystemViewComponent implements OnInit {
  @Input() systemID: number = -1;
  system: BehaviorSubject<System> = new BehaviorSubject({id: -1, name: "", address: "-1.-1.-1.-1"});
  servosList: BehaviorSubject<Set<string>> = new BehaviorSubject(new Set());
  cameraList: Array<CameraSerialized> = [];
  cameraImgSrcList: Array<string> = [];
  dhtDeviceList: BehaviorSubject<Set<string>> = new BehaviorSubject(new Set());
  pumpDeviceList: BehaviorSubject<Set<number>> = new BehaviorSubject(new Set());
  
  constructor(
    private systems: SystemService,
    private servos: ServoService,
    public cameras: CameraService,
    private dhts: DhtsensorService,
    private pumps: PumpService
  ) { }

  async ngOnInit(): Promise<void> {
    this.system = await this.systems.getSystem(this.systemID as number);
    this.servosList = this.servos.servoMotors;
    this.cameraList = await this.cameras.listCameras();
    this.dhtDeviceList = this.dhts.dhtSensors;
    this.pumpDeviceList = this.pumps.pumps;

    this.dhtDeviceList.subscribe((update) => {
      console.log("DHTDEVICES", update);
    });
    this.pumpDeviceList.subscribe((result) => {
      console.log("Pumps", result);
    })
    let imgSrcArray = [];
    for(let index=0;index < this.cameraList.length; index++){
      let imgsrc = this.cameras.getCameraStream(index);
      imgSrcArray.push(imgsrc);
    }
    this.cameraImgSrcList = imgSrcArray;
    this.servos.listServoMotors();
    this.dhts.getDHTSensorData();
    this.pumps.listAllPumps();
  }

}
