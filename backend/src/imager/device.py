import abc


class Device(abc.ABC):
    """
    A device is a piece of hardware that we interact with
    Devices can be connected to and have their connections closed,
    which perform some setup and cleanup respectively
    """
    
    # opens the connection to the device
    # raises a ConnectionError if connecting to the device fails
    @abc.abstractmethod
    def connect(self):
        pass

    # closes the connection to the device,
    # performing any necessary cleanup
    @abc.abstractmethod
    def close(self):
        pass

    # returns true if the device has an active connection
    @abc.abstractmethod
    def is_connected(self) -> bool:
        pass