import logging
import atexit

import platform


logging.basicConfig(level=logging.INFO)
logging.getLogger("werkzeug").setLevel(logging.ERROR)

import io
from tkinter import Tk
import tkfilebrowser
from tkinter.filedialog import askdirectory

from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
from PIL import Image

from camera.concurrent_pmm_camera import CPMMCamera 
from stage.pmm_stage import PMMStage 

# from camera.mock_camera import MockCamera
# from stage.mock_stage import MockStage

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


@app.route("/initialize")
def initialize():
    try:
        if "manager" in cache:
            raise Exception("already initialized")
        """ cam = CPMMCamera() """
        cam = CPMMCamera()
        cam.connect()
        cam.set_exposure(100)
        cache["camera"] = cam

        """ stage = PMMStage() """
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


@app.route("/status")
def get_status():
    if "manager" in cache:  # take this as initialized
        manager: ImagerManager = cache["manager"]
        return jsonify([True, manager.get_status()])

    return jsonify([False, "offline"])


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


@app.route("/exposure/<exposure>")
def set_camera_exposure(exposure):
    exposure = float(exposure)
    if "camera" in cache:
        cam = cache["camera"]
        cam.set_exposure(exposure)
        return jsonify([True, f"set exposure to {exposure}"])
    return jsonify([False, "camera not initialized"])


@app.route("/gain/<gain>")
def set_gain(gain):
    gain = float(gain)
    if "camera" in cache:
        cam = cache["camera"]
        cam.set_gain(gain)
        return jsonify([True, f"set gain to {gain}"])
    return jsonify([False, "camera not initialized"])


@app.route("/promptDataPath")
def prompt_acquisition_path():
    # prompts the user to select where the data images will be saved
    if "manager" in cache:
        manager: ImagerManager = cache["manager"]
        # # TODO: put popup calling in a function with return being new dir
        # root = Tk()
        # root.wm_attributes("-topmost", 1)
        # root.mainloop()
        # root.update()
        directory_path = tkfilebrowser.askopendirname(initialdir="./")

        # directory_path = askdirectory(initialdir="./")
        if directory_path is None:
            return jsonify([False, "directory not selected"])
        return jsonify(manager.set_imaging_output_path(directory_path))
    return jsonify([False, "please initialize the device first"])

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


@app.route("/topLeft")
def save_top_left():
    if "manager" in cache:
        manager: ImagerManager = cache["manager"]
        manager.save_top_left_position()
        return jsonify([True, "saved top left position"])
    return jsonify([False, "please initialize the device first"])

# ===============================  stitching routes ============================

@app.route("/manualGrid/<h>/<w>")
def server_images(h, w):
    stitcher: StitcherManager = cache['stitcher']
    image_grid_res = stitcher.get_manual_grid(int(h), int(w))
    return jsonify(image_grid_res)

@app.route("/setStitchingParams/<theta>/<pixelsPerUm>")
def set_stitching_params(theta, pixelsPerUm):
    stitcher: StitcherManager = cache['stitcher']
    try:
        theta = float(theta)
        pixelsPerUm = float(pixelsPerUm)
    except Exception:
        return jsonify(False, "failed to parse theta and number of pixels per um")

    return jsonify(stitcher.configure(theta, pixelsPerUm))

@app.route("/promptStitchingPath")
def prompt_path():
    stitcher: StitcherManager = cache['stitcher']
    directory_path = None

    if platform.system() != 'Darwin':
        directory_path = tkfilebrowser.askopendirname(initialdir="./")
    else:
        directory_path = DEMO_STITCH_DATA_PATH
    if directory_path is None:
        return jsonify([False, "directory not selected"])

    return jsonify(stitcher.initialize(str(directory_path)))

@app.route("/stitch")
def start_stitching():
    stitcher: StitcherManager = cache['stitcher']
    return jsonify(stitcher.stitch())


def shut_down():
    cache.clear()

if __name__ == "__main__":
    cache['stitcher'] = StitcherManager()
    atexit.register(shut_down)
    sock.run(app, host="127.0.0.1", port=8079, debug=True)
