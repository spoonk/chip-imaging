# top-level class :)
from stage.stage_interface import Stage
from camera.camera_interface import Camera
from imager.imaging_grid import ImagingGrid
from PIL import Image
from imager.movement_coordinator import MovementCoordinator
# from imager import device
from os import path
from time import sleep
from imager.config import CAMERA_WAIT_DURATION

import logging

class ChipImager():
    """
    Chip imager takes control of a stage and camera.
    It maintains an imaging grid that can be retrieved
    and modified by the client to update the 
    imaging step
    """

    # TODO: maybe this should connect the devices (probably not)

    def __init__(self, stage: Stage, camera: Camera):
        self._camera: Camera = camera
        self._stage: Stage = stage
        self._grid: ImagingGrid = ImagingGrid()
        self._ready = False

        self._movement: MovementCoordinator = MovementCoordinator(self._stage, self._grid)

    def get_imaging_grid(self) -> ImagingGrid:
        # returns a reference to the imaging grid to allow 
        # the client to configure the imaging session
        return self._grid

    def run_image_acquisition(self, data_directory_path:str):
        # runs through the entire process of scanning the chip and saving images
        if not self._ready: return
        if not path.exists(data_directory_path): return

        self._movement.reset()

        image_num = 1
        while self._movement.has_next_location():
            # print(self._movement.has_next_location())
            self._movement.move_to_next_location()
            sleep(CAMERA_WAIT_DURATION)
            image = self._camera.take_image()
            sleep(CAMERA_WAIT_DURATION)
            self._save_image(image, data_directory_path, f"{str(image_num)}.TIFF")
            logging.getLogger().info(f"saved image {str(image_num)}")
            image_num += 1

        logging.getLogger().info(f"finished snapping images, check {data_directory_path}")

    def save_top_left_pos(self):
        # saves the current position as the top left corner of the microchip
        # This will be the initial position of the scan
        pos = self._stage.get_current_position()

        logging.getLogger().info(f"saving {pos[0]}, {pos[1]} as top-left position")
        self._grid.set_top_left(pos)
        self._ready = True
    
    def _save_image(self, image, data_directory_path:str, image_name:str):
        # @requires pah exists
        "saves this image to the target directory"
        pilIm: Image = Image.fromarray(image) 
        pilIm.save(path.join(data_directory_path, image_name))
        pass