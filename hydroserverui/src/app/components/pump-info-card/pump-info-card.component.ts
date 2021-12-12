import { Component, Input, OnInit } from '@angular/core';
import { PumpWrapper } from 'src/app/types/pump';
import { IPumpSchedule } from 'src/app/types/pumpschedule';

@Component({
  selector: 'app-pump-info-card',
  templateUrl: './pump-info-card.component.html',
  styleUrls: ['./pump-info-card.component.scss']
})
export class PumpInfoCardComponent implements OnInit {
  @Input() pump: PumpWrapper | undefined;

  constructor() { }

  ngOnInit(): void {
  }

  updateSchedule(pumpSchedule: IPumpSchedule, index: number){
    // if angular does pass by reference this will work, if not then we have to
    console.log(pumpSchedule);
    // pass the updated schedule object
    this.pump?.modifyScheduleForPump(this.pump.schedules[index]);
  }

  startPump(){
    this.pump?.startPump();
  }

}
