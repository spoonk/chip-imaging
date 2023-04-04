from serial import Serial, SerialException
from stage import Stage
from device import Device
from config import STAGE_BAUD_RATE, STAGE_POLL_DELAY
from time import sleep # don't use this often

class PriorStage(Stage, Device):
    """
    A prior stage consists of a stage and a stage controller.
    Messages are sent via USB to the controller, which in turn 
    controls the stage    
    """

    def __init__(self, serial_port:str):
        self.__serial_port = serial_port
        self.__connected = False
        self.__connection: Serial = None

    def connect(self):
        try:
            self.connection = Serial(port=self.__serial_port, baudrate=STAGE_BAUD_RATE)
            self.__is_connected = True
        except SerialException as e:
            raise ConnectionError(f"Unable to connect to stage: reason {e}")
        
    def close(self):
        if self.is_connected():
            self.__connected = False
            self.connection.close()

    def is_connected(self) -> bool:
        return self.__connected
    

    def move(self, x:int, y:int):
        move_command = self.__format_move_cmd(x, y)
        self.__send_command(move_command)
        self.__wait_for_not_moving()

    # formats a x,y movement command to a string that can be directly
    # sent to the controller
    def __format_move_cmd(self, x:int, y:int) -> str:
        return f"G,{x},{y}"
        
    def __send_command(self, command:str):
        self.connection.write(command)
        self.connection.flush()


    # waits for the stage to finish moving, blocking
    # control until the stage stops moving
    def __wait_for_not_moving(self):
        while self.__is_moving():
            sleep(STAGE_POLL_DELAY)

    def __is_moving(self) -> bool:
        return (self.__check_axis_moving_cmd('X') and
                self.__check_axis_moving_cmd('Y') and
                self.__check_axis_moving_cmd('X') and
                self.__check_axis_moving_cmd('Y'))

    def __check_axis_moving_cmd(self, axis:str) -> bool:
        check_axis_moving_cmd = f"$,{axis}"
        self.__send_command(check_axis_moving_cmd)
        response = self.connect.readline().decode()
        try:
            return bool(response)
        except Exception as e:
            # TODO: when in doubt, be safe and say the stage is moving
            print(e)
            return True
