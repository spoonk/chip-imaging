# top-level clas :)
from stage import Stage
from camera import Camera
from imaging_grid import ImagingGrid

class ChipImager():

    def __init__(self, stage: Stage, camera: Camera):
        pass


    def get_imaging_grid(self) -> ImagingGrid:
        # returns a reference to the imaging grid to allow 
        # the client to configure the imaging session
        pass


