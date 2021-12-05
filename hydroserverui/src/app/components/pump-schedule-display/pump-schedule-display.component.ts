import { Component, EventEmitter, Input, OnInit } from '@angular/core';
import { IPumpSchedule, DayCodes } from 'src/app/types/pumpschedule';

@Component({
  selector: 'app-pump-schedule-display',
  templateUrl: './pump-schedule-display.component.html',
  styleUrls: ['./pump-schedule-display.component.scss']
})
export class PumpScheduleDisplayComponent implements OnInit {
  @Input() schedule: IPumpSchedule | undefined;
  updatedEvent: EventEmitter<IPumpSchedule> = new EventEmitter();
  
  activeDays: Set<string> | undefined;
  allDays = DayCodes;

  constructor() { }

  ngOnInit(): void {
    this.activeDays = new Set(this.schedule?.days_active);
  }

  toggleDay(daycode: string){
    if(this.activeDays?.has(daycode)){
      this.activeDays.delete(daycode)
    } else{
      this.activeDays?.add(daycode);
    }
    this.schedule!.days_active = Array.from(this.activeDays!);
    this.updatedEvent.emit(this.schedule!);
  }

  addTime(){
    // open time dialog
  }

  removeTime(index: number){
    this.schedule!.times = this.schedule!.times.splice(index, 1);
    this.updatedEvent.emit(this.schedule!);
  }


}
