import { Component, ElementRef, Input, AfterViewInit, ViewChild, ViewRef } from '@angular/core';

@Component({
  selector: 'app-dual-circle-graph',
  templateUrl: './dual-circle-graph.component.html',
  styleUrls: ['./dual-circle-graph.component.scss']
})
export class DualCircleGraphComponent implements AfterViewInit {
  @ViewChild("dualCircleCanvas", {static: false})
  dualCircleCanvas: ElementRef<HTMLCanvasElement> | null = null;
  @Input() value1 = 0;
  @Input() value2 = 0;
  @Input() range1 = 0;
  @Input() range2 = 0;
  @Input() strokeWidth = 10;

  canvasElement: HTMLCanvasElement | undefined;
  ctx: CanvasRenderingContext2D | undefined;

  constructor() { }

  ngAfterViewInit(): void {
    this.canvasElement = this.dualCircleCanvas?.nativeElement!;
    this.ctx = this.canvasElement.getContext("2d")!;
    setInterval(() => {this.draw()}, 1000);
  }

  draw(){
    this.ctx?.clearRect(0,0,this.canvasElement!.width, this.canvasElement!.height);
    let canvasCenterX = this.canvasElement!.width/2;
    let canvasCenterY = this.canvasElement!.height/2;
    let minRad = Math.min(canvasCenterY, canvasCenterX);
    this.drawInnerGraph(canvasCenterX, canvasCenterY, minRad);
    this.drawOuterGraph(canvasCenterX, canvasCenterY, minRad);
  }

  drawOuterGraph(canvasCenterX: number, canvasCenterY: number, minRad: number){
    //get canvas center
    let percentage = this.value1/this.range1;
    this.ctx?.beginPath();
    this.ctx!.strokeStyle = "#00AB84";
    this.ctx!.lineWidth = this.strokeWidth;
    this.ctx!.lineCap = "round";
    this.ctx!.textAlign = "center";
    this.ctx?.arc(canvasCenterX, canvasCenterY, minRad-this.strokeWidth, 0, (2*Math.PI)*percentage);
    this.ctx?.fillText(`${this.value1} %`, canvasCenterX, canvasCenterY);
    this.ctx?.stroke();
  }

  drawInnerGraph(canvasCenterX: number, canvasCenterY: number, minRad: number){
    let percentage = this.value2/this.range2;
    this.ctx?.beginPath();
    this.ctx!.strokeStyle = "#0095b3";
    this.ctx!.lineWidth = this.strokeWidth;
    this.ctx!.lineCap = "round";
    this.ctx!.textAlign = "center";
    this.ctx!.fillStyle = "white";
    this.ctx!.font = "20px arial";
    this.ctx?.arc(canvasCenterX, canvasCenterY, minRad-this.strokeWidth*2, 0, (2*Math.PI)*percentage);
    this.ctx?.fillText(`${Math.round(this.value2)} °`, canvasCenterX, canvasCenterY+20);

    this.ctx?.stroke();
  }

}
