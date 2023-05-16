from flask import Flask
from flask_cors import CORS
from stitcher.cv_stitcher import CVStitchPipeline
from io import BytesIO
from flask import jsonify
from base64 import encodebytes

""" IMAGES_PATH ="/home/spoonk/dev/allbritton/chip-imaging/backend/prototyping/sample_data/test1" """
IMAGES_PATH = "/Users/spunk/college/work/chip-imaging/backend/prototyping/sample_data/test1"
app = Flask('src')
CORS(app)

@app.route("/manualGrid/<h>/<w>")
def server_images(h, w):
    stitcher = CVStitchPipeline(IMAGES_PATH)
    stitcher._generate_jpeg_from_tiff()
    images = stitcher._load_jpeg_images()
    # convert images
    images_bytes = []
    for image in images:
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format='PNG')
        images_bytes.append(encodebytes(img_byte_arr.getvalue()).decode('ascii'))

    return jsonify({'result': images_bytes})
    

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8079, debug=True)
