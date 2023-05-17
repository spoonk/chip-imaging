# top-level class :)
from stage.stage_interface import Stage
from camera.camera_interface import Camera
from imager.imaging_grid import ImagingGrid
from PIL import Image
from imager.movement_coordinator import MovementCoordinator
from imager.config import CAMERA_WAIT_DURATION, RAW_DATA_DIR_NAME, GRID_PROPERTIES_FILE_NAME
from time import sleep
from os import path, makedirs
from json import dump

import logging

class ChipImager():
    """
    Chip imager takes control of a stage and camera.
    It maintains an imaging grid that can be retrieved
    and modified by the client to update the 
    imaging step
    """

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

    def run_image_acquisition(self, acquisition_path:str):
        # runs through the entire process of scanning the chip and saving images
        if not self._ready: return
        if not path.exists(acquisition_path): return
        # save the imaging grid used for this 

        self._movement.reset()

        image_num = 1
        while self._movement.has_next_location():
            self._movement.move_to_next_location()
            sleep(CAMERA_WAIT_DURATION)

            image = self._camera.take_image()

            sleep(CAMERA_WAIT_DURATION)
            self._save_image(image, acquisition_path, f"{str(image_num)}.TIFF")
            logging.getLogger().info(f"saved image {str(image_num)}")
            image_num += 1

        logging.info(f"finished snapping images, check {acquisition_path}")

    def save_top_left_pos(self):
        # saves the current position as the top left corner of the microchip
        # This will be the initial position of the scan
        pos = self._stage.get_current_position()

        logging.getLogger().info(f"saving {pos[0]}, {pos[1]} as top-left position")
        self._grid.set_top_left(pos)
        self._ready = True
    
    def _save_image(self, image, acquisition_path:str, image_name:str):
        raw_image_dir = self._handle_data_dir(acquisition_path)

        "saves this image to the target directory"
        pilIm = Image.fromarray(image) 
        pilIm.save(path.join(raw_image_dir, image_name))


    def _handle_data_dir(self, parent_directory_path: str):
        data_dir:str = path.join(parent_directory_path, RAW_DATA_DIR_NAME)
        if not path.exists(data_dir):
           makedirs(data_dir) 
        return data_dir


    def _save_grid(self, acquisition_path: str):
        # saves the properties of a grid in a file called 'grid.json'
        grid_properites = self._grid.get_properties()
        file_name = path.join(acquisition_path, GRID_PROPERTIES_FILE_NAME)
        # jsonified = dumps(grid_properites)
        with open(file_name, 'w') as f:
            dump(grid_properites, f)
        
