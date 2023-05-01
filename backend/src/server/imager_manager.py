
from imager.chip_imager import ChipImager

"""
An imager manager wraps an imager, allowing 
for concurrent access to the device. The manager
is responsible for guaranteeing that the device
is only executing one process at a time, so it 
will 'reject' any method calls that may interfere
with the current process
"""

# STATUS_IDLE = 0
# STATUS_IMAGING = 1
# STATUS_STITCHING = 3

class ImagerManager():
    STATUS_IDLE = 0
    STATUS_IMAGING = 1
    STATUS_STITCHING = 3
    
    def __init__(self, imager: ChipImager):
        self._imager = imager
        self._status = ImagerManager.STATUS_IDLE
        self._imaging_path = None

    # edit chip parameters

    # change path of where images are saved to

    # 