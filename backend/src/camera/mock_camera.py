from camera.camera_interface import Camera
import logging
import numpy as np
from math import ceil
from PIL import Image


""" mock_image_path = "../../figures/topleft.png" """

mock_image_path = "/home/spoonk/dev/allbritton/chip-imaging/backend/figures/topleft.png"
class MockCamera(Camera):


    """mock camera used for testing without a connection to hardware"""
    def __init__(self):
        logging.info('camera instantiated')
        self._gain = 1
        self._exposure = 1
        self._connected = False

    def connect(self):
        logging.info('camera instantiated')
        self._connected = True

    def close(self):
        logging.info('camera instantiated')
        self._connected = False

    def take_image(self) -> np.array:
        im = Image.open(mock_image_path)
        im = np.array(im)
        self._apply_gain(im)
        return im

    def set_gain(self, gain: int):
        self._gain = max(gain, 1)

    def set_exposure(self, exposure:float):
        exposure = max(exposure, 0)
        self._exposure = exposure

    def is_connected(self) -> bool:
        return self._connected

    def get_gain(self) -> int:
        return self._gain

    def get_exposure(self) -> float:
        return self._exposure

    def _apply_gain(self, image: np.array):
        if self._gain < 10: self.set_gain(100)
        else: self.set_gain(self._gain - 1)

        # the extra number of bits we will need to apply 
        # this gain without overflow
        gainFactor = ceil(np.log10(self._gain) / np.log10(2))

        np.clip(image, 0, 2**(16-gainFactor)-1, out=image)
        np.multiply(image, np.array(self._gain)
                    .astype(np.float64), out=image, casting='unsafe')
