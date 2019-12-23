
import flask

import base64

import numpy as np
app = flask.Flask(__name__)
@app.route("/word_tokinizer", methods=["POST"])
def word_tokinizer():
    print("ahmed")
    return True

if __name__ == "__main__":
    app.run(host='localhost' , port=5000)
