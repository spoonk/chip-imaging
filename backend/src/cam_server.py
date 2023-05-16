from flask import Flask,request
from flask_socketio import SocketIO

from camera.mock_camera import MockCamera
import io
from PIL import Image

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('server')
def sendmessage():
    print('image')
    cam = MockCamera()
    cam.connect()

    while True:
        print('hi')
        im = Image.fromarray(cam.take_image())
        img_byte_arr = io.BytesIO()
        im.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        """ sock.emit('frame', {'image_data': img_byte_arr}) """
        socketio.emit('client', 'hi')
        """ socketio.sleep(0.01) """


@socketio.on('connect')
def connect():
    print('client connected',request.sid)

@socketio.on('disconnect')
def disconnect():
    print('client disconnected',request.sid)

if __name__ == '__main__':
    try:
        socketio.run(app,port=5000)
    except Exception as e:
        print("\n Execption occurs while starting the socketio server",str(e))
