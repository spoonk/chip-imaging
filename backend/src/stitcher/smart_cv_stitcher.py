from stitcher.stitch_pipeline_interface import StitchPipeline
from imager.imaging_grid import ImagingGrid

import cv2 
import numpy as np
import os
from PIL import Image

class SmartCVStitcher(StitchPipeline):
    """
    A pipeline that uses opencv to stitch images together.
    Does the stitching in batches defined by an ImagingGrid
    in order to reduce the used memory
    """

    def __init__(self, tiff_images_dir_path: str, image_grid: ImagingGrid):
        # TODO: make a copy of the grid (elsewhere)
        self._grid = image_grid
        self._result = None
        self._data_path = tiff_images_dir_path
    
    def run(self):
        # divide the data into a bunch of 4 x 1 image chunks 
        self._generate_jpeg_from_tiff()
        images = self._load_jpeg_images()
        return self._smart_stitch_images(images)
        # self._delete_temp_jpegs()

    def get_stitch_result(self):
        return self._result

    def save_stitch_result(self, save_dir_path: str):
        # TODO: !!!!! (lazy rn)
        pass


    def _smart_stitch_images(self, images):

        # make an array of rows, where each row has a list of at most 2 imaging locations
        row_chunks = self._get_row_chunks(images, 2)
        for row in row_chunks:
            print(f"row length {len(row)}")
            for chunk in row:
                print(len(chunk))

        # stitch just those chunks, replacing the chunk with the stitched result
        row_chunks = [row_chunks[0]]
        stitched_row_chunks = self._get_stitched_row_chunks(row_chunks)

        stitched_row = self._get_stitched_rows(stitched_row_chunks)

        full_image = self._stitch_images(stitched_row)
        return full_image

    def _get_row_chunks(self, images, num_per_chunk):
        rows, cols = self._grid.get_grid_dimensions()
        image_index = 0
        row_chunks = []
        for row in range(rows):
            chunks = []
            chunk = []
            in_chunk = 0
            for col in range(cols):
                if image_index == len(images): break
                chunk.append(images[image_index])
                image_index += 1
                in_chunk += 1
                if (in_chunk == num_per_chunk) or (col == cols - 1):
                    chunks.append(chunk)
                    chunk = []
                    in_chunk = 0

            if len(chunks) != 0:
                row_chunks.append(chunks)
        return row_chunks
    
    def _get_stitched_row_chunks(self, row_chunks):
        # stitch each row's chunks into an image
        # a row with 3 chunks gets 3 images
        stitched_chunks = []
        for row in row_chunks:
            row_stitches = [] 
            for chunk in row:
                if len(chunk) != 1:
                    # stitch the images in this chunk together
                    stitched = self._stitch_images(chunk)
                    row_stitches.append(stitched)
                else:
                    row_stitches.append(chunk[0])
            stitched_chunks.append(row_stitches)

        return stitched_chunks
    
    def _get_stitched_rows(self, row_stitches):
        # rows: a list of lists of images
        # the result will be a list where each row is a full image
        row_images = []
        for row in row_stitches:
            # a list of images
            stitched_row = self._stitch_images(row)
            row_images.append(stitched_row)
        
        return row_images

    def _stitch_images(self, images):
        stitcher = cv2.Stitcher_create(cv2.Stitcher_SCANS)
        print(images[0].shape)

        status, result = stitcher.stitch(images)
        if status != cv2.Stitcher_OK:
                for img in images:
                    im = Image.fromarray(img)
                    im.show()
                print("Can't stitch images, error code = %d" % status)
        return result
    
    
    def _comparefun(self, file_name):
        no_ext = file_name.split(".jpeg")[0].split(".TIFF")[0]
        return int(no_ext)

    def _generate_jpeg_from_tiff(self):
        # helper function to produce a jpeg image 
        # from each tiff image
        files = os.listdir(self._data_path)
        files.sort(key=self._comparefun)

        for file_name in files:
            if file_name.endswith(".TIFF"):
                in_file_path = os.path.join(self._data_path, file_name)
                file_name = in_file_path.split(".TIFF")[0]
                out_file_path = file_name + ".jpeg"
                image = Image.open(in_file_path)

                image.mode = 'I'
                image.point(lambda i:i*(1./256)).convert('L').save(out_file_path)

    def _load_jpeg_images(self):
        images = []
        files = os.listdir(self._data_path)
        files.sort(key=self._comparefun)

        for file_name in files:
            if file_name.endswith(".jpeg"):
                file_path = os.path.join(self._data_path, file_name)
                image = cv2.imread(file_path)
                images.append(image)

        images = np.array(images)
        return images
    
    def _delete_temp_jpegs(self):
        for file_name in os.listdir(self._data_path):
            if file_name.endswith(".jpeg"):
                os.remove(os.path.join(self._data_path, file_name))
