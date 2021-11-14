from hydroserver.physical_interfaces.camera_controller import CameraController
from hydroserver.physical_interfaces.camera_storage import CameraStore
from hydroserver.physical_interfaces.camera_streamer import CameraStreamer
import datetime
import time

cam_stream = CameraStreamer()
cam_store = CameraStore("./tests/camera", datetime.datetime.now().time())
cam_man = CameraController(cam_store, cam_stream)
cam_man.start()

time.sleep(2)

print(cam_store.list_all_images())