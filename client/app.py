#!/usr/bin/env python3

from flask import Flask, render_template, Response, jsonify, request, flash
from Camera import Camera
import requests

app = Flask(__name__)

video_camera = None
global_frame = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reconhecer')
def reconhecer():
    try:
        files = {"foto": video_camera.get_jpg_frame()}
        r = requests.post("https://rennan.herokuapp.com/api/reconhecer", files=files)
        return Response(r.text)
    except Exception as err:
        print(err)
        return Response(str(err), 400)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'GET':
        return render_template('cadastro.html')
    elif request.method == 'POST':
        try:
            if not ('foto' in request.files and 'nome' in request.form and 'email' in request.form):
                raise Exception("Formulário inválido.")

            if(request.form['nome'] == '' or request.form['email'] == ''):
                raise Exception("Formulário inválido.")
            file = request.files['foto']
            files = {"foto": file}
            payload = {"nome": request.form['nome'],
                       "email": request.form['email']}
            print(payload)
            r = requests.post("https://rennan.herokuapp.com/api/pessoas", data=payload, files=files)
            return Response(r.text)
        except Exception as err:
            print(err)
            return Response(str(err), 400)


def video_stream():
    global video_camera
    global global_frame

    if video_camera == None:
        video_camera = Camera()

    while True:
        frame = video_camera.get_jpg_frame()

        if frame != None:
            global_frame = frame
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + global_frame + b'\r\n\r\n')

@app.route('/video_viewer')
def video_viewer():
    return Response(video_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')