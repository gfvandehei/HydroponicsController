import { Component, Input, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { SystemObject } from 'src/app/models/system';

@Component({
  selector: 'app-system-information-card',
  templateUrl: './system-information-card.component.html',
  styleUrls: ['./system-information-card.component.scss']
})
export class SystemInformationCardComponent implements OnInit {
  toggled: boolean = false;
  @Input() systemObject: SystemObject | null = null;

  constructor(
    private router: Router,
  ) { }

  navigateToSystem(){
    this.router.navigate(["system", this.systemObject?.system.id]);
  }
  ngOnInit(): void {
  }

}
