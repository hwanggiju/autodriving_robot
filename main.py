from base64 import encode
from cgi import print_form
from codecs import backslashreplace_errors
from glob import glob
from multiprocessing.sharedctypes import Value
from pickle import TRUE
from pickletools import read_uint1
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

'''

BackEnd 
python-Flask 활용

'''

try :
    # 전역변수 선언
    global user, switch, name
    # 사용자 얼굴 인식 확인
    user = 0
    # 카메라 동작 on/off 확인 1 : on, 0 : off
    switch = 1
    # 사용자 이름 기본값
    name = 'Unknown'
    # 아두이노 시리얼 포트 넘버와 brate 설정 
    port = '/dev/ttyACM0'
    brate = 115200

    # 이미지 파일 dlib 라이브러리를 활용한 이미지 학습
    obama_image = face_recognition.load_image_file("image_dir/obama.jpg") # 이미지 로드
    obama_face_encoding = face_recognition.face_encodings(obama_image)[0] # 이미지 인코딩 후 데이터 저장

    biden_image = face_recognition.load_image_file("image_dir/biden.jpg") # 이미지 로드
    biden_face_encoding = face_recognition.face_encodings(biden_image)[0] # 이미지 인코딩 후 데이터 저장

    giju_image = face_recognition.load_image_file("image_dir/giju_image.jpg") # 이미지 로드
    giju_face_encoding = face_recognition.face_encodings(giju_image)[0] # 이미지 인코딩 후 데이터 저장

    # 이미지 인코딩 데이터 리스트 저장
    known_face_encodings = [
        obama_face_encoding,
        biden_face_encoding,
        giju_face_encoding
    ]
    # 인코딩 데이터 리스트와 매칭되는 고유값 리스트
    known_face_names = [
        "Barack Obama",
        "Joe Biden",
        "Gi ju"
    ]
    # 어플리케이션 선언
    app = Flask(__name__, static_url_path='/static')

    # 카메라 device 연결
    cap = cv2.VideoCapture(0)

    # 사용자 얼굴 감지 구현 함수
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
        
    # 카메라 frame 읽어오고 웹에서 표현하는 형식으로 인코딩해주는 함수
    def gen_frame(cap):
        # 웹 브라우저에서 객체 인식하라는 버튼 입력을 받으면, 
        # 객체 인식 함수를 실행하기 위한 신호를 알려주기 위한 변수
        global user 
        while True:
            success, frame = cap.read() # 카메라 읽기
            if success:
                # 스트리밍과 같이 동작하면, 스트리밍 속도 저하 문제
                # 객체 인식이 필요한 상황에만 적용할 수 있도록 작업하였음.
                if (user) : 
                    user = 0
                    name = user_detect(frame) # 객체 인식 함수
                try :
                    ret, jpeg = cv2.imencode('.jpg', cv2.flip(frame, 1)) # 프레임 -> 메모리 버퍼로 인코딩
                    frame = jpeg.tobytes()
                    # HTTP 응답으로 전송하는데 필요한 형식으로 전환
                    yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n') 
                except Exception as e:
                    pass
            else :
                pass

    # 웹 기본 화면 - 카메라 실시간 화면 표시
    @app.route('/')
    def index():
        return render_template('main.html')

    # 데이터 그래프 화면 - 모터값을 표시
    @app.route('/Sensor')
    def bridge_sensor():
        return render_template('index.html')

    # 지도 그려주는 화면 - 현재 미완성 작성중
    @app.route("/Map")
    def bridge_map():
        # 0 : no data, 1 : 라이다 센싱, 2 : 벽, 3 : 목적지, 4 : 빈공간, 5 : 현재 로봇 위치, 6 : 경로 
        # csv 파일 읽어오고 데이터 처리하다가 다시 텍스트 파일로 읽어오는 코드로 바꿈
        # 현한 : 비트맵 파일 형식 저장, 시도해보아야 함.
        with open("map.txt", mode = "rt", encoding = 'utf-8') as f :
            line = f.readlines()
            tmp_lst = [[] for i in range(1000)]
            item_lst = list(line) # 문자열 리스트에 저장
        
        return render_template('map.html', string_lst = item_lst)

    # 데이터 그래프 실시간으로 그려주는 동적 함수 - 자바 코드와 연동됨
    @app.route('/live-data')
    def live_data():
        # 아두이노 Serial 데이터 읽어오기 위한 설정값
        ser = serial.Serial(port, brate, timeout=None)
        # Serial 데이터 읽어오기
        SerialData = ser.readline()
        # [:len(SerialData)]
        SerialData = SerialData.decode(errors='ignore')[:4] # 읽어온 데이터 슬라이싱
        # print(SerialData)
        # 시간과 Serial 데이터 값 리스트 형식 저장
        data = [time() * 1000,  SerialData] # random() * 100 
        # 자바 함수의 입력으로 반환
        response = make_response(json.dumps(data))
        response.content_type = 'application/json'
        return response
    
    # 카메라 실시간 스트리밍 화면 보여주는 함수
    @app.route('/stream')
    def stream():
        global cap
        return Response(gen_frame(cap), \
                        mimetype='multipart/x-mixed-replace; boundary=frame')

    # 웹 브라우저 신호 입력으로 받아서 처리되는 부분
    @app.route('/requests', methods=['POST', 'GET'])
    def tasks() :
        global switch, name, cap
        # POST 메서드를 사용하여 웹 브라우저의 신호를 받음
        if request.method == 'POST' :
            # 객체 인식 버튼 입력 시
            if request.form.get('clicked') == 'User':
                global user
                user = 1
            # 스트리밍 ON/OFF 버튼 입력 시
            elif request.form.get('camera_stop') == 'Stop/Start':
                if(switch==1):
                    switch = 0
                    cap.release()
                else :
                    cap = cv2.VideoCapture(0)
                    switch = 1
        # GET 메서드를 사용할 가능성으로 작성만 해놓은 것.
        # 실제로 사용되는 곳은 아직 없음.
        elif request.method == 'GET' :
            return render_template('main.html')
        return render_template('main.html', value = name)
        
    # 모터 동작 명령 수행
    # stop, front, left, right, back, reset, Pos 명령어
    @app.route('/requests1', methods=['POST'])
    def gostop() :
        try:
            ser = serial.Serial(port, brate)
            data = ser.readline()
            data = data.decode(errors='ignore')[:len(data)-2]
            print(data)
            direction = ''
            if request.method == 'POST' :
                if request.form.get('s') == 'stop' :
                    direction = 'STOP'
                    ser.write('stop'.encode())
                if request.form.get('f') == 'front' :
                    direction = '전진'
                    ser.write('front'.encode())
                if request.form.get('l') == 'left' :
                    direction = '좌회전'
                    ser.write('left'.encode())
                if request.form.get('r') == 'right' :
                    direction = '우회전'
                    ser.write('right'.encode())
                if request.form.get('b') == 'back' :
                    direction = '후진'
                    ser.write('back'.encode())
                if request.form.get('R') == 'Reset' :
                    direction = '초기화'
                    ser.write('reset'.encode())
                if request.form.get('P') == 'Pos' :
                    direction = '위치 저장'
                    ser.write('Pos'.encode())
            return render_template('index.html', value=direction, encode='utf-8')
        
        # 시리얼 오류 예외 처리 -> 동작에 영향 x, 무시 가능한 오류
        except serial.serialutil.SerialException:
            return render_template('index.html')

    if __name__ == '__main__':
        # 웹 서버 실행
        app.run(host='0.0.0.0', threaded=True, debug=True)
        
except KeyboardInterrupt :
    pass