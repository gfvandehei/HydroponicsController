import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { SystemObject } from 'src/app/models/system';
import {SystemService} from "src/app/services/system.service";

@Component({
  selector: 'app-system-view',
  templateUrl: './system-view.component.html',
  styleUrls: ['./system-view.component.scss']
})
export class SystemViewComponent implements OnInit {
  systemObject: SystemObject | null = null;

  constructor(
    private systemService: SystemService,
    private activatedRoute: ActivatedRoute
  ) { }

  async ngOnInit(): Promise<void> {
    await this.systemService.getSystems();
    this.systemObject = this.systemService.systemObjects.get(Number.parseInt(this.activatedRoute.snapshot.paramMap.get("systemId")!))!;
  }

}
