import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { SystemObject } from 'src/app/models/system';
import { SystemService } from 'src/app/services/system.service';
import { PumpWrapper } from 'src/app/types/pump';

@Component({
  selector: 'app-system-automation',
  templateUrl: './system-automation.component.html',
  styleUrls: ['./system-automation.component.scss']
})
export class SystemAutomationComponent implements OnInit {
  systemObject: SystemObject | undefined;
  pumps: Array<PumpWrapper> | undefined;
  constructor(
    private route: ActivatedRoute,
    private systems: SystemService
  ) { }

  ngOnInit(): void {
    let systemId = Number.parseInt(this.route.parent!.snapshot.paramMap.get("systemId")!);
    this.systemObject = this.systems.systemObjects.get(systemId);
    this.systemObject!.pumps.subscribe((pumps) => {
      this.pumps = pumps;
    });
  }

}
