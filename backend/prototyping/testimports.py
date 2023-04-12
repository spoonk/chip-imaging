import pymmcore
import os
mm_dir = "C:\Program Files\Micro-Manager-2.0gamma"
device_config_file_name = "MMConfig_demo.cfg" # this demo file has a bunch of 'mock' devices
# this lets us simulate running on hardware without actually controlling anything

mmc = pymmcore.CMMCore()
mmc.setDeviceAdapterSearchPaths

