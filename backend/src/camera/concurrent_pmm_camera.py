from camera.camera_interface import Camera
from camera.pmm_camera import PMMCamera
from threading import Lock

class CPMMCamera(Camera):
    """
    Concurrency wrapper around a pycromanager-camera that 
    only allows one thread to access the camera at a time
    """

    def __init__(self):
        self._cam = PMMCamera()
        self._lock = Lock()

    def connect(self):
        self._lock.acquire()
        self._cam.connect()
        self._lock.release()

    def close(self):
        self._lock.acquire()
        self._cam.close()
        self._lock.release()

    def take_image(self):
        self._lock.acquire()
        im = self._cam.take_image()
        self._lock.release()
        return im

    def set_gain(self, gain: int):
        self._lock.acquire()
        self._cam.set_gain(gain)
        self._lock.release()

    def set_exposure(self, exposure: float):
        self._lock.acquire()
        self._cam.set_exposure(exposure)
        self._lock.release()

    def is_connected(self):
        return self._cam.is_connected()
    
    def get_gain(self):
        return self._cam.get_gain()
    
    def get_exposure(self) -> float:
        return self._cam.get_exposure()
    