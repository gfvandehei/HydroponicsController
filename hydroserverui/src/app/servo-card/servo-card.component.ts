import { Component, OnInit, Input } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { ServoMotor } from '../types/servo';
import { ServoService } from "../services/servo.service";

@Component({
  selector: 'app-servo-card',
  templateUrl: './servo-card.component.html',
  styleUrls: ['./servo-card.component.scss']
})
export class ServoCardComponent implements OnInit {
  @Input() servoID: string = "-1";
  servo: BehaviorSubject<ServoMotor> = new BehaviorSubject({pin: -1, value: -99, id: -1, system_id: -1, label: "default"});
  stepAmount = .1;

  constructor(
    private servos: ServoService
  ) { }

  ngOnInit(): void {
    this.servo = this.servos.servoById.get(this.servoID.toString()) as BehaviorSubject<ServoMotor>;
  }

  increment(){
    this.servos.incrementServo(Number.parseInt(this.servoID), this.stepAmount);
  }

  decrement(){
    this.servos.decrementServo(Number.parseInt(this.servoID), this.stepAmount);
  }

  setValue(value: number){
    this.servos.moveServo(Number.parseInt(this.servoID), value);
  }

}
