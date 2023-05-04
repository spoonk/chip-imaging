import logging
logging.basicConfig(level = logging.INFO)
logging.getLogger('werkzeug').setLevel(logging.ERROR)
# logging.getLogger('socketio').setLevel(logging.ERROR)
# logging.getLogger('engineio').setLevel(logging.ERROR)
# logging.getLogger('geventwebsocket.handler').setLevel(logging.ERROR)

from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from time import sleep, time
import io
from PIL import Image
from tkinter.filedialog import askdirectory
from tkinter import Tk

# from camera.pmm_camera import PMMCamera
from camera.concurrent_pmm_camera import CPMMCamera
from stage.pmm_stage import PMMStage
from imager.chip_imager import ChipImager
from server.imager_manager import ImagerManager

app = Flask('src')
CORS(app)
sock = SocketIO(app, cors_allowed_origins='*')

cache = {} # server lifetime-wide cache

@sock.on('video')
def handle_video():
    if 'feeding' in cache and not cache['feeding']:
        cache['feeding'] = True
        cam = cache['camera']

        logging.getLogger().info("starting video loop")
        while True:
            logging.getLogger().info(f"{cam.get_exposure()}, {cam.get_gain()}")
            im = Image.fromarray(cam.take_image())
            img_byte_arr = io.BytesIO()
            im.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            sock.emit('frame', {'image_data': img_byte_arr})


@app.route('/initialize')
def initialize():
    cam = CPMMCamera()
    cam.connect()
    cam.set_exposure(100)
    cache['camera'] = cam

    stage = PMMStage()
    cache['stage'] = stage

    imager = ChipImager(stage, cam)  
    cache['imager'] = imager

    imager_manager = ImagerManager(imager)
    cache['manager'] = imager_manager

    cache['feeding'] = False

    return "initialized"

@app.route('/status')
def get_status():
    if 'manager' in cache:
        return cache['manager'].get_status()
    return "offline"

@app.route('/update/<float:width>/<float:height>/<float:distance>')
def update_imaging_parameters(width, height, distance):
    if 'manager' in cache:
        cache['manager'].change_imaging_parameters(width, height, distance)
        return f"success"
    return 'please initialize the device'

@app.route('/exposure/<exposure>')
def set_camera_exposure(exposure):
    exposure = float(exposure)
    if 'camera' in cache:
        cache['camera'].set_exposure(exposure)
        print("EXPO")
        return f"set exposure to {exposure}"
    return "camera not initialized"
    
@app.route('/gain/<gain>')
def set_gain(gain):
    gain = float(gain)
    if 'camera' in cache:
        cache['camera'].set_gain(gain)
        print("GAING")
        return f"set gain to {gain}"
    return "camera not initialized"

@app.route('/promptDataPath')
def prompt_path():
    # prompts the user to select where the data images will be saved
    if 'manager' in cache:
        # TODO: move into a helper function, add a button on tkinter window
        # that says select path then destroys window
        root = Tk()
        root.wm_attributes('-topmost', 1)
        root.mainloop()
        directory_path = askdirectory(initialdir="./")
        print(directory_path)
        cache['manager'].set_imaging_output_path(directory_path)
        return directory_path
    return "please initialize the device first"

@app.route('/stitch')
def start_stitching():
    if 'manager' in cache:
        cache['manager'].stitch()
        return "stitching started"
    return "please initialize the device first"


@app.route('/acquire')
def run_acquisition():
    if 'manager' in cache:
        cache['manager'].start_acquisition
        return "acquisition started"
    return "please initialize the device first"


# TODO: this
# @app.route('/getStitch')
# def get_stitch_result():
#     if 'manager' in cache:

@app.route('./topLeft')
def save_top_left():
    if 'manager' in cache:
        cache['manager'].save_top_left_position()
        return "saved"
    return "please initialize the device first"

if __name__ == '__main__':
    sock.run(app, host='127.0.0.1', port=8079, debug=True)