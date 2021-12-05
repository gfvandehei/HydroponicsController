from flask import Blueprint, Response, request
from queue import Queue
import cv2
from hydroserver.controllers.camera_manager import CameraManager
from hydroserver.physical_interfaces.camera_storage import CameraStore
from hydroserver.physical_interfaces.camera_streamer import CameraStreamer, CameraStreamerEvents

class CameraStreamSubscriber(object):

    def __init__(self, camera_streamer: CameraStreamer):
        self.img_queue = Queue()
        self.streamer = camera_streamer
        self.streamer.on(CameraStreamerEvents.image_published, self.get_image)
    
    def get_image(self, image: bytes):
        self.img_queue.put(image)

    def __call__(self):
        while True:
            frame = self.img_queue.get()
            # encode to jpg
            ret, jpg_encoded = cv2.imencode(".jpg", frame)
            frame = jpg_encoded.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def create_camera_blueprint(camera_manager: CameraManager):

    camera_blueprint = Blueprint("camera", __name__)

    @camera_blueprint.route("/")
    def get_camera_datas():
        values = camera_manager.cameras.values()
        serialized_values = list(map(lambda x: x.json(), values))
        return {
            "data": serialized_values
        }

    @camera_blueprint.route("/<camera_id>/stream")
    def get_camera_stream(camera_id):
        camera_id = int(camera_id)
        camera = camera_manager.cameras[camera_id]
        camera_streamer = camera.image_stream
        new_camera_streamer_subscriber = CameraStreamSubscriber(camera_streamer)
        return Response(new_camera_streamer_subscriber(), mimetype='multipart/x-mixed-replace; boundary=frame')

    @camera_blueprint.route("/<camera_id>/image")
    def get_camera_image(camera_id):
        camera_id = int(camera_id)
        camera = camera_manager.cameras[camera_id]
        image_bytes = camera.image_stream._current_image_bytes
        ret, as_jpeg = cv2.imencode(".jpg", image_bytes)
        return Response(as_jpeg.tobytes(), content_type="image/jpeg")
        
    @camera_blueprint.route("/<camera_id>/refresh_rate", methods=["POST"])
    def set_camera_refresh_rate(camera_id):
        camera_id = int(camera_id)
        body = request.json()
        ref_rate = body['refresh_rate']
        camera = camera_manager.cameras[camera_id]
        camera.update_refresh_rate(ref_rate)
        return camera.json()

    return camera_blueprint

