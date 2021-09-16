export interface CameraSerialized{
    index: number,
    refresh_rate: number
}

export interface CameraListResponse{
    data: Array<CameraSerialized>
}