
import pymmcore
from imager.config import MICROMANAGER_PATH, DEVICE_CONFIG 

class PymmcoreSingleton():
    """
    Singleton for the pymmcore instance
    """
    _instance = None
    _instance_counter = 0

    def __init__(self):
        if PymmcoreSingleton._instance is None or PymmcoreSingleton._instance_counter == 0:
            PymmcoreSingleton._instance = pymmcore.CMMCore()
            PymmcoreSingleton._instance.setDeviceAdapterSearchPaths([MICROMANAGER_PATH])
            PymmcoreSingleton._instance.loadSystemConfiguration(DEVICE_CONFIG)
            print("instance loading")

        self.core = PymmcoreSingleton._instance
        PymmcoreSingleton._instance_counter += 1


    def __del__(self):
        """
        When all references to the singleton are lost, we reset the pymmcore session
        """
        PymmcoreSingleton._instance_counter -= 1
        if PymmcoreSingleton._instance_counter == 0:
            print('resetining')
            PymmcoreSingleton._instance.reset()
