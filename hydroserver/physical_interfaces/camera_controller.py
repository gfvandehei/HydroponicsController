import time
import cv2
from threading import Thread
import numpy as np
from hydroserver.physical_interfaces.camera_streamer import CameraStreamer
from hydroserver.physical_interfaces.camera_storage import CameraStore
import hydroserver.model.model as Model

class CameraController(Thread):

    def __init__(
        self, 
        camera_store: CameraStore,
        camera_stream: CameraStreamer,
        camera_db_object: Model.Camera):
        """Controls a single camera connected to the system, camera
        is selected via system index

        :param camera_store: an object dedicated to handling storage of images from
        the camera on the system
        :type camera_store: CameraStore
        :param camera_stream: an object dedicated to handling instantanios camera data,
        and its interactions with other objects
        :type camera_stream: CameraStreamer
        :param camera_index: the index of the camera within the system
        :type camera_index: int
        """

        Thread.__init__(self)
        self.image_store = camera_store
        self.image_stream = camera_stream
        self.camera_index = camera_db_object.index
        self.camera_db_obj = camera_db_object
        #self.rawCapture = PiRGBArray(self.camera, size=(640, 480))
        self.camera = cv2.VideoCapture(self.camera_index)
        self.most_recent_image = None
        self._refresh_rate = 1
        # sleep for a 1/10 second to allow camera to start up
        time.sleep(.1)

    def run(self):
        """
        runs in a thread on start(), reads camera frames and adds frame to
        storage and stream
        :extends Thread.run
        """
        while True:
            ret, frame = self.camera.read()
            frame: np.ndarray
            # need to flip camera, it is upsidown
            frame = np.flip(frame)
            # add to stream
            self.image_stream.add_new_image(frame)
            # check if needs to be saved for timelapse
            self.image_store.save_image(frame)
            time.sleep(self._refresh_rate)

    def update_refresh_rate(self, new_refresh: float):
        """changes the time between frame grabs

        :param new_refresh: the new refresh rate in seconds
        :type new_refresh: float
        """
        self._refresh_rate = new_refresh

    def json(self):
        """a function used to grab serializable information
        about the class for web responses

        :return: a serializable dict representing the camera
        :rtype: Dict[str, Any]
        """
        as_dict = self.camera_db_obj.__dict__.copy()
        del as_dict["_sa_instance_state"]
        as_dict['refresh_rate'] = self._refresh_rate
        return as_dict

