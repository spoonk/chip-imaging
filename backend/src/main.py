import logging
logging.basicConfig(level = logging.INFO)
from PIL import Image
import io
# import pyserial

# from imager.chip_imager import ChipImager


from flask import Flask, Response
from flask_cors import CORS
from camera.pmm_camera import PMMCamera

app = Flask('src')

# cam = PMMCamera()
# cam.connect()

# cam = None

cache = {}

# app.run(host='127.0.0.1', port=8078, debug=True)
# CORS(app)
# cam.connect()
# cam.set_gain(2)


# @app.route('/')
# def hello():
    # return 'Hello, cruel world!'

# @app.route('/echo/<phrase>')
# def echo(phrase):
#     return [phrase]

# @app.route('/camera_feed')
# def stream_camera_feed():
#     return Response(cam.generate_live_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')

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


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8078, debug=True)
    if 'camera' in cache:
        del cache['camera']