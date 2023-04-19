import logging
logging.basicConfig(level = logging.INFO)
logging.getLogger('socketio').setLevel(logging.ERROR)
logging.getLogger('engineio').setLevel(logging.ERROR)
logging.getLogger('geventwebsocket.handler').setLevel(logging.ERROR)

logging.getLogger('werkzeug').setLevel(logging.ERROR)
from PIL import Image
import io
from flask_socketio import SocketIO
from time import sleep

from flask import Flask, Response
from flask_cors import CORS
from camera.pmm_camera import PMMCamera

app = Flask('src')
CORS(app)
sock = SocketIO(app, cors_allowed_origins='*')

cache = {}


# @app.route('/')
# def hello():
    # return 'Hello, cruel world!'

@app.route('/frame')
def get_frame():
    # cam = PMMCamera()
    # cam.connect()
    cam = cache['camera']

    im = Image.fromarray(cam.take_image())
    img_byte_arr = io.BytesIO()
    im.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    return Response(img_byte_arr, mimetype='image/jpeg; boundary=frame')

@app.route('/init')
def init_camera():
    cache['camera'] = PMMCamera()
    cache['camera'].connect()
    cache['camera'].set_gain(35)
    return "worked!"


@sock.on('connect')
def handle_connect():
    print('connected')
    sock.emit('message', 'hello there, my new socket friend')

@sock.on('video')
def handle_connect():
    while True:
        # sock.emit('message', i)
        cam = cache['camera']

        im = Image.fromarray(cam.take_image())
        img_byte_arr = io.BytesIO()
        im.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        sock.emit('image', {'image_data': img_byte_arr})
        sleep (0.1)




@sock.on('disconnect')
def handle_disconnect():
    print('disconnected')

if __name__ == '__main__':
    sock.run(app, host='127.0.0.1', port=8078, debug=True)
    if 'camera' in cache:
        del cache['camera']