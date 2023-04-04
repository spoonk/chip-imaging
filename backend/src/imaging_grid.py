import math

class ImagingLocation():
    def __init__(self, center: tuple[float, float]):
        self.__center = center

    def get_center_location(self) -> tuple[float, float]:
        """
        Returns the (x,y) center of this imaging location
        """
        return self.__center




class ImagingGrid():
    """
    An imaging grid plans a set of locations
    to take pictures at
    """

    # distance_between_cells is measured in nanometers (nm)
    # top_left is the x,y (nm) coordinates of the center of the top left image cell
    def __init__(self, top_left: tuple[float, float], imaging_width: float, imaging_height: float, distance_between_cells: float):
        self.__top_left: tuple[float, float] = top_left 
        self.__imaging_width = imaging_width
        self.__imaging_height = imaging_height
        self.__distance_between: float = distance_between_cells 
        self.__cells = self.__compute_image_grid()


    def __compute_image_grid(self) -> list[ImagingLocation]:
        """Recompute the imaging grid with the current parameters"""
        rows = math.ceil(self.__imaging_height / self.__distance_between)
        cols = math.ceil(self.__imaging_width / self.__distance_between)

        top_left_x, top_left_y = self.__top_left 
        cells: list[ImagingLocation] = []

        for r in range(rows):
            for c in range(cols):
               # vertical position
               y_offset: float = top_left_y + self.__distance_between * r
               # horizontal position
               x_offset: float = top_left_x + self.__distance_between * c
               loc = ImagingLocation(tuple(x_offset, y_offset))
               cells.append(loc)
        
        return cells

    # pre: index is in [0, num_cells)
    def get_cell(self, index: int) -> ImagingLocation:
        return self.__cels[index]
    

    def get_num_cels(self) -> int:
        return len(self.__cells)
    

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
        self.__distance_between = self.__compute_image_grid()
