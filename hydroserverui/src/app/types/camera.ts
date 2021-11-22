import { HttpClient } from "@angular/common/http";
import { environment } from "src/environments/environment";
import { System } from "../models/system";

export interface CameraSerialized{
    refresh_rate: number
    id: number
    name: string
    index: number
    system_id: number
    camera_store_id: number
}

export interface CameraListResponse{
    data: Array<CameraSerialized>
}

export class CameraWrapper{
    public camera: CameraSerialized;
    private system: System;
    private http: HttpClient;
    private baseUrl: string;

    constructor(camera: CameraSerialized, system: System, http: HttpClient){
        this.system = system;
        this.camera = camera;
        this.http = http;
        this.baseUrl = `${environment.API_URL}/system/${this.system.id}/camera/${this.camera.id}`;

    }

    async getImage(){
        let image = this.http.get(this.baseUrl+"/image", {responseType: "blob"})
        return image;
    }
}