import { Component, Input, OnInit } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { Pump } from '../types/pump';
import { PumpService } from '../services/pump.service';
@Component({
  selector: 'app-pump-card',
  templateUrl: './pump-card.component.html',
  styleUrls: ['./pump-card.component.scss']
})
export class PumpCardComponent implements OnInit {
  @Input("pumpId") pumpId: number = -1;
  pump: BehaviorSubject<Pump> | undefined;

  constructor(
    private pumpService: PumpService
  ) { }

  async ngOnInit(): Promise<void> {
    this.pump = await this.pumpService.getPumpInformation(this.pumpId) as BehaviorSubject<Pump>;
  }

  fillPump(){
    this.pumpService.runPump(this.pumpId);
  }

}
