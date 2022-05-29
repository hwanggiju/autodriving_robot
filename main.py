from glob import glob
from multiprocessing.sharedctypes import Value
from pickle import TRUE
from urllib import response
from flask import Flask, Response, render_template, request, make_response
import cv2
import face_recognition
import numpy as np
from threading import Thread
from time import time 
import serial
from random import random
import json
import os

global user, switch, name
user = 0 
switch = 1 
name = 'Unknown'

# 이미지 학습 전처리
# C:/opencv/development/face/
obama_image = face_recognition.load_image_file("image_dir/obama.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

biden_image = face_recognition.load_image_file("image_dir/biden.jpg")
biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

giju_image = face_recognition.load_image_file("image_dir/giju_image.jpg")
giju_face_encoding = face_recognition.face_encodings(giju_image)[0]

known_face_encodings = [
    obama_face_encoding,
    biden_face_encoding,
    giju_face_encoding
]
known_face_names = [
    "Barack Obama",
    "Joe Biden",
    "Gi ju"
]
# 어플리케이션 선언
app = Flask(__name__, static_url_path='/static')

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
    
def gen_frame(cap):
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

@app.route('/Sensor')
def bridge_sensor():
    return render_template('index.html')

@app.route("/Map")
def bridge_map():
    # 0 : no data, 1 : 라이다 센싱, 2 : 벽, 3 : 목적지, 4 : 빈공간, 5 : 현재 로봇 위치, 6 : 경로 
    with open("map.txt", mode = "rt", encoding = 'utf-8') as f :
        line = f.readlines()
        tmp_lst = [[] for i in range(1000)]
        item_lst = list(line) # 문자열 리스트에 저장
        # string_lst = []
        # cnt = 0
        '''
        for i in item_lst :
            line_lst = list(i) # 문자열 문자 쪼개어 리스트 저장
            # 아스키코드 변환 표 참고
           
            for j in range(0, len(line_lst)) :
                if line_lst[j] == '0':
                    tmp_lst[cnt].append(chr(32))
                elif line_lst[j] == '1' :
                    tmp_lst[cnt].append(chr(49))
                elif line_lst[j] == '2' :
                    tmp_lst[cnt].append(chr(254))
                elif line_lst[j] == '3' :
                    tmp_lst[cnt].append(chr(94))
                elif line_lst[j] == '4' :
                    tmp_lst[cnt].append(chr(92))
                elif line_lst[j] == '5' :
                    tmp_lst[cnt].append(chr(64))
                elif line_lst[j] == '6' :
                    tmp_lst[cnt].append(chr(80))
            cnt += 1
            
        for i in tmp_lst :
            result = ''.join(s for s in i)
            string_lst.append(result)
        '''
    return render_template('map.html', string_lst = item_lst)

@app.route('/live-data')
def live_data():
    '''
    port = '/dev/ttyACM0'
    brate = 9600
    ser = serial.Serial(port, brate, timeout=None)
    senser_data = ser.readline()
    senser_data = float(data.decode()[:len(data)-3])
    '''
    data = [time() * 1000, random() * 100]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

@app.route('/stream')
def stream():
    global cap
    return Response(gen_frame(cap), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/requests', methods=['POST', 'GET'])
def tasks() :
    global switch, name, cap
    
    port = '/dev/ttyACM0'
    brate = 9600
    ser = serial.Serial(port, brate, timeout=None)
    
    if request.method == 'POST' :
        if request.form.get('clicked') == 'User':
            global user
            user = 1
            
        elif request.form.get('camera_stop') == 'Stop/Start':
            if(switch==1):
                switch = 0
                cap.release()
                cv2.destroyAllWindows()
            else :
                cap = cv2.VideoCapture(0)
                switch = 1
        while True :  
            if request.form.get('go') == 'GO' :
                ser.write('g'.encode()) # 아두이노 데이터 전송 (동작 코드는 아두이노에서)
            if request.form.get('motor_stop') == 'STOP' :
                ser.write('s'.encode())
                return
                
    elif request.method == 'GET' :
        return render_template('main.html')
    
    return render_template('main.html', value = name)
        
        # elif request.form.get('stop') == 'STOP' :
        #    ser.write('s'.encode()) # 아두이노 데이터 전송 (동작 코드는 아두이노에서)
        #    return render_template('index.html')
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, debug=True)