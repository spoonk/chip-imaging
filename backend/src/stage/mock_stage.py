import logging
from time import sleep

from stage.stage_interface import Stage


class MockStage(Stage):
    def __init__(self):
        self._x = 0.0
        self._y = 0.0
        logging.info('mock stage instantiated')

    def move_to(self, x: float, y:float):
        self._x = x
        self._y = y
        sleep(0.3)
        logging.info(f'mock stage moved to {self._x}, {self._y}')

    def get_current_position(self) -> tuple[float, float]:
        return tuple([self._x, self._y])
