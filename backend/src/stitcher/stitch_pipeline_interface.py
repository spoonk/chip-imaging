from abc import ABC, abstractmethod


class StitchPipeline(ABC):

    """
    A stitch pipeline stitches a directory of *.TIFF
    images into a single, larger .TIFF image
    """

    @abstractmethod
    def __init__(self, tiff_images_dir_path: str):
        pass

    @abstractmethod
    def run(self):
        # stitch all tiff images in the directory pointed to by path
        # saves the result to disk
        pass

    @abstractmethod
    def get_stitch_result(self):
        # returns the stitching result or None if stitching hasn't been run yet
        pass

    # @abstractmethod
    # def save_stitch_result(self, save_dir_path: str):
    #     # saves the stitched image to the directory pointed to by
    #     # save_dir_path
    #     pass
