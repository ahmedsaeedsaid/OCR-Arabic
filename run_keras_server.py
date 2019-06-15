
import flask

import base64

from AOCR import *
import numpy as np
from flask_cors import CORS
app = flask.Flask(__name__)
loaded_model=load_model('models/NN_Model.h5')
CORS(app)
@app.route("/word_tokinizer", methods=["POST"])
def tokinize():
    data = {}
    if flask.request.method == "POST":
        try:
            image = flask.request.get_json()['image']
            image = base64.b64decode(image)
            with open('temp/temp_picture.jpg', 'wb') as f:
                f.write(image)
            text=aocr('temp/temp_picture.jpg',loaded_model)
            data["data"] = text
            return flask.jsonify(text)
        except:
            text = flask.request.get_json()['text']
            list=[['مصر','مبتدأ مرفوع بالضمه'],['جميله','خبر مرفوع بالضمه']]
            return flask.jsonify(list)
if __name__ == "__main__":
    app.run(host='0.0.0.0' , port=5000)
