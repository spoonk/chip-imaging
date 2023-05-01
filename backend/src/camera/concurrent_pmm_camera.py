from camera.camera_interface import Camera
from camera.pmm_camera import PMMCamera
from threading import Lock

class CPMMCamera(Camera):
    """
    Concurrency wrapper around a pycromanager-camera that 
    only allows one thread to access the camera at a time
    """
    # TODO: could write a decorator...

    def __init__(self):
        self._cam = PMMCamera()
        self._lock = Lock()

    def connect(self):
        with self._lock:
            self._cam.connect()

    def close(self):
        with self._lock:
            self._cam.close()

    def take_image(self):
        with self._lock:
            im = self._cam.take_image()
            return im

    def set_gain(self, gain: int):
        with self._lock:
            self._cam.set_gain(gain)

    def set_exposure(self, exposure: float):
        with self._lock:
            self._cam.set_exposure(exposure)

    def is_connected(self):
        with self._lock:
            return self._cam.is_connected()
    
    def get_gain(self):
        with self._lock:
            return self._cam.get_gain()
    
    def get_exposure(self) -> float:
        with self._lock:
            return self._cam.get_exposure()
    