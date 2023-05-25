from threading import RLock
from server.imager_manager import ManagerResponse
import os
from imager.imaging_grid import ImagingGrid
from PIL import Image
from stitcher.linear_stitcher import LinearStitcher
from imager.config import (
    GRID_PROPERTIES_FILE_NAME,
    RAW_DATA_DIR_NAME,
    STITCHED_IMAGE_NAME,
)
from base64 import encodebytes
from io import BytesIO
from json import load
import logging

"""
a stitcher manager wraps a stitcher, handling 
logic for checking if the stitcher has 
been initialized with everything it needs 
before it can stitch. Return values are 
of type ManagerResponse, which indicate
if the request succeeded alongside a message
for why the request may not have succeeded

This class is responsible for handling error 
checking
"""


# TODO: use lock decorator
class StitcherManager:
    def __init__(self):
        self._stitcher: LinearStitcher | None = None
        self._path: str | None = None
        self._grid: ImagingGrid | None = None
        self._lock = RLock()

    # True if the stitcher has a valid directory to
    # stitch from
    def is_ready(self) -> bool:
        with self._lock:
            return (
                self._stitcher is not None
                and self._path is not None
                and self._grid is not None
            )

    # configures the stitcher to stitch from path, loading
    # the imaging grid from the stoored grid.json at that path
    def initialize(self, path: str) -> ManagerResponse:
        # note: we always stitch from a directory now, so no need to configure these independently
        with self._lock:
            if not self._is_stitchable_dir(path):
                return (False, f"not something we can stitch from: {path}")
            grid_path = os.path.join(path, GRID_PROPERTIES_FILE_NAME)
            grid = self._load_grid_from_json(grid_path)
            self._stitcher = LinearStitcher(path, grid)
            self._grid = grid
            self._path = path
            return (True, "stitcher initialized")

    def configure(self, theta: float, pixels_per_um: float) -> ManagerResponse:
        with self._lock:
            if not self.is_ready():
                return (False, "stitcher uninitialized")

            self._stitcher.set_params(theta, pixels_per_um)
            return (True, "parameters set")

    # stitches from the configured directory
    def stitch(self) -> ManagerResponse:
        with self._lock:
            if not self.is_ready():
                return (False, "stitcher uninitialized")
            try:
                assert(self._stitcher is not None)
                self._stitcher.run()
                return (True, "stitching complete")
            except Exception as e:
                logging.exception(e)
                return (False, str(e))

    # returns a h x w grid of raw images, fewer if the
    # requested size doesn't adhere to the grid
    def get_manual_grid(self, h, w) -> tuple[bool, dict | str]:
        with self._lock:
            if not self.is_ready():
                return (False, "please initialize the stitcher first")
            try:
                assert self._path is not None

                grid_path = os.path.join(self._path, GRID_PROPERTIES_FILE_NAME)
                grid = self._load_grid_from_json(os.path.join(grid_path))
                images = self._load_tiff_images()

                grid_r, grid_c = grid.get_grid_dimensions()
                h = min(grid_r, h)
                w = min(grid_c, w)

                image_grid = []
                for r in range(h):
                    image_grid_row = []
                    for c in range(w):
                        image_ind = r * grid_c + c
                        if image_ind >= len(images):
                            break
                        image_grid_row.append(self._encode_image(images[image_ind]))
                    image_grid.append(image_grid_row)
                return (True, {"result": image_grid, "grid": grid.get_properties()})

            except Exception as e:
                return (False, str(e))

    def _encode_image(self, image: Image.Image):
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format="PNG")
        return encodebytes(img_byte_arr.getvalue()).decode("ascii")

    # only to be called from get_manual_grid
    def _load_tiff_images(self) -> list[Image.Image]:
        assert self._path is not None
        assert self._stitcher is not None

        images = []
        raw_data_path = os.path.join(self._path, RAW_DATA_DIR_NAME)
        files = os.listdir(raw_data_path)
        files.sort(
            key=self._stitcher._file_comparefun
        )  # TODO: this is a bit messy, maybe we want some global util comparison function

        for file_name in files:
            file_path = os.path.join(raw_data_path, file_name)
            if file_path.endswith(".TIFF"):
                image = Image.open(file_path)
                images.append(image)
        return images
        ...

    # True if the directory only has a raw_data directory and a
    # grid.json
    def _is_stitchable_dir(self, dir: str) -> bool:
        # checks if a dir contains only a raw_data dir and a grid.json
        acceptable = True
        grid_found = False
        data_dir_found = False
        for item in os.listdir(dir):
            abs_path = os.path.join(dir, item)
            if os.path.isfile(abs_path):  # must check absolute path to file
                base_name = os.path.basename(item)
                if (
                    base_name != GRID_PROPERTIES_FILE_NAME
                    and base_name != STITCHED_IMAGE_NAME
                ):
                    acceptable = False
                else:
                    if base_name == GRID_PROPERTIES_FILE_NAME:
                        grid_found = True
            else:
                if os.path.basename(item) != RAW_DATA_DIR_NAME:
                    acceptable = False
                else:
                    data_dir_found = True
        return acceptable and grid_found and data_dir_found

    def _load_grid_from_json(self, json_file_path: str) -> ImagingGrid:
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

