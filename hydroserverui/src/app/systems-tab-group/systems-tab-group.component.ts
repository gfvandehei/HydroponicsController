import { Component, OnInit } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { System } from '../models/system';
import {SystemService} from "../services/system.service";

@Component({
  selector: 'app-systems-tab-group',
  templateUrl: './systems-tab-group.component.html',
  styleUrls: ['./systems-tab-group.component.scss']
})
export class SystemsTabGroupComponent implements OnInit {
  systemsList: BehaviorSubject<Set<number>> = new BehaviorSubject(new Set([-1]));

  constructor(
    private systems: SystemService
  ) { }

  ngOnInit(): void {
    this.systemsList = this.systems.systems;
    this.systems.loadAllSystems();
  }

}
