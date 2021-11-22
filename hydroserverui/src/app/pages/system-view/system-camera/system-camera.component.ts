import { Component, ElementRef, Input, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { SystemObject } from 'src/app/models/system';
import { SystemService } from 'src/app/services/system.service';
import { CameraSerialized, CameraWrapper } from 'src/app/types/camera';

@Component({
  selector: 'app-system-camera',
  templateUrl: './system-camera.component.html',
  styleUrls: ['./system-camera.component.scss']
})
export class SystemCameraComponent implements OnInit {
  systemObject: SystemObject | null = null;
  camera: CameraWrapper | null = null
  @ViewChild("imageContainer") imageContainer: ElementRef | null = null;

  image: any;

  constructor(
    private activatedRoute: ActivatedRoute,
    private systemService: SystemService
  ) { }

  ngOnInit(): void {
    let systemId = Number.parseInt(this.activatedRoute.parent!.snapshot.paramMap.get("systemId")!);
    this.systemObject = this.systemService.systemObjects.get(systemId)!;
    console.log(this.systemObject);
    let cameraId = Number.parseInt(this.activatedRoute.snapshot.paramMap.get("cameraId")!);
    console.log(cameraId)
    console.log(cameraId);
    console.log(this.activatedRoute.parent!.snapshot.paramMap);
    this.systemObject?.cameras.subscribe((cameraWrappers) => {
      this.camera = cameraWrappers.find((value, index, obj) => value.camera.id == cameraId)!;
      this.updateImage();
    });
  }

  updateImage(){
    this.camera?.getImage().then((result) => {
      result.subscribe(image => this.imageContainer!.nativeElement.src = window.URL.createObjectURL(image));
    });
  }

}
