
class DeviceInterruptException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


interrupted: bool = False

def interruptable(func):
    global interrupted
    def wrapper(*args, **kwargs):
        if interrupted:
            raise DeviceInterruptException("interrupt issued, terminating process")

        return func(*args, **kwargs)
    return wrapper

def interrupted_handler(func):
    def exception_handler_wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except DeviceInterruptException as e:
            print(e)
    return exception_handler_wrapper









# I like this design: break fundamental movements into a function,
# that function has a decorator that checks for an interrupt
# We also define a decorator for the higher-level function that 
# will handle an interrupte being raised from the lower-level functions

@interruptable
def move_stage():
    print('stage')

@interruptable
def move_arm():
    print('arm')

@interrupted_handler
def process():
    global interrupted
    move_stage()
    move_arm()
    move_stage()
    move_stage()
    move_arm()
    move_stage()
    interrupted = True
    move_stage()
    move_arm()
    move_arm()
    move_stage()
    move_stage()
    move_arm()

def main():
    process()

if __name__ == "__main__":
    main()
