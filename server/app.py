from flask import Flask, render_template, Response, jsonify, request
import face_recognition
import sys
import os

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello"

def run(host='0.0.0.0', debug=False):
    port = int(os.environ.get("PORT", 5000))
    app.debug = debug
    app.run(host=host, port=port)

if __name__ == "__main__":
    run(debug='-d' in sys.argv or '--debug' in sys.argv)