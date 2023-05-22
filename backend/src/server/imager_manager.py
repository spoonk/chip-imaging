import logging
import os
from json import dumps, load
from threading import Lock, Thread
from typing import Tuple
from io import BytesIO
from base64 import encodebytes

from imager.chip_imager import ChipImager
from imager.config import GRID_PROPERTIES_FILE_NAME, RAW_DATA_DIR_NAME
from imager.imaging_grid import ImagingGrid
from stitcher.linear_stitcher import LinearStitcher

"""
An imager manager wraps an imager, allowing 
for concurrent access to the device. The manager
is responsible for guaranteeing that the device
is only executing one process at a time, so it 
will 'reject' any method calls that may interfere
with the current process
"""

# TODO: integrate this, lets us use a message + success flag for each return
ManagerResponse = Tuple[bool, str]  # [success, reason]
busy_message = "device busy"

class ImagerManager:
    # possible device states
    STATUS_IDLE = 0
    STATUS_IMAGING = 1
    STATUS_STITCHING = 2
    status_lut = {
        STATUS_IDLE: "idle",
        STATUS_IMAGING: "imaging",
        STATUS_STITCHING: "stitching", # TODO: unnecessary
    }

    def __init__(self, imager: ChipImager):
        self._imager = imager
        self._status = ImagerManager.STATUS_IDLE

        self._imaging_path: str | None = None

        self._running_thread: Thread | None = None
        self._state_lock: Lock = Lock()


        # TODO: make a stitcher manager
        self._stitcher: LinearStitcher | None = None 
        self._stitch_theta: float = 0.0
        self._stitch_pix_per_um = 1.0

    # change path of where images are saved to and where stitching occurs
    # this must be used before acquiring or stitching
    def set_imaging_output_path(self, path: str) -> ManagerResponse:
        # requires: path must be an existing directory
        with self._state_lock:
            if self._status == ImagerManager.STATUS_IDLE:
                if len(os.listdir(path)) != 0: 
                    return (False, f"{path} is not an empty directory")

                self._imaging_path = path

                """ self._stitcher = LinearStitcher(path, self._imager.get_imaging_grid()) """
                return (True, f'set acquisition path to {path}')
            return (False, busy_message)

    def set_stitching_directory(self, path: str) -> ManagerResponse:
        # side effect: instantiates a stitcher, meaning this method
        # must be called before stitching takes place
        with self._state_lock:
            if self._status == ImagerManager.STATUS_IDLE:
                # TODO: try except
                if not check_stitchable_dir(path):
                    return (False, f"{path} doesn't meet the requirements for stitching")

                grid: ImagingGrid = load_grid_from_json(
                    os.path.join(path, GRID_PROPERTIES_FILE_NAME)
                )

                self._stitcher = LinearStitcher(path, grid)
                return (True, f"{path} saved as stitching directory")
            return (False, busy_message)


    def set_stitching_parameters(self, theta:float, pixels_per_um:float) -> ManagerResponse:
    # NOTE: enforce that we have a stitching path first...
        if self._stitcher is None:
            return (False, "please select a stitching directory first")
        else:
            self._stitcher.set_params(theta, pixels_per_um)
            return (True, "parameters set")

    # change chip parameters
    def change_imaging_parameters(
        self, imaging_width: float, imaging_height: float, distance_between_cells: float
    ) -> ManagerResponse:
        with self._state_lock:
            if self._status == ImagerManager.STATUS_IDLE:
                grid: ImagingGrid = self._imager.get_imaging_grid()
                grid.set_properties(
                    grid.get_cell(0).get_center_location(),  # reuse top left
                    imaging_width,
                    imaging_height,
                    distance_between_cells,
                )

                # NOTE: that updating the grid will still update the stitcher
                return (True, "updated chip parameters")
            return (False, busy_message)

    def save_top_left_position(self) -> ManagerResponse:
        with self._state_lock:
            if self._status == ImagerManager.STATUS_IDLE:
                self._imager.save_top_left_pos() # TODO: error check?
                return (True, "saved top left position")
            return (False, busy_message)

    # tells the device to start snapping images
    # returns True if the request wasn't rejected
    def start_acquisition(self) -> ManagerResponse:
        with self._state_lock:
            if self._imaging_path != None and self._status == ImagerManager.STATUS_IDLE:
                if not self._imager._ready: # TODO: have a get_is_ready function in manager
                    return (False, 'please select imaging parameters first')

                imaging_thread = Thread(
                    target=self._thread_wrapper,
                    args=[self._imager.run_image_acquisition, self._imaging_path],
                )
                imaging_thread.start()

                self._status = ImagerManager.STATUS_IMAGING
                self._running_thread = imaging_thread

                return (True, "acquisition started")
            return (False, busy_message)

    def stitch(self) -> ManagerResponse:
        with self._state_lock:
            if self._stitcher is None:
                return (False, "no stitching directory has been specified")
            if self._status == ImagerManager.STATUS_IDLE:
                # TODO: try except in case running fails
                try:
                    self._stitcher.run()
                    return (True, "stitching complete")
                except Exception as e:
                    return (False, str(e))
            return (False, busy_message)

    def get_status(self):
        with self._state_lock:
            return {
                "status": ImagerManager.status_lut[self._status],
                "data path": self._imaging_path,
            }

    def _thread_wrapper(self, function, args):
        function(args)
        with self._state_lock:
            self._status = ImagerManager.STATUS_IDLE
            self._running_thread = None

    def get_saved_acquisition_path(self):
        return self._imaging_path
    
    def get_saved_stitching_path(self):
        if self._stitcher is None:
            return None
        return self._stitcher._data_path


    def get_manual_grid(self, h, w):
        data_path = self.get_saved_stitching_path()
        if data_path is None:
            return (False, 'please select a directory to stitch from first')
        try: 
            grid = load_grid_from_json(os.path.join(data_path, GRID_PROPERTIES_FILE_NAME))
            images = self._stitcher._load_tiff_images() # TODO: stitcher shouldn't be responsible for loading iamges, that should be done here
            grid_r, grid_c = grid.get_grid_dimensions()
            h = min(grid_r, h)
            w = min(grid_c, w)

            # grab h x w images
            image_grid = []
            for r in range(h):
                image_grid_row = []
                for c in range(w):
                    image_ind = r * grid_c + c
                    if image_ind >= len(images): break
                    image = images[image_ind]

                    img_byte_arr = BytesIO()
                    image.save(img_byte_arr, format="PNG")
                    image_grid_row.append(encodebytes(img_byte_arr.getvalue()).decode("ascii"))
                image_grid.append(image_grid_row)

            return (True, {"result": image_grid, "grid": grid.get_properties()})

        except Exception as e:
            print(estack)
            return (False, str(e))

def check_stitchable_dir(dir_path: str) -> bool:
    # checks if a dir contains only a raw_data dir and a grid.json
    acceptable = True
    grid_found = False
    data_dir_found = False
    for item in os.listdir(dir_path):
        logging.info(item)
        if os.path.isfile(os.path.join(dir_path, item)): # must check absolute path to file
            logging.info('it is a file')
            if os.path.basename(item) != GRID_PROPERTIES_FILE_NAME:
                acceptable = False
            else:
                grid_found = True
        else:
            logging.info('it is a directory')
            if os.path.basename(item) != RAW_DATA_DIR_NAME:
                acceptable = False
            else:
                data_dir_found = True
    logging.info(str([acceptable, grid_found, data_dir_found]))
    return acceptable and grid_found and data_dir_found


def load_grid_from_json(json_file_path: str) -> ImagingGrid:
    grid = ImagingGrid()

    with open(json_file_path) as f:
        grid_json = load(f)
        grid.set_properties(
            top_left=grid_json["top_left"],
            imaging_width=grid_json["width"],
            imaging_height=grid_json["height"],
            distance_between_cells=grid_json["distance"],
        )
        return grid
