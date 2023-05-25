import logging
from time import sleep

from imager.config import DEVICE_CONFIG
from imager.pymmcore_singleton import PymmcoreSingleton
from stage.stage_interface import Stage


class PMMStage(Stage):
    """
    A PMMStage is a stage that is controlled by pymmcore
    This means this class is rather versatile as it works
    with any stage being controlled by pymmcore
    """

    def __init__(self):
        self._pymm = PymmcoreSingleton()
        self._core = self._pymm.core
        logging.getLogger().info("stage instantiated")

    def move_to(self, x:float, y:float):
        sleep(0.5)
        self._core.setXYPosition(x, y)
        logging.getLogger().info(f"stage moving to ({x}, {y})")

        self._core.waitForDevice(DEVICE_CONFIG["stage_name"]) # the xy stage
        sleep(0.5)
        
        final_pos = self.get_current_position()
        sleep(0.5)
        logging.getLogger().info(f"movement complete, final position ({final_pos[0]}, {final_pos[1]})")

    def get_current_position(self) -> tuple[float, float]:
        return self._core.getXYPosition()
    
