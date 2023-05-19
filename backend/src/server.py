import logging

logging.basicConfig(level=logging.INFO)
logging.getLogger("werkzeug").setLevel(logging.ERROR)

import io
from base64 import encodebytes
from io import BytesIO
from tkinter import Tk
from tkinter.filedialog import askdirectory

from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
from PIL import Image

""" from camera.concurrent_pmm_camera import CPMMCamera """
""" from stage.pmm_stage import PMMStage """
from camera.mock_camera import MockCamera
from imager.chip_imager import ChipImager
from server.imager_manager import ImagerManager
from stage.mock_stage import MockStage
from stitcher.cv_stitcher import CVStitchPipeline  # TODO: temp for generating images

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
                sock.sleep(0.01)
        except Exception as e:
            sock.emit(
                "camera_failure", str(e)
            )  # note: this goes away with a real camera :O

    else:
        sock.emit("camera_uninitialized", "please initialize the device first")


@app.route("/initialize")
def initialize():
    try:
        if "manager" in cache:
            raise Exception("already initialized")
        """ cam = CPMMCamera() """
        cam = MockCamera()
        cam.connect()
        cam.set_exposure(100)
        cache["camera"] = cam

        """ stage = PMMStage() """
        stage = MockStage()
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
        manager: ImagerManager = cache['manager']
        return jsonify([True, manager.get_status()])

    return jsonify([False, "offline"])


@app.route("/update/<width>/<height>/<distance>")
def update_imaging_parameters(width, height, distance):
    if "manager" in cache:
        manager: ImagerManager = cache['manager']
        manager.change_imaging_parameters(
            float(width), float(height), float(distance)
        )
        return jsonify([True, "imaging parameters updated"])
    return jsonify([False, "please initialize the device"])


@app.route("/exposure/<exposure>")
def set_camera_exposure(exposure):
    exposure = float(exposure)
    if "camera" in cache:
        cam = cache['camera']
        cam.set_exposure(exposure)
        return jsonify([True, f"set exposure to {exposure}"])
    return jsonify([False, "camera not initialized"])


@app.route("/gain/<gain>")
def set_gain(gain):
    gain = float(gain)
    if "camera" in cache:
        cam = cache['camera']
        cam.set_gain(gain)
        return jsonify([True, f"set gain to {gain}"])
    return jsonify([False, "camera not initialized"])


@app.route("/promptDataPath")
def prompt_acquisition_path():
    # prompts the user to select where the data images will be saved
    if "manager" in cache:
        manager: ImagerManager = cache['manager']
        root = Tk()
        root.wm_attributes("-topmost", 1)
        root.mainloop()
        directory_path = askdirectory(initialdir="./")
        if manager.set_imaging_output_path(directory_path):
            return jsonify([True, f"directory saved!"])
        else:
            return jsonify(
                [
                    False,
                    f"{directory_path} is not empty, please select an empty directory",
                ]
            )
    return jsonify([False, "please initialize the device first"])


@app.route("/promptStitchingPath")
def prompt_path():
    # prompts the user to select where the data images will be saved
    if "manager" in cache:
        manager: ImagerManager = cache['manager']
        root = Tk()
        root.wm_attributes("-topmost", 1)
        root.mainloop()
        directory_path = askdirectory(initialdir="./")
        if manager.set_stitching_directory(directory_path):
            return jsonify([True, f"stitching directory saved!"])
        else:
            return jsonify(
                [
                    False,
                    f"{directory_path} is not stitchable, please make sure it only has a raw_data directory and a grid.json file",
                ]
            )
    return jsonify([False, "please initialize the device first"])


@app.route("/stitch")
def start_stitching():
    if "manager" in cache:
        manager: ImagerManager = cache['manager']
        if manager.get_saved_path() is None:
            return jsonify(
                [False, "please choose a directory from the acquisition menu first"]
            )
        try:
            manager.stitch()
            return jsonify([True, "stitching succeeded"])
        except Exception as e:
            return jsonify([False, f"something went wrong: {e}"])
    return jsonify([False, "please initialize the device first"])


@app.route("/acquire")
def run_acquisition():
    if "manager" in cache:
        manager: ImagerManager = cache['manager']
        if manager.get_saved_path() is None:
            return jsonify(
                [False, "please select an empty directory to save the images in first"]
            )

        res = manager.start_acquisition()
        if res:
            return jsonify([True, "acquisition started"])
        else:
            return jsonify([False, "acquisition already in progress"])

    return jsonify([False, "please initialize the device first"])


@app.route("/topLeft")
def save_top_left():
    if "manager" in cache:
        manager: ImagerManager = cache['manager']
        manager.save_top_left_position()
        return jsonify([True, "saved top left position"])
    return jsonify([False, "please initialize the device first"])


# TODO: store jpegs in a buffer man
@app.route("/manualGrid/<h>/<w>")
def server_images(h, w):
    try:
        # TODO: check if manager exists and has stitching path, return correct result
        # TODO: try except
        stitcher = CVStitchPipeline(IMAGES_PATH)
        stitcher._generate_jpeg_from_tiff()
        images = stitcher._load_jpeg_images()
        # convert images
        images_bytes = []
        for image in images:
            img_byte_arr = BytesIO()
            image.save(img_byte_arr, format="PNG")
            images_bytes.append(encodebytes(img_byte_arr.getvalue()).decode("ascii"))

        stitcher._delete_temp_jpegs()
        return [True, jsonify({"result": images_bytes})]
    except Exception as e:
        return [False, str(e)]

if __name__ == "__main__":
    sock.run(app, host="127.0.0.1", port=8079, debug=True)
