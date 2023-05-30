import logging
from math import ceil
from time import sleep

import numpy as np
from camera.camera_interface import Camera
from PIL import Image



# NOTE: unfortunately, we need to reference some image to be able to mock a camera. 
#       this depends on the computer you are using
mock_image_path = "/home/spoonk/dev/allbritton/chip-imaging/backend/figures/example.TIFF"
# mock_image_path = '/Users/spunk/college/work/chip-imaging/backend/figures/topleft.png'
# mock_image_path = r'C:\Users\Luke\Desktop\chip-imager\chip-imaging\backend\figures\topleft.png'
# mock_image_path = r'C:\Users\Luke\Desktop\chip-imager\chip-imaging\backend\src\demo_images\stitched.TIFF'

"""
A simulated camera to use when not 
testing the code on hardware. 

This camera mimics a live-feed by automatically 
changing the gain. This makes all the images 
not appear the same and indicates that 
there is some feed being streamed
"""
class MockCamera(Camera):

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

    def take_image(self):
        im = Image.open(mock_image_path)
        im = np.array(im)
        self._apply_gain(im)
        sleep(self._exposure / 1000)
        return im

    def set_gain(self, gain: float):
        self._gain = max(gain, 1)

    def set_exposure(self, exposure:float):
        exposure = max(exposure, 0)
        self._exposure = exposure

    def is_connected(self) -> bool:
        return self._connected

    def get_gain(self) -> float:
        return self._gain

    def get_exposure(self) -> float:
        return self._exposure

    def _apply_gain(self, image: np.ndarray):
        if self._gain <= 1.0: self.set_gain(15.0)
        else: self.set_gain(self._gain - 0.1)

        # the extra number of bits we will need to apply 
        # this gain without overflow
        gainFactor = ceil(np.log10(self._gain) / np.log10(2))

        np.clip(image, 0, 2**(16-gainFactor)-1, out=image)
        np.multiply(image, np.array(self._gain)
                    .astype(np.float64), out=image, casting='unsafe')
