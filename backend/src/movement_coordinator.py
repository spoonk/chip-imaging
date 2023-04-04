from stage import Stage

class MovementCoordinator():
    """
    A movement coordinator is reponsible for 
    moving the stage so that the camera can see 
    regions of the chip. A coordinator
    is able to define a grid of locations

    """
    def __init__(self, stage: Stage):
        self.__stage = stage