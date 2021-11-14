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