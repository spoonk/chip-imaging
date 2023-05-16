from imager.imaging_grid import ImagingGrid
from imager.chip_imager import ChipImager
from threading import Thread, Lock
from stitcher.linear_stitcher import LinearStitcher
from stitcher.cv_stitcher import CVStitchPipeline
import logging

"""
An imager manager wraps an imager, allowing 
for concurrent access to the device. The manager
is responsible for guaranteeing that the device
is only executing one process at a time, so it 
will 'reject' any method calls that may interfere
with the current process
"""

class ImagerManager():
    # possible device states
    STATUS_IDLE = 0
    STATUS_IMAGING = 1
    STATUS_STITCHING = 2
    status_lut = {
        STATUS_IDLE: "idle",
        STATUS_IMAGING: "imaging",
        STATUS_STITCHING: "stitching",
    }

    def __init__(self, imager: ChipImager):
        self._imager = imager
        self._status = ImagerManager.STATUS_IDLE

        self._imaging_path: str | None = None
        self._running_thread: Thread | None = None
        self._state_lock: Lock = Lock()

        # self._stitcher: LinearStitcher | None = None
        self._stitcher: CVStitchPipeline | None = None

    # change path of where images are saved to and where stitching occurs
    # this must be used before acquiring or stitching
    def set_imaging_output_path(self, path:str) -> bool:
        # requires: path must be an existing directory
        with self._state_lock:
            if self._status == ImagerManager.STATUS_IDLE:
                self._imaging_path = path
                self._stitcher = CVStitchPipeline(path)
                # self._stitcher = LinearStitcher(path, self._imager.get_imaging_grid())
                return True
            return False

    # change chip parameters
    def change_imaging_parameters(self, imaging_width: float, imaging_height: float, 
                                  distance_between_cells: float) -> bool:
        with self._state_lock:
            if self._status == ImagerManager.STATUS_IDLE:
                grid:ImagingGrid = self._imager.get_imaging_grid()
                grid.set_properties(
                    grid.get_cell(0).get_center_location(), # reuse top left
                    imaging_width,
                    imaging_height,
                    distance_between_cells,
                    grid.get_pixels_per_um())

                # note that updating the grid will still update the stitcher
                return True
            return False

    def save_top_left_position(self):
        with self._state_lock:
            if self._status == ImagerManager.STATUS_IDLE:
                self._imager.save_top_left_pos()
                return True
            return False

    # tells the device to start snapping images
    # returns True if the request wasn't rejected
    def start_acquisition(self) -> bool:
        with self._state_lock:
            if self._imaging_path != None and self._status == ImagerManager.STATUS_IDLE:
                # start the device
                imaging_thread = Thread(target = self._thread_wrapper, args=[self._imager.run_image_acquisition, self._imaging_path])
                imaging_thread.start()

                self._status = ImagerManager.STATUS_IMAGING
                self._running_thread = imaging_thread

                return True
            return False

    def stitch(self):
        with self._state_lock:
            if self._imaging_path != None: return False # implies stitcher is None
            if self._status == ImagerManager.STATUS_IDLE:
                imaging_thread = Thread(target = self._thread_wrapper, args=[self._stitcher.run, self._imaging_path])
                imaging_thread.start()

                self._status = ImagerManager.STATUS_STITCHING
                self._running_thread = imaging_thread

                return True
            return False

    def get_status(self):
        with self._state_lock:
            return {"status":
                    ImagerManager.status_lut[self._status], 
                    "data path": self._imaging_path}

    def _thread_wrapper(self, function, args):
        function(args)
        logging.info('done acquiring')
        with self._state_lock:
            self._status = ImagerManager.STATUS_IDLE
            self._running_thread = None

    # @TODO: also return imaging grid
    def get_top_left_grid(self, w, h):
        # images = self._stitcher._load_tiff_images()
        self._stitcher._generate_jpeg_from_tiff()
        images = self._stitcher._load_jpeg_images()

        # images = self._stitcher._load_tiff_images()
        grid = self._imager.get_imaging_grid()
        r, c = grid.get_grid_dimensions()
        if r < h or c < w: return None
        # for now we will know nothing about the location of the images 
        top_lefties = []
        for row in range(h):
            row_images = []
            for col in range(w): 
                row_images.append(images[row * w + col])

            top_lefties.append(row_images)
        return top_lefties

    def get_saved_path(self):
        return self._imaging_path

