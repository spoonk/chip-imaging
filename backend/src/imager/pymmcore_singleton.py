import pymmcore
from imager.config import MICROMANAGER_PATH, DEVICE_CONFIG 
import logging

class PymmcoreSingleton():
    """
    Singleton for the pymmcore instance.
    Maintains a 'reference counter' to track how many different 
    'instantiations' of the singleton there are, resetting
    the pymmcore instance when the counter hits 0

    Responsible for loading the correct file. Capable of 
    emitting errors if the loading fails
    """
    _instance = None
    _instance_counter = 0

    def __init__(self):
        if PymmcoreSingleton._instance is None or PymmcoreSingleton._instance_counter == 0:
            PymmcoreSingleton._instance = pymmcore.CMMCore()
            PymmcoreSingleton._instance.setDeviceAdapterSearchPaths([MICROMANAGER_PATH])
            PymmcoreSingleton._instance.loadSystemConfiguration(DEVICE_CONFIG["config_path"])
            logging.getLogger().info(f"pymmcore instance loaded from {DEVICE_CONFIG['config_path']}")

        self.core = PymmcoreSingleton._instance
        PymmcoreSingleton._instance_counter += 1

    def __del__(self):
        """
        When all references to the singleton are lost, we reset the pymmcore session
        """
        PymmcoreSingleton._instance_counter -= 1
        if PymmcoreSingleton._instance_counter == 0:
            PymmcoreSingleton._instance.reset()
            logging.getLogger().info("pymmcore reset")