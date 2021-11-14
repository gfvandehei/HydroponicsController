import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import { environment } from 'src/environments/environment';
import {CameraSerialized, CameraListResponse} from "../types/camera"

@Injectable({
  providedIn: 'root'
})
export class CameraService {

  constructor(
    private http: HttpClient
  ) { }

  async listCameras(): Promise<CameraSerialized[]>{
    let response = await this.http.get<CameraListResponse>(`${environment.API_URL}/camera`).toPromise();
    return response.data;
  }

  getCameraStream(index: number): string{
    return `${environment.API_URL}/camera/${index}/stream`;
  }

  async setCameraRefreshRate(index: number, newRefreshRate: number): Promise<CameraSerialized>{
    let response = await this.http.post<CameraSerialized>(
      `${environment.API_URL}/camera/${index}/refresh_rate`,
      {
        refresh_rate: newRefreshRate
      }
    ).toPromise()
    return response;
  }
}
