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

from camera.pmm_camera import PMMCamera

app = Flask('src')
CORS(app)
sock = SocketIO(app, cors_allowed_origins='*')

cache = {} # server lifetime-wide cache

@sock.on('video')
def handle_video():
    cam = PMMCamera()
    cam.connect()
    cam.set_exposure(100)

    logging.getLogger().info("starting video loop")
    while True:
        im = Image.fromarray(cam.take_image())
        img_byte_arr = io.BytesIO()
        im.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        sock.emit('frame', {'image_data': img_byte_arr})

@sock.on('connect')
def connect():
    print('connected')

@sock.on('disconnect')
def connect():
    print('disconnected')

if __name__ == '__main__':
    sock.run(app, host='127.0.0.1', port=8079, debug=True)