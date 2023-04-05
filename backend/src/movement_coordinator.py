from stage import Stage
from imaging_grid import ImagingGrid, ImagingLocation

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
        self.__nm_per_step: float = stage.get_step_resolution()

    def move_to_next_location(self):
        # move to the next imaging location
        self.__current_cell_ind += 1
        location: ImagingLocation = self.__grid.get_cell(self.__current_cell_ind)

        new_stage_position: tuple[float, float] = location.get_center_location()
        pos_in_steps: tuple[int, int] = self.__location_nm_to_steps(new_stage_position)

        self.__stage.move_to(pos_in_steps[0], pos_in_steps[1]) 

    def has_next_location(self) -> bool:
        # returns true if we are not at the final location
        return self.__current_cell_ind != self.__grid.get_num_cells()

    def reset(self):
        # resets us to the start of the iteration 
        # does not move the stage to the first position
        self.__current_cell_ind = -1
        pass

    def __location_nm_to_steps(self, location: tuple[float, float]) -> tuple[int, int]:
        x_steps = location[0] / self.__nm_per_step
        y_steps = location[1] / self.__nm_per_step
        return tuple([x_steps, y_steps])
