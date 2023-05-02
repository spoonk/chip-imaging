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
        cache['amount'] += 1
        cam = cache['camera']

        logging.getLogger().info("starting video loop")
        while True:
            logging.getLogger().info(f"{cam.get_exposure()}, {cam.get_gain()}")
            im = Image.fromarray(cam.take_image())
            img_byte_arr = io.BytesIO()
            im.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            sock.emit('frame', {'image_data': img_byte_arr})
            # print(cache['amount'])
        print("I exited")
        cache['feeding'] = False


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
    cache['amount'] = 0

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
        return f"set parameters to {width} {height} {distance}"
    return f"{width}, {height}, {distance}"


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


# set a path

# start stitching

# get stitch result

# start acquiring

# @sock.on('connect')
# def connect():
#     print('connected')

# @sock.on('disconnect')
# def connect():
#     print('disconnected')

if __name__ == '__main__':
    sock.run(app, host='127.0.0.1', port=8079, debug=True)