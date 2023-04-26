from stitcher.stitch_pipeline_interface import StitchPipeline
from imager.imaging_grid import ImagingGrid
from os import listdir, join
from PIL import Image
from imager.config import CAMERA_RESOLUTION

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

    def run(self):
        # load images
        images = self._load_tiff_images()
        # figure out each image's center (via imaging grid's get cell)

        # convert those centers to pixel locations

        # paste the images into a canvas based off of their offset
        
        pass

    def get_stitch_result(self):
        
        pass
    
    def save_stitch_result(self, save_dir_path: str):

        pass

    def _stitch_images(self, images):
        total_width_um = self._compute_image_width_um()

        canvas:Image = Image.new()

        # for image in images:

    def _compute_image_width_um(self):
        rows, cols = self._grid.get_grid_dimensions()
        # determine the total width of the canvas that will be needed
        # (assume at least 1 image)

        # the centers of the leftmost and rightmost images in um
        tl_image_center = self._grid.get_cell(0).get_center_location()
        tr_image_center = self._grid.get_cell(cols - 1).get_center_location()

        total_width_um = tr_image_center[0] - tl_image_center[0] + self.pixel_to_um(CAMERA_RESOLUTION[0])
        return total_width_um

    def pixel_to_um(self, pixels:float):
        # computes the number um spanned by pixels pixels
        return pixels * (1./self._grid.get_pixels_per_um())

    def _load_tiff_images(self):
        # loads and returns a list of tiff images
        images = []
        files = listdir(self._data_path)
        files = files.sort(key=self._file_comparefun)

        for file_name in files:
            file_path = join(self._data_path, file_name)
            if file_path.endswith(".TIFF"):
                # use this file
                image = Image.open(file_path)
                images.append(image)

        return images

    def _file_comparefun(self, file_name):
        # sorts files named {number}.{extension} by increasing 
        # number where number is some decimal value
        no_ext = file_name.split(".jpeg")[0].split(".TIFF")[0]
        return int(no_ext)