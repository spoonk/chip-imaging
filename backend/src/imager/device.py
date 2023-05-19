from abc import ABC, abstractmethod


class Device(ABC):
    """
    A device is a piece of hardware that we interact with
    Devices can be connected to and have their connections closed,
    which perform some setup and cleanup respectively
    """
    
    # opens the connection to the device
    # raises a ConnectionError if connecting to the device fails
    @abstractmethod
    def connect(self):
        pass

    # closes the connection to the device,
    # performing any necessary cleanup
    @abstractmethod
    def close(self):
        pass

    # returns true if the device has an active connection
    @abstractmethod
    def is_connected(self) -> bool:
        pass