import logging

logging.basicConfig(level = logging.INFO)
logging.getLogger('werkzeug').setLevel(logging.ERROR)
# logging.getLogger('socketio').setLevel(logging.ERROR)
# logging.getLogger('engineio').setLevel(logging.ERROR)
# logging.getLogger('geventwebsocket.handler').setLevel(logging.ERROR)

import io
from time import sleep, time

# from camera.pmm_camera import PMMCamera
from camera.concurrent_pmm_camera import CPMMCamera
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from imager.chip_imager import ChipImager
from PIL import Image
from server.imager_manager import ImagerManager
from stage.pmm_stage import PMMStage

app = Flask('src')
CORS(app)
sock = SocketIO(app, cors_allowed_origins='*')

cache = {} # server lifetime-wide cache

@sock.on('video')
def handle_video():
    # cam = CPMMCamera()
    # cam.connect()
    # cam.set_exposure(100)
    cam = cache['camera']

    logging.getLogger().info("starting video loop")
    while True:
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

    return "initialized"

@app.route('status')
def get_status():
    return cache['manager'].get_status()



# set imaging parameters

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