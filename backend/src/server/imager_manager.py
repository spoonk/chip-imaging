from imager.imaging_grid import ImagingGrid
from imager.chip_imager import ChipImager
from camera.camera_interface import Camera
from stage.stage_interface import Stage
from threading import Thread, Lock
from stitcher.linear_stitcher import LinearStitcher

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
    
    def __init__(self, imager: ChipImager):
        self._imager = imager
        self._status = ImagerManager.STATUS_IDLE

        self._imaging_path: str = None
        self._running_thread: Thread = None
        self._state_lock: Lock = Lock()

        self._stitcher: LinearStitcher = None

    # change path of where images are saved to and where stitching occurs
    # this must be used before acquiring or stitching
    def set_imaging_output_path(self, path:str) -> bool:
        # requires: path must be an existing directory
        with self._state_lock:
            if self._stitcher == None: return False
            if self._status == ImagerManager.STATUS_IDLE:
                self._imaging_path = path
                self._stitcher = LinearStitcher(path, self._imager.get_imaging_grid())

                return True
            return False

    # change chip parameters
    def change_imaging_parameters(self, top_left: tuple[float, float], 
            imaging_width: float, imaging_height: float, 
            distance_between_cells: float, pixel_size_um: float) -> bool:

        with self._state_lock:
            if self._status == ImagerManager.STATUS_IDLE:
                grid:ImagingGrid = self._imager.get_imaging_grid()
                grid.set_properties(
                    top_left,
                    imaging_width,
                    imaging_height,
                    distance_between_cells,
                    pixel_size_um)
                
                # note that updating the grid will still update the stitcher
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
            return self._status
        
    def _thread_wrapper(self, function, args):
        function(args)
        with self._state_lock:
            self._status = ImagerManager.STATUS_IDLE
            self._running_thread = None