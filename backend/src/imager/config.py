STAGE_BAUD_RATE = 9600

# number of seconds to wait when polling the 
# stage to see if it's moving
STAGE_POLL_DELAY = 0.2

# the number of pixels moved when the stage moves by 1 nanometer
# (placeholder)
PIXELS_PER_NM = 1.0

# micro manager path
MICROMANAGER_PATH = r"C:\Program Files\Micro-Manager-2.0chipimaging"

# the path to the pymmcore config for the eclipse device 
ECLIPSE_DEVICE_CONFIG_PATH =  r"C:\Users\Luke\Desktop\Barracuda\AutomatedCE\config\NikonEclipseTi.cfg"

# path to demo device config (the dummy one)
DEMO_DEVICE_CONFIG_PATH = r"C:\Program Files\Micro-Manager-2.0chipimaging/MMConfig_demo.cfg"

# default directory to store images int
DATA_PATH = r"C:\Users\Luke\Desktop\chip-imager\chip-imaging\backend\prototyping\sample_data"


# configuration of the eclipse device 
_ECLIPSE_DEVICE_CONFIG = {
    "config_path": ECLIPSE_DEVICE_CONFIG_PATH,
}

# configuration of the eclipse device 
_DEMO_DEVICE_CONFIG = {
    "config_path": DEMO_DEVICE_CONFIG_PATH,
}

# the device configuration that gets used in the program
DEVICE_CONFIG = _DEMO_DEVICE_CONFIG

# serial port the prior stage connects to
PRIOR_CONTROLLER_PORT = "COM5"
