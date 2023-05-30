import logging
import atexit

import platform


logging.basicConfig(level=logging.INFO)
logging.getLogger("werkzeug").setLevel(logging.ERROR)

import io
import tkfilebrowser    # this package is such a pain, but needs to be used since tk doesn't work
                        # with eclipse device running for some reason

from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
from PIL import Image

from camera.concurrent_pmm_camera import CPMMCamera 
from stage.pmm_stage import PMMStage 

from imager.chip_imager import ChipImager
from server.imager_manager import ImagerManager
from server.stitcher_manager import StitcherManager
from imager.config import DEMO_STITCH_DATA_PATH

app = Flask("src")
CORS(app)
sock = SocketIO(app, cors_allowed_origins="*")


cache = {}  # server lifetime-wide cache

IMAGES_PATH = (
    "/home/spoonk/dev/allbritton/chip-imaging/backend/prototyping/sample_data/test1"
)
""" IMAGES_PATH = "/Users/spunk/college/work/chip-imaging/backend/prototyping/sample_data/test1" """


# Streams images from the camera to the socket that  
# requested a video feed
@sock.on("video")
def handle_video():
    if "camera" in cache:
        try:
            cam = cache["camera"]
            while True:
                im = Image.fromarray(cam.take_image())
                img_byte_arr = io.BytesIO()
                im.save(img_byte_arr, format="PNG")
                img_byte_arr = img_byte_arr.getvalue()
                sock.emit("frame", {"image_data": img_byte_arr})
                sock.sleep(0.01)  # I don't care!!!!!!
        except Exception as e:
            sock.emit(
                "camera_failure", str(e)
            )  # note: this goes away with a real camera :O (does it?)

    else:
        sock.emit("camera_uninitialized", "please initialize the device first")

# Initializes all of the hardware needed for acquisition
# stitching can be done without calling initialize
@app.route("/initialize")
def initialize():
    try:
        if "manager" in cache:
            raise Exception("already initialized")

        cam = CPMMCamera()
        cam.connect()
        cache["camera"] = cam

        stage = PMMStage()
        cache["stage"] = stage

        imager = ChipImager(stage, cam)
        cache["imager"] = imager

        imager_manager = ImagerManager(imager)
        cache["manager"] = imager_manager

        cache["feeding"] = False

        return jsonify([True, "initialized"])

    except Exception as e:
        return jsonify([False, e.__str__()])

# gets the status of the devices needed for acquisition
# this response also includes the file path to where images
# will be saved
@app.route("/status")
def get_status():
    if "manager" in cache:  # take this as initialized
        manager: ImagerManager = cache["manager"]
        return jsonify([True, manager.get_status()])

    return jsonify([False, "devices not initialized"])

# updates the parameters that will be used to image the chip
@app.route("/update/<width>/<height>/<distance>")
def update_imaging_parameters(width, height, distance):
    if "manager" in cache:
        manager: ImagerManager = cache["manager"]
        return jsonify(
            manager.change_imaging_parameters(
                float(width), float(height), float(distance)
            )
        )
    return jsonify([False, "please initialize the device"])

# sets the exposure of the camera
@app.route("/exposure/<exposure>")
def set_camera_exposure(exposure):
    exposure = float(exposure)
    if "camera" in cache:
        cam = cache["camera"]
        cam.set_exposure(exposure)
        return jsonify([True, f"set exposure to {exposure}"])
    return jsonify([False, "camera not initialized"])

# sets the gain of the camera
@app.route("/gain/<gain>")
def set_gain(gain):
    gain = float(gain)
    if "camera" in cache:
        cam = cache["camera"]
        cam.set_gain(gain)
        return jsonify([True, f"set gain to {gain}"])
    return jsonify([False, "camera not initialized"])

# opens a file explorer for the user to select which directory
# they want to save the acquisition data to
# note that a directory can only be used if it is empty
@app.route("/promptDataPath")
def prompt_acquisition_path():
    if "manager" in cache:
        manager: ImagerManager = cache["manager"]
        directory_path = tkfilebrowser.askopendirname(initialdir="./")

        if directory_path is None or directory_path == '':
            return jsonify([False, "directory not selected"])
        return jsonify(manager.set_imaging_output_path(directory_path))
    return jsonify([False, "please initialize the device first"])


# Runs the data acquisition process, saving images to where 
# the user selected in the promptDataPath route
@app.route("/acquire")
def run_acquisition():
    if "manager" in cache and cache["manager"] is not None:
        manager: ImagerManager = cache["manager"]
        if manager.get_saved_acquisition_path() is None:
            return jsonify(
                [False, "please select an empty directory to save the images in first"]
            )

        res = manager.start_acquisition()
        logging.info(f"res is {res}")
        return jsonify(res)

    return jsonify([False, "please initialize the device first"])

# indicates that the current position of the stage should be used
# as the top left corner of the stitched image
@app.route("/topLeft")
def save_top_left():
    if "manager" in cache:
        manager: ImagerManager = cache["manager"]
        manager.save_top_left_position()
        return jsonify([True, "saved top left position"])
    return jsonify([False, "please initialize the device first"])

# ===============================  stitching routes ============================
# opens a file explorer where the user selects the directory from 
# which they would like to stitch
# the selected directory must contain a grid.json file and a 
# subdirectory called raw_data
@app.route("/promptStitchingPath")
def prompt_path():
    stitcher: StitcherManager = cache['stitcher']
    directory_path = None

    if platform.system() != 'Darwin':
        directory_path = tkfilebrowser.askopendirname(initialdir="./")
        print(directory_path)
    else:
        directory_path = DEMO_STITCH_DATA_PATH
    if directory_path is None or directory_path == '':
        return jsonify([False, "directory not selected"])

    return jsonify(stitcher.initialize(str(directory_path)))

# Sends back an h x w grid of images from 
# the directory selected as the stitching path
@app.route("/manualGrid/<h>/<w>")
def server_images(h, w):
    stitcher: StitcherManager = cache['stitcher']
    image_grid_res = stitcher.get_manual_grid(int(h), int(w))
    return jsonify(image_grid_res)

# Updates the stitcher's hyperparameters
# these values will come from the frontend manual alignment process
# and are used to get the stitching to be just right
@app.route("/setStitchingParams/<theta>/<pixelsPerUm>")
def set_stitching_params(theta, pixelsPerUm):
    stitcher: StitcherManager = cache['stitcher']
    try:
        theta = float(theta)
        pixelsPerUm = float(pixelsPerUm)
    except Exception:
        return jsonify(False, "failed to parse theta and number of pixels per um")

    return jsonify(stitcher.configure(theta, pixelsPerUm))

# Runs the stitching process, resulting in a stitched.TIFF 
# file to appear in the stitching directory
@app.route("/stitch")
def start_stitching():
    stitcher: StitcherManager = cache['stitcher']
    return jsonify(stitcher.stitch())


def shut_down():
    cache.clear()

if __name__ == "__main__":
    # stitcher manager doesn't rely on hardware
    cache['stitcher'] = StitcherManager()
    atexit.register(shut_down)

    sock.run(app, host="127.0.0.1", port=8079, debug=True)

