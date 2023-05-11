import cv2
import numpy as np
from PIL import Image
import os

from stitcher.stitch_pipeline_interface import StitchPipeline

class CVStitchPipeline(StitchPipeline):
    """
    opencv powered pipeline for stitching images together
    """

    def __init__(self, tiff_images_dir_path):
        self._data_path = tiff_images_dir_path
        self._result = None

    def run(self):
        self._generate_jpeg_from_tiff()
        images = self._load_jpeg_images()
        self._stitch_images(images)
        # self._delete_temp_jpegs()

    def get_stitch_result(self):
        return self._result

    def save_stitch_result(self, save_dir_path: str):
        # TODO: !!!!! (lazy rn)
        pass

    def _stitch_images(self, images):
        stitcher = cv2.Stitcher_create(cv2.Stitcher_SCANS)
        print(images[0].shape)

        status, result = stitcher.stitch(images)
        if status != cv2.Stitcher_OK:
                print("Can't stitch images, error code = %d" % status)
        
        self._result = result
    
    def _generate_jpeg_from_tiff(self):
        # helper function to produce a jpeg image 
        # from each tiff image
        files = os.listdir(self._data_path)
        files.sort(key=self._file_comparefun)
        for file_name in files:
            if file_name.endswith(".TIFF"):
                in_file_path = os.path.join(self._data_path, file_name)
                out_file_path = in_file_path.split(".TIFF")[0] + ".jpeg"
                image = Image.open(in_file_path)

                image.mode = 'I'
                image.point(lambda i:i*(1./256)).convert('L').save(out_file_path)

    def _file_comparefun(self, file_name):
        # sorts files named {number}.{extension} by increasing 
        # number where number is some decimal value
        no_ext = file_name.split(".jpeg")[0].split(".TIFF")[0]
        return int(no_ext)

    def _load_jpeg_images(self):
        images = []
        files = os.listdir(self._data_path)
        files.sort(key=self._file_comparefun)

        for file_name in files:
            if file_name.endswith(".jpeg"):
                file_path = os.path.join(self._data_path, file_name)
                image = Image.open(file_path)
                # image = cv2.imread(file_path)
                images.append(image)

        # images = np.array(images)
        return images
    
    def _delete_temp_jpegs(self):
        for file_name in os.listdir(self._data_path):
            if file_name.endswith(".jpeg"):
                os.remove(os.path.join(self._data_path, file_name))
