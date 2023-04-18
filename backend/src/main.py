import logging
logging.basicConfig(level = logging.INFO)
from PIL import Image
import io

# from imager.chip_imager import ChipImager


from flask import Flask, Response
from flask_cors import CORS
from camera.pmm_camera import PMMCamera

app = Flask('src')

cam = PMMCamera()
cam.connect()

app.run(host='127.0.0.1', port=8078, debug=True)
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

# @app.route('/frame')
# def get_frame():
#     im = Image.fromarray(cam.take_image())
#     # im.show()

#     img_byte_arr = io.BytesIO()
#     im.save(img_byte_arr, format='PNG')
#     img_byte_arr = img_byte_arr.getvalue()

#     return Response(img_byte_arr, mimetype='image/jpeg; boundary=frame')

# if __name__ == '__main__':
    # app.run(host='127.0.0.1', port=8078, debug=True)