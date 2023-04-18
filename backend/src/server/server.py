from flask import Flask, Response
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, cruel world!'

@app.route('/echo/<phrase>')
def echo(phrase):
    return [phrase]


@app.route("/camera_feed")
def stream_camera_feed():
    return Response()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8078, debug=True)