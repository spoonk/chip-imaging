from stitcher.stitch_pipeline_interface import StitchPipeline
from imager.imaging_grid import ImagingGrid
from os import listdir, path
from PIL import Image, ImageDraw
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
        total_height_um = self._compute_image_height_um()

        pixels_y = int(self.um_to_pixels(total_height_um))
        pixels_x = int(self.um_to_pixels(total_width_um))

        canvas:Image = Image.new('I;16',  size=(pixels_x, pixels_y))

        return canvas

        # for image in images:

    def _paste_images_into_canvas(self, canvas, images):
        # pre: images must be sorted by increasing file name
        # uses the image grid to determine where to paste the images in the canvas
        top_left = self._grid.get_cell(0).get_center_location()
        center_offset = (0, 0) # shift x and y by the width of the image / 2, height / 2
        # y_shift = -18
        # x_shift = 5
        y_shift = 0
        x_shift = 0

        grid_dims = self._grid.get_grid_dimensions()

        for i in range(len(images)):
            image = images[i]
            # compute pixel coords of where this image's center should go
            image_center_um = self._grid.get_cell(i).get_center_location()
            image_center_px = (self.um_to_pixels(image_center_um[0]), self.um_to_pixels(image_center_um[1]))
            image_center_px = list(image_center_px)

            image_center_px[0] = int(abs(image_center_px[0])) + (x_shift * (i // grid_dims[0]))
            image_center_px[1] = int(abs(image_center_px[1])) + (y_shift * (i % grid_dims[1]))

            # image_center_px[0] += -top_left[0] + center_offset[0]
            # image_center_px[1] += -top_left[1] + center_offset[1]

            # image_center_px[0] = int(image_center_px[0])
            # image_center_px[1] = int(image_center_px[1])


            print(image_center_px)
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
        total_width_um += abs(self.pixel_to_um(CAMERA_RESOLUTION[0])) # add one more image of width
        return total_width_um
    
    def _compute_image_height_um(self):
        rows, cols = self._grid.get_grid_dimensions()

        tl_image_center = self._grid.get_cell(0).get_center_location()
        br_image_center = self._grid.get_cell(rows * cols - 1).get_center_location()

        total_height_um = abs(br_image_center[1] - tl_image_center[1])
        total_height_um += self.pixel_to_um(CAMERA_RESOLUTION[1])
        return total_height_um

    def pixel_to_um(self, pixels:float):
        # computes the number um spanned by pixels pixels
        return pixels * (1./self._grid.get_pixels_per_um())

    def um_to_pixels(self, um:float):
        # computes the number pixels spanned by um um
        return um * self._grid.get_pixels_per_um()

    def _load_tiff_images(self):
        # loads and returns a list of tiff images
        images = []
        files = listdir(self._data_path)
        files.sort(key=self._file_comparefun)

        for file_name in files:
            file_path = path.join(self._data_path, file_name)
            if file_path.endswith(".TIFF"):
                # use this file
                image = Image.open(file_path)
                draw = ImageDraw.Draw(image, 'I;16') 
                # draw.line((0,0, image.width - 1, 0), fill=0, width=20)
                # draw.line((0,0, 0, image.height - 1), fill=0, width=20)
                images.append(image)

        return images

    def _file_comparefun(self, file_name):
        # sorts files named {number}.{extension} by increasing 
        # number where number is some decimal value
        no_ext = file_name.split(".jpeg")[0].split(".TIFF")[0]
        return int(no_ext)