import { Component, OnInit } from '@angular/core';
import { SystemObject } from 'src/app/models/system';
import { SystemService } from 'src/app/services/system.service';

@Component({
  selector: 'app-systems-home',
  templateUrl: './systems-home.component.html',
  styleUrls: ['./systems-home.component.scss']
})
export class SystemsHomeComponent implements OnInit {
  systems: Array<SystemObject> = new Array();

  constructor(
    private systemService: SystemService
  ) { }

  ngOnInit(): void {
    this.systemService.getSystems().then((result) => {
      console.log(result);
      this.systems = Array.from(result);
    });
  }

}
