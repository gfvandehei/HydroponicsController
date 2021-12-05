import { Component, Input, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { SystemObject } from 'src/app/models/system';
import {SystemService} from "../../../services/system.service";
import {DhtSensorWrapper} from "../../../types/dht";

@Component({
  selector: 'app-system-sensors',
  templateUrl: './system-sensors.component.html',
  styleUrls: ['./system-sensors.component.scss']
})
export class SystemSensorsComponent implements OnInit {
  systemObject: SystemObject | null = null;

  constructor(
    private systemService: SystemService,
    private route: ActivatedRoute
  ) { }

  ngOnInit(): void {
    console.log(this.route.snapshot.parent!.params);
    let systemId = Number.parseInt(this.route.parent!.snapshot.params.systemId);
    this.systemService.getSystem(systemId).then((result) =>
      this.systemObject = this.systemService.systemObjects.get(systemId)!
    );
  }

}
