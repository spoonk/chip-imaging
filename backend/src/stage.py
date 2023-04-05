from abc import ABC, abstractmethod

"""
An interface for a microscope stage device
"""

class Stage(ABC):
    """
    A stage is a moveable 2d-plane that can move to specified 
    positions and read the current position.
    A stage's movement commands are all blocking, meaning 
    they will pause the execution of the code until the physical
    movement has finished
    """

    # serialport: which COM port the stage controller is on 
    @abstractmethod
    def __init__(self, serialPort:str):
        pass

    # moves the stage to the absolute position (x,y) where x is left-right
    # y is forward-back and both are measured in steps
    @abstractmethod
    def move_to(self, x: int, y:int):
        pass

    # returns how much the stage moves in a single step (measured in nm / step)
    # steps may differ between each axis
    @abstractmethod
    def get_step_resolution(self) -> tuple[float, float]:
        pass

    # returns an [x, y] tuple representing the coordinates of the center of 
    # the stage. Measure in nm
    @abstractmethod
    def get_current_position(self) -> tuple[float, float]:
        pass