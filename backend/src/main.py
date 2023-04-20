import logging
logging.basicConfig(level = logging.INFO)
# logging.getLogger('werkzeug').setLevel(logging.ERROR)
# logging.getLogger('socketio').setLevel(logging.ERROR)
# logging.getLogger('engineio').setLevel(logging.ERROR)
# logging.getLogger('geventwebsocket.handler').setLevel(logging.ERROR)

from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from time import sleep
import io
from PIL import Image

from camera.pmm_camera import PMMCamera

app = Flask('src')
# CORS(app)
sock = SocketIO(app, cors_allowed_origins='*')

cache = {} # server lifetim-wide cache

@app.route('/initCamera')
def init_camera():
    cache['camera'] = PMMCamera()
    cache['camera'].connect()
    cache['camera'].set_gain(1)
    logging.getLogger().info("camera initialized")
    return "worked!"

@sock.on('video')
def handle_video():
    # cache['camera'] = PMMCamera()
    # cache['camera'].connect()
    # cache['camera'].set_gain(1)
    # logging.getLogger().info("camera initialized")
    # init_camera()
    logging.getLogger().info("starting video loop")
    while True:
        # sock.emit('message', i)
        # cam = cache['camera']
        # sock.emit('message', 'dddddd')
        sock.send('hi')

        # im = Image.fromarray(cam.take_image())
        # img_byte_arr = io.BytesIO()
        # im.save(img_byte_arr, format='PNG')
        # img_byte_arr = img_byte_arr.getvalue()
        # sock.emit('frame', {'image_data': img_byte_arr})
        sleep (0.1)
        # logging.getLogger().info("sent image")

@sock.on('connect')
def connect():
    print('connected')


@sock.on('disconnect')
def connect():
    print('disconnected')


if __name__ == '__main__':
    sock.run(app, host='127.0.0.1', port=8078, debug=True)
    if 'camera' in cache:
        del cache['camera']