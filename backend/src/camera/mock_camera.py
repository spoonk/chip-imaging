from camera_interface import Camera
import logging
import numpy as np
from math import ceil
from PIL import Image


mock_image_path = "../../figures/topleft.png"

class MockCamera(Camera):


    """mock camera used for testing without a connection to hardware"""
    def __init__(self):
        logging.info('camera instantiated')

    def connect(self):
        logging.info('camera instantiated')
        self._connected = True

    def close(self):
        logging.info('camera instantiated')
        self._connected = False

    def take_image(self) -> np.array:
        im = Image.open(mock_image_path)
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

