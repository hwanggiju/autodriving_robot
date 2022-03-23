from glob import glob
from flask import Flask, Response, render_template, request
import cv2
import face_recognition
import numpy as np
from threading import Thread
import time 

global user, switch, name
user = 0
switch = 1
user = ' '

obama_image = face_recognition.load_image_file("C:/opencv/development/face/obama.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

biden_image = face_recognition.load_image_file("C:/opencv/development/face/biden.jpg")
biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

giju_image = face_recognition.load_image_file("C:/opencv/development/face/giju_small_image.jpg")
giju_face_encoding = face_recognition.face_encodings(giju_image)[0]

known_face_encodings = [
    obama_face_encoding,
    biden_face_encoding,
    giju_face_encoding
]
known_face_names = [
    "Barack Obama",
    "Joe Biden",
    "giju"
]

app = Flask(__name__)

cap = cv2.VideoCapture(0)

def user_detect(frame) :
    global name
    rgb_frame = frame[:, :, ::-1]
    
    face_locations = face_recognition.face_locations(rgb_frame) # 찾은 얼굴 값
    
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations) # 얼굴 인코딩
    
    for face_encoding in face_encodings:
    
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            return name
    return name   
    
def gen_frame():
    global user
    while True:
        success, frame = cap.read()
        if success:
            if (user) :
                user = 0
                name = user_detect(frame)
            try :
                ret, jpeg = cv2.imencode('.jpg', cv2.flip(frame, 1)) # 프레임 -> 메모리 버퍼로 인코딩
                frame = jpeg.tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n') # HTTP 응답으로 전송하는데 필요한 형식으로 전환
            except Exception as e:
                pass
        else :
            pass
        
@app.route('/')
def index():
    return render_template('main.html')

@app.route('/stream')
def stream():
    return Response(gen_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/requests', methods=['POST', 'GET'])
def tasks() :
    global switch, cap, name
    if request.method == 'POST' :
        if request.form.get('clicked') == 'User':
            global user
            user = 1
            
        elif request.form.get('stop') == 'Stop/Start':
            if(switch==1):
                switch = 0
                cap.release()
                cv2.destroyAllWindows()
            else :
                cap = cv2.VideoCapture(0)
                switch = 1
                
    elif request.method == 'GET' :
        return render_template('main.html')
    
    return render_template('main.html', value=name)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)