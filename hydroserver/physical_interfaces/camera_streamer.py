import observable
import enum

class CameraStreamerEvents(enum.Enum):
    image_published="image_pub"

class CameraStreamer(observable.Observable):

    def __init__(self):
        observable.Observable.__init__(self)
        self._current_image_bytes = None

    def add_new_image(self, image_bytes: bytes):
        self._current_image_bytes = image_bytes
        self.trigger(CameraStreamerEvents.image_published, self._current_image_bytes)
