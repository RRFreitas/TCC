from flask import Flask, render_template, Response, jsonify, request
from client.Camera import Camera
import face_recognition

app = Flask(__name__)

video_camera = None
global_frame = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reconhecer')
def reconhecer():
    enc = gerar_encoding()
    print(enc)
    return str(len(enc))

def gerar_encoding():
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
    app.run(host='0.0.0.0')