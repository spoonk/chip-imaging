from abc import ABC, abstractmethod

# camera interface

class Camera(ABC):
    
    @abstractmethod
    def __init__(self, MMConfigPath: str):
        pass
    