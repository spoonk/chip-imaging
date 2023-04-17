from abc import ABC, abstractmethod
import numpy as np

# camera interface

class Camera(ABC):
    """
    A camera is a device that is capable of taking
    images of the microchip.
    The camera's exposure and gain can be modified via
    setter methods
    """
    #TODO: decide if we want continuous acquisition or not (leave it out for now)
    
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def take_image(self) -> np.ndarray:
        # snap and return an image
        pass

    @abstractmethod
    def set_gain(self, gain: int):
        # sets the amount to scale each pixel 
        # by when taking images. May compromise
        # visual acuity if gain is too high 
        pass
    
    @abstractmethod
    def set_exposure(self, exposure: float):
        # sets the exposure (ms) of the camera
        pass 

    @abstractmethod
    def get_gain(self) -> int:
        pass

    @abstractmethod
    def get_exposure(self) -> float:
        pass
