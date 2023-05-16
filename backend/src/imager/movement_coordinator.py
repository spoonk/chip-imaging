from stage.stage_interface import Stage
from imager.imaging_grid import ImagingGrid, ImagingLocation

class MovementCoordinator():
    """
    A movement coordinator is reponsible for 
    moving the stage so that the camera can see 
    regions of the chip. A coordinator is stateful
    in the way that it is currently showing
    one stage position and can be moved 
    to the next position as well as 
    reset to some initial state.
    It is designed to conceptually be 
    an iterator that moves through stage locations
    """

    def __init__(self, stage: Stage, grid: ImagingGrid):
        # pre: stage is connected
        self.__stage: Stage = stage
        self.__grid: ImagingGrid = grid
        self.__current_cell_ind: int = -1

    def move_to_next_location(self):
        # move to the next imaging location
        self.__current_cell_ind += 1
        location: ImagingLocation = self.__grid.get_cell(self.__current_cell_ind)

        new_stage_position: tuple[float, float] = location.get_center_location()
        # pos_in_steps: tuple[int, int] = self.__location_nm_to_steps(new_stage_position)

        self.__stage.move_to(new_stage_position[0], new_stage_position[1]) 

    def has_next_location(self) -> bool:
        # returns true if we are not at the final location
        # print(self.__grid.get_num_cells())
        return self.__current_cell_ind < self.__grid.get_num_cells() - 1

    def reset(self):
        # resets us to the start of the iteration 
        # does not move the stage to the first position
        self.__current_cell_ind = -1
        pass

