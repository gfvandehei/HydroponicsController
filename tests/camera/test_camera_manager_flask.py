from hydroserver.physical_interfaces.camera_controller import CameraController
from hydroserver.physical_interfaces.camera_storage import CameraStore
from hydroserver.physical_interfaces.camera_streamer import CameraStreamer
import datetime
import time
import flask
from hydroserver.views.camera_blueprint import create_camera_blueprint

cam_stream = CameraStreamer()
cam_store = CameraStore("./tests/camera", datetime.datetime.now().time())
cam_man = CameraController(cam_store, cam_stream)
cam_man.start()

app = flask.Flask(__name__)
app.register_blueprint(create_camera_blueprint(
    cam_man,
    cam_stream
), url_prefix="/camera")
print("starting flask")
app.run(host="localhost", port=5000)