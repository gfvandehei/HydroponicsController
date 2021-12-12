import { Component, EventEmitter, Output, Input, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { IPumpSchedule, DayCodes } from 'src/app/types/pumpschedule';
import { NewTimeDialogComponent } from './new-time-dialog/new-time-dialog.component';

@Component({
  selector: 'app-pump-schedule-display',
  templateUrl: './pump-schedule-display.component.html',
  styleUrls: ['./pump-schedule-display.component.scss']
})
export class PumpScheduleDisplayComponent implements OnInit {
  @Input() schedule: IPumpSchedule | undefined;
  @Output() updatedEvent= new EventEmitter<IPumpSchedule>();
  
  activeDays: Set<string> | undefined;
  allDays = DayCodes;

  constructor(
    public dialog: MatDialog
  ) { }

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
    let ref = this.dialog.open(NewTimeDialogComponent, {
      width: '250px',
      data: {}
    });
    ref.afterClosed().subscribe((newTime) => {
      console.log(newTime);
      this.schedule!.times.push(newTime);
      this.updatedEvent.emit(this.schedule);
    })
  }

  removeTime(index: number){
    console.log(this.schedule?.times, index);
    this.schedule!.times.splice(index, 1);
    console.log(this.schedule?.times);
    this.updatedEvent.emit(this.schedule!);
  }


}
