from imager.pymmcore_singleton import PymmcoreSingleton
from camera.camera_interface import Camera
import numpy as np
from math import ceil
import logging

class PMMCamera(Camera):
    """
    Generic camera controlled by pymmcore
    """

    def __init__(self):
        self._pymm = PymmcoreSingleton()
        self._core = self._pymm.core
        self._connected = False
        self._gain = 1
        logging.getLogger().info("camera instantiated")

    def connect(self):
        # set the camera to a state where it can take pictures
        self._core.setAutoShutter(False)
        self._core.setShutterOpen(False)
        self._connected = True

    def close(self):
        self._connected = False

    def take_image(self) -> np.array:
        self._core.snapImage()
        im = self._core.getImage()
        self._apply_gain(im)
        return np.array(im)
    
    def set_gain(self, gain: int):
        self._gain = max(gain, 1)

    def set_exposure(self, exposure:float):
        exposure = max(exposure, 0)
        self._core.setExposure(exposure)

    def is_connected(self) -> bool:
        return self._connected
    
    def get_gain(self) -> int:
        return self._gain
    
    def get_exposure(self) -> float:
        return self._core.getExposure()

    def _apply_gain(self, image):
        # @modifies image

        # the extra number of bits we will need to apply 
        # this gain without overflow
        gainFactor = ceil(np.log10(self._gain) / np.log10(2))

        np.clip(image, 0, 2**(16-gainFactor)-1, out=image)
        np.multiply(image, np.array(image)
            .astype(np.float64), out=image, casting='unsafe')