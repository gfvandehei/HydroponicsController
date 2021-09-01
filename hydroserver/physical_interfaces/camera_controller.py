import time
import datetime
import cv2
from threading import Thread
import os
import io
import numpy as np
from hydroserver.physical_interfaces.camera_streamer import CameraStreamer
from hydroserver.physical_interfaces.camera_storage import CameraStore

class CameraController(Thread):

    def __init__(
        self, 
        camera_store: CameraStore,
        camera_stream: CameraStreamer,
        camera_index: int,
        max_images=100):

        Thread.__init__(self)
        self.image_store = camera_store
        self.image_stream = camera_stream
        self.camera_index = camera_index
        #self.rawCapture = PiRGBArray(self.camera, size=(640, 480))
        self.camera = cv2.VideoCapture(camera_index)
        self.most_recent_image = None
        self._refresh_rate = 1
        time.sleep(.1)

    def run(self):
        while True:
            ret, frame = self.camera.read()
            frame: np.ndarray
            frame = np.flip(frame)
            self.image_stream.add_new_image(frame)
            self.image_store.save_image(frame)
            time.sleep(self._refresh_rate)

    def update_refresh_rate(self, new_refresh:int):
        self._refresh_rate = new_refresh

    def json(self):
        return {
            "index": self.camera_index,
            "refresh_rate": self._refresh_rate
        }

