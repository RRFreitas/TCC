#!/usr/bin/env python3

from flask import Flask, render_template, Response, jsonify, request, flash
from Camera import Camera
import face_recognition
import cv2
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
        enc = gerar_encoding_camera()
        print(enc)
        if (len(enc) != 1):
            raise Exception("Nenhuma ou mais de uma face.")

        payload = {"encoding": enc[0].tolist()}
        r = requests.post("https://rennan.herokuapp.com/api/reconhecer", json=payload)
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
                raise Exception("Má formatação.")

            if(request.form['nome'] == '' or request.form['email'] == ''):
                raise Exception("Má formatação.")
            file = request.files['foto']
            encoding = gerar_encoding(file)

            if(len(encoding) != 1):
                raise Exception("Nenhuma ou mais de uma face.")

            payload = {"nome": request.form['nome'],
                       "email": request.form['email'],
                       "encoding": encoding[0].tolist()}
            r = requests.post("https://rennan.herokuapp.com/api/pessoas", json=payload)
            return Response(r.text)
        except Exception as err:
            print(err)
            return Response(str(err), 400)

def gerar_encoding(file):
    file.save('cache/' + file.filename)
    image = cv2.imread("cache/" + file.filename)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, boxes)
    return encodings

def gerar_encoding_camera():
    small_frame = video_camera.get_small_frame()
    boxes = face_recognition.face_locations(small_frame)
    return face_recognition.face_encodings(small_frame, boxes)

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