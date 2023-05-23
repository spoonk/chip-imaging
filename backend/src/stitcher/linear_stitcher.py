import logging
from os import listdir, path

import numpy as np
from imager.config import (CAMERA_RESOLUTION, RAW_DATA_DIR_NAME,
                           STITCHED_IMAGE_NAME)
from imager.imaging_grid import ImagingGrid
from PIL import Image, ImageDraw
from stitcher.stitch_pipeline_interface import StitchPipeline


class LinearStitcher(StitchPipeline):
    """
    A linear stitcher uses information about
    the size of pixels as well as the imaging
    grid to paste pictures next to each other
    """

    def __init__(self, tiff_images_dir_path: str, grid: ImagingGrid):
        # use imaging grid to determine layout of each image
        self._data_path = tiff_images_dir_path
        self._grid = grid
        # todo: deprecate dx and dy, only using theta pls
        self._theta = 0.0
        self._pix_per_um = 1.0

    def run(self):
        print(self._theta, self._pix_per_um)
        # load images
        images = self._load_tiff_images()
        # figure out each image's center (via imaging grid's get cell)
        result = self._stitch_images(images)
        # convert those centers to pixel locations
        result.save(path.join(self._data_path, STITCHED_IMAGE_NAME))

    def get_stitch_result(self):
        pass

    def set_xy_shift(self, x_shift, y_shift):
        self._dx = x_shift
        self._dy = y_shift

    def set_params(self, theta: float, pix_per_um: float):
        self._theta = theta
        self._pix_per_um = pix_per_um

    def _stitch_images(self, images):
        total_width_um = self._compute_image_width_um()
        total_height_um = self._compute_image_height_um()

        pixels_y = int(self.um_to_pixels(total_height_um))
        pixels_x = int(self.um_to_pixels(total_width_um))

        canvas = Image.new("I;16", size=(pixels_x, pixels_y))

        # shift_factor = (0.009) * self._grid.get_distance_between_images_um()
        # to make math easier, set the center location of the grid to be (0,0)
        # undo the transformation to the grid when done

        top_left = self._grid.get_cell(0).get_center_location()
        self._grid.set_top_left((0, 0))
        canvas = self._paste_images_into_canvas(canvas, images)
        self._grid.set_top_left(top_left)

        return canvas

    def _paste_images_into_canvas(self, canvas, images):
        # @modifies: canvas
        # pre: images must be sorted by increasing file name
        # uses the image grid to determine where to paste the images in the canvas
        rot = np.matrix(
            [
                [np.cos(self._theta), -np.sin(self._theta)],
                [np.sin(self._theta), np.cos(self._theta)],
            ]
        )

        # center of image with rotation applied
        first_image_center_offset = (
            (self._pix_per_um)
            * rot
            * (np.matrix([self._grid.get_distance_between_images_um(), 0]).T)
        )

        # === weird
        projected_x = self._pix_per_um * self._grid.get_distance_between_images_um()
        projected_y = 0.0

        x_shift = first_image_center_offset[0] - projected_x

        y_shift = first_image_center_offset[1] - projected_y

        # === weird

        grid_dims = self._grid.get_grid_dimensions()
        # for i in range(len(images))[::-1]:
        for i in range(len(images)):
            image = images[i]
            image_center_um = self._grid.get_cell(i).get_center_location()
            rotated_center_pix = self._pix_per_um * rot * (np.matrix([image_center_um[0], image_center_um[1]]).T)
            projected_x = self._pix_per_um * image_center_um[0]
            x_shift = rotated_center_pix[0] - projected_x
            print(x_shift)
            # compute pixel coords of where this image's center should go


            image_center_px = (
                self.um_to_pixels(image_center_um[0]),
                self.um_to_pixels(image_center_um[1]),
            )
            image_center_px = list(image_center_px)

            image_center_px[0] = int(abs(image_center_px[0])) - ( # TODO: ??? (originally +)
                x_shift * (i // grid_dims[0])
            )
            image_center_px[1] = int(abs(image_center_px[1])) + (
                y_shift * (i % grid_dims[1])
            )

            # image_center_px[0] += -top_left[0] + center_offset[0]
            # image_center_px[1] += -top_left[1] + center_offset[1]

            image_center_px[0] = int(image_center_px[0])
            image_center_px[1] = int(image_center_px[1])

            logging.info(image_center_px)
            canvas.paste(image, image_center_px)

        return canvas

    def _compute_image_width_um(self):
        _, cols = self._grid.get_grid_dimensions()
        # determine the total width of the canvas that will be needed
        # (assume at least 1 image)

        # the centers of the leftmost and rightmost images in um
        tl_image_center = self._grid.get_cell(0).get_center_location()
        tr_image_center = self._grid.get_cell(cols - 1).get_center_location()

        total_width_um = tr_image_center[0] - tl_image_center[0]
        total_width_um += abs(
            self.pixel_to_um(CAMERA_RESOLUTION[0])
        )  # add one more image of width
        return total_width_um

    def _compute_image_height_um(self):
        rows, cols = self._grid.get_grid_dimensions()

        tl_image_center = self._grid.get_cell(0).get_center_location()
        br_image_center = self._grid.get_cell(rows * cols - 1).get_center_location()

        total_height_um = abs(br_image_center[1] - tl_image_center[1])
        total_height_um += self.pixel_to_um(CAMERA_RESOLUTION[1])
        return total_height_um

    def pixel_to_um(self, pixels: float):
        # computes the number um spanned by pixels pixels
        return pixels * (1.0 / self._pix_per_um)

    def um_to_pixels(self, um: float):
        # computes the number pixels spanned by um um
        return um * self._pix_per_um

    def _load_tiff_images(self):
        # loads and returns a list of tiff images
        images = []
        raw_data_path = path.join(self._data_path, RAW_DATA_DIR_NAME)
        files = listdir(raw_data_path)
        files.sort(key=self._file_comparefun)

        for file_name in files:
            file_path = path.join(raw_data_path, file_name)
            if file_path.endswith(".TIFF"):
                image = Image.open(file_path)
                images.append(image)
        return images

    def _file_comparefun(self, file_name):
        # sorts files named {number}.{extension} by increasing
        # number where number is some decimal value
        no_ext = file_name.split(".jpeg")[0].split(".TIFF")[0]
        return int(no_ext)

    def get_path(self):
        return self._data_path
