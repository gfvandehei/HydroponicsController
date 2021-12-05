import { Component, Input, OnInit } from '@angular/core';
import {DhtSensorWrapper} from "../../types/dht";

@Component({
  selector: 'app-dht-card',
  templateUrl: './dht-card.component.html',
  styleUrls: ['./dht-card.component.scss']
})
export class DhtCardComponent implements OnInit {
  @Input() dhtSensor: DhtSensorWrapper | null = null;

  constructor() { }

  ngOnInit(): void {
  }

}
