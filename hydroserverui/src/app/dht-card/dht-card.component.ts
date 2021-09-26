import { Component, OnInit, Input, ViewChild, AfterViewInit, ElementRef } from '@angular/core';
import {DhtsensorService} from "../services/dhtsensor.service";
import {BehaviorSubject} from "rxjs";
import {DHTSensor} from "../types/dht";

@Component({
  selector: 'app-dht-card',
  templateUrl: './dht-card.component.html',
  styleUrls: ['./dht-card.component.scss']
})
export class DhtCardComponent implements OnInit, AfterViewInit {
  @Input() dhtID: string = "-1";
  dht: BehaviorSubject<DHTSensor> = new BehaviorSubject(
    {
      label: "loading",
      pin: -1,
      temperature: -1,
      humidity: -1
    }
  );
  @ViewChild("humCanvas", {static: true}) humidityCanvas: ElementRef<HTMLCanvasElement> | null = null;
  @ViewChild("tempCanvas", {static: true}) temperatureCanvas: ElementRef<HTMLCanvasElement> | null = null;

  stepAmount = .1;

  constructor(
    private dhts: DhtsensorService
  ) { }

  ngOnInit(): void {
    this.dht = this.dhts.dhtSensorMap.get(this.dhtID) as BehaviorSubject<DHTSensor>;
  }

  ngAfterViewInit(){
    console.log(this.humidityCanvas, this.temperatureCanvas);
    this.dht.subscribe((result) => {
      this.redrawCanvases(result);
    })
  }

  getBarColor(percentage: number){
    let hue_range = 360-240;
    let hue = percentage*hue_range+240;
    console.log(hue);
    return `hsv(${hue}, 100, 100)`
  }

  redrawCanvases(dhtResult: DHTSensor){
    let hum = this.humidityCanvas?.nativeElement as HTMLCanvasElement;
    let temp = this.temperatureCanvas?.nativeElement as HTMLCanvasElement;
    let humctx = hum.getContext("2d") as CanvasRenderingContext2D;
    let tempctx = temp.getContext("2d") as CanvasRenderingContext2D;
    let hum_scaling_factor = dhtResult.humidity / 100;
    let temp_scaling_factory = dhtResult.temperature / 110;
    console.log(hum_scaling_factor, temp_scaling_factory)
    humctx.beginPath()
    humctx.lineWidth = hum.height;
    humctx.lineCap = "round"
    humctx.strokeStyle = this.getBarColor(hum_scaling_factor)
    humctx.moveTo(0, hum.height/2);
    let humLength = hum.width*hum_scaling_factor-hum.height/2;
    humctx.lineTo(humLength, hum.height/2);
    console.log(hum.width, humLength)
    humctx.stroke();

    tempctx.beginPath()
    tempctx.lineWidth = temp.height;
    tempctx.lineCap = "round"
    tempctx.strokeStyle = this.getBarColor(hum_scaling_factor)
    tempctx.moveTo(0, temp.height/2);
    let tempWidth = temp.width*temp_scaling_factory-temp.height/2;
    tempctx.lineTo(tempWidth, temp.height/2);
    console.log(temp.width, tempWidth);
    tempctx.stroke();
  }

}
