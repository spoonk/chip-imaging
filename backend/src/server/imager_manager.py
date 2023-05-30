import logging
import os
from base64 import encodebytes
from io import BytesIO
from json import dumps, load
from threading import Lock, Thread
from typing import Tuple

from imager.chip_imager import ChipImager
from imager.config import GRID_PROPERTIES_FILE_NAME, RAW_DATA_DIR_NAME
from imager.imaging_grid import ImagingGrid
from stitcher.linear_stitcher import LinearStitcher

"""
An imager manager wraps an imager, handling 
concurrent access to the device. The manager
is responsible for guaranteeing that the device
is only executing one process at a time, so it 
will 'reject' any method calls that may interfere
with the current process

Most return values from the manager take the following form:
[success: bool, data: str]
Success indicates if the request was rejected or not.
If the request was rejected, data will be a string explanation for why 
it was rejected. If not, it will be some success message
"""

ManagerResponse = Tuple[bool, str]  # [success, reason]
busy_message = "device busy"

class ImagerManager:
    # possible device states
    STATUS_IDLE = 0
    STATUS_IMAGING = 1
    status_lut = {
        STATUS_IDLE: "idle",
        STATUS_IMAGING: "imaging",
    }

    def __init__(self, imager: ChipImager):
        self._imager = imager
        self._status = ImagerManager.STATUS_IDLE
        self._imaging_path: str | None = None
        self._running_thread: Thread | None = None
        self._state_lock: Lock = Lock()

    # change path of where images are saved to
    # this must be set before acquiring
    # requires: path must be an existing directory
    # requires: path is an empty directory
    def set_imaging_output_path(self, path: str) -> ManagerResponse:
        with self._state_lock:
            if self._status == ImagerManager.STATUS_IDLE:
                if len(os.listdir(path)) != 0:
                    return (False, f"{path} is not an empty directory")

                self._imaging_path = path
                return (True, f"set acquisition path to {path}")
            return (False, busy_message)

    # change the parameters used for image acquisition
    # width: how many um the resulting stitched image will span horizontally
    # height: how many um the resulting stitched image will span vertically
    # distance: um between the center of adjacent images
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

                return (True, "updated chip parameters")
            return (False, busy_message)

    # saves the current position of the stage as 
    # the one in which the top-left corner of the 
    # chip is visible to the camera
    def save_top_left_position(self) -> ManagerResponse:
        with self._state_lock:
            if self._status == ImagerManager.STATUS_IDLE:
                self._imager.save_top_left_pos()  # TODO: error check?
                return (True, "saved top left position")
            return (False, busy_message)

    # tells the device to start snapping images
    def start_acquisition(self) -> ManagerResponse:
        # this function is threaded so the server may respond quickly
        with self._state_lock:
            if self._imaging_path != None and self._status == ImagerManager.STATUS_IDLE:
                if (
                    not self._imager._ready
                ):  # TODO: have a get_is_ready function in manager
                    return (False, "please select imaging parameters first")

                imaging_thread = Thread(
                    target=self._thread_wrapper,
                    args=[self._imager.run_image_acquisition, self._imaging_path],
                )
                imaging_thread.start()

                self._status = ImagerManager.STATUS_IMAGING
                self._running_thread = imaging_thread

                return (True, "acquisition started")
            return (False, busy_message)

    # returns a dictionary of the devices current state 
    # and the path that is being used for data acquisition
    def get_status(self) -> dict[str, str | None]:
        with self._state_lock:
            return {
                "status": ImagerManager.status_lut[self._status],
                "data path": self._imaging_path,
            }

    # helper method to run a process asynchronously
    # and that performs cleanup when the function finishes
    def _thread_wrapper(self, function, args):
        function(args)
        with self._state_lock:
            self._status = ImagerManager.STATUS_IDLE
            self._running_thread = None

    def get_saved_acquisition_path(self):
        return self._imaging_path

