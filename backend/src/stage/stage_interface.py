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

    @abstractmethod
    def __init__(self):
        pass

    # moves the stage to the absolute position (x,y) where x is left-right
    # y is forward-back and both are measured in um
    @abstractmethod
    def move_to(self, x: float, y:float):
        pass

    # returns an [x, y] tuple representing the coordinates of the center of 
    # the stage. Measure in um
    @abstractmethod
    def get_current_position(self) -> tuple[float, float]:
        pass