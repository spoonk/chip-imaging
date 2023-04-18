from flask import Flask, Response
from camera.pmm_camera import PMMCamera

app = Flask(__name__)
cam = PMMCamera()
cam.connect()

@app.route('/')
def hello():
    return 'Hello, cruel world!'

@app.route('/echo/<phrase>')
def echo(phrase):
    return [phrase]

@app.route("/camera_feed")
def stream_camera_feed():
    return Response(cam.generate_live_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8078, debug=True)