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

# how long the camera should wait before and after taking an image (ms)
CAMERA_WAIT_DURATION = 0.5


CAMERA_RESOLUTION = (1344, 1024)

# name of the stitched file
STITCHED_IMAGE_NAME = "stitched.TIFF"


# configuration of the eclipse device 
_ECLIPSE_DEVICE_CONFIG = {
    "config_path": ECLIPSE_DEVICE_CONFIG_PATH,
    "stage_name" : "TIXYDrive"
}

# configuration of the eclipse device 
_DEMO_DEVICE_CONFIG = {
    "config_path": DEMO_DEVICE_CONFIG_PATH,
    "stage_name": "XY"
}

# the device configuration that gets used in the program
# DEVICE_CONFIG = _DEMO_DEVICE_CONFIG
DEVICE_CONFIG = _ECLIPSE_DEVICE_CONFIG

DEMO_STITCH_DATA_PATH = '/Users/spunk/college/work/chip-imaging/backend/src/demo_images/realtest4'

# serial port the prior stage connects to
PRIOR_CONTROLLER_PORT = "COM5"

RAW_DATA_DIR_NAME = 'raw_data'
GRID_PROPERTIES_FILE_NAME = 'grid.json'
