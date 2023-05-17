import math
from typing import TypedDict, Tuple

class ImagingLocation():
    def __init__(self, center: tuple[float, float]):
        self.__center = center

    def get_center_location(self) -> tuple[float, float]:
        """ Returns the (x,y) center of this imaging location """
        return self.__center


class GridProperties(TypedDict):
    top_left: Tuple[float, float]
    width: float
    height: float
    distance: float
    rows: int
    cols: int

class ImagingGrid():
    """
    An imaging grid plans a set of locations
    to take pictures at. A single imaging grid 
    refernce is meant to be shared across several
    different objects to sync the imaging plan
    across those objects
    """

    def __init__(self):
        # empty constructor representing an unspecified grid
        self.__top_left = (0.0, 0.0)
        self.__imaging_width = 1000.0
        self.__imaging_height = 1000.0
        self.__distance_between = 500.0
        self.__cells = self.__compute_image_grid()
        self.__pixels_per_um = 1 # each pixel represents a 1x1 um square TODO: does this belong in this class?

    def __compute_image_grid(self) -> list[ImagingLocation]:
        """Recompute the imaging grid with the current parameters"""
        # 1 + since the first image won't be 100% chip
        # TODO: put these in a function
        rows, cols = self.get_grid_dimensions()

        top_left_x, top_left_y = self.__top_left 
        cells: list[ImagingLocation] = []

        for r in range(rows):
            for c in range(cols):
               # vertical position
               # note we use minus here since a negative value moves to a downward channel on the chip
               y_offset: float = top_left_y - self.__distance_between * r
               # horizontal position
               x_offset: float = top_left_x + self.__distance_between * c
               loc = ImagingLocation(tuple([x_offset, y_offset]))
               cells.append(loc)
        
        return cells

    # returns (rows, cols) for imaging locations
    def get_grid_dimensions(self) -> Tuple[int, int]:
        rows = 1 + math.ceil(self.__imaging_height / self.__distance_between)
        cols = 1 + math.ceil(self.__imaging_width / self.__distance_between)
        return tuple([rows, cols])

    # pre: index is in [0, num_cells)
    def get_cell(self, index: int) -> ImagingLocation:
        return self.__cells[index]
    
    def get_num_cells(self) -> int:
        return len(self.__cells)
    
    def get_pixels_per_um(self) -> float:
        return self.__pixels_per_um
    
    def get_distance_between_images_um(self) -> float:
        return self.__distance_between
    
    def set_pixels_per_um(self, pixels_per_um: float):
        self.__pixels_per_um = pixels_per_um

    def set_properties(self, top_left: tuple[float, float], imaging_width: float, imaging_height: float, distance_between_cells: float, pixel_size_um: float):
        # reset all properties of the imaging grid
        self.__top_left: tuple[float, float] = top_left 
        self.__imaging_width = imaging_width
        self.__imaging_height = imaging_height
        self.__distance_between: float = distance_between_cells 
        self.__cells = self.__compute_image_grid()
        self.__pixels_per_um = pixel_size_um

    def set_top_left(self, top_left: tuple[float, float]):
        self.__top_left = top_left
        self.__cells = self.__compute_image_grid()

    def set_imaging_width(self, width: float):
        self.__imaging_width = width
        self.__cells = self.__compute_image_grid()

    def set_imaging_height(self, height: float):
        self.__imaging_height = height
        self.__cells = self.__compute_image_grid()

    def set_distance_between_images(self, distance: float):
        self.__distance_between = distance
        self.__cells = self.__compute_image_grid()
            
    def get_properties(self) -> GridProperties:
        rows, cols = self.get_grid_dimensions()
        data: GridProperties = {
            "top_left": self.__top_left,
            "width": self.__imaging_width,
            "height": self.__imaging_height,
            "distance": self.__distance_between,
            "rows": rows,
            "cols": cols,
        }
        return data

