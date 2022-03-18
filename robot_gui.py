from curses import baudrate
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import cv2
import numpy as np
import face_recognition
import sys
import serial
import time
import serial

class Robot_UI(QDialog):
    def __init__(self):
        super().__init__()
        self.UIReset1()
        
    def UIReset1(self):
        tabs = QTabWidget()
        
        tabs.addTab(Camera_tab(), 'Camera')
        tabs.addTab(Radar_tab(), 'Map')
        tabs.addTab(Motor_tab(), 'Motor')
        
        vbox = QVBoxLayout()
        vbox.addWidget(tabs)
        
        self.setLayout(vbox)
        
        self.setWindowTitle('Robot_Control_UI')
        self.setGeometry(500, 500, 700, 500)
        self.show()
        
class Camera_tab(QWidget):
    def __init__(self):
        super().__init__()
        self.UIReset2()
        
    def UIReset2(self):
        self.btn1 = QPushButton("Video")
        self.btn2 = QPushButton("User Detect")
        
        self.btn1.clicked.connect(self.streaming_mode)
        self.btn2.clicked.connect(self.face_rec_mode)
        
        self.label = QLabel("원하는 모드를 선택해주세요.")
        
        vbox = QVBoxLayout(self)
        vbox.addWidget(self.label, alignment=Qt.AlignCenter)
        vbox.addWidget(self.btn1)
        vbox.addWidget(self.btn2)
        
    def streaming_mode(self):
        sender = self.sender()
        cap = cv2.VideoCapture(0)
        print("camera is Opened")
        delay = int(1000 / cap.get(cv2.CAP_PROP_FPS)) 
        while True:
            ret, img = cap.read()
            if ret:
                cv2.imshow('Camera', img)
                if cv2.waitKey(delay) & 0xFF == 27:
                    print("Good Bye~!!")
                    break
            else:
                print(ret, img)
                break
        cap.release()
        cv2.destroyAllWindows()
                
    def face_rec_mode(self):
        sender = self.sender()
        obama_image = face_recognition.load_image_file("obama_small.jpg")
        obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

        biden_image = face_recognition.load_image_file("biden.jpg")
        biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

        giju_image = face_recognition.load_image_file("giju_small_image.jpg")
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
        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True

        cap = cv2.VideoCapture(0)
        
        if cap.isOpened():
            print("camera open")
            while True:
                ret, frame = cap.read()
                small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

                rgb_small_frame = small_frame[:, :, ::-1]

                if process_this_frame:
                    face_locations = face_recognition.face_locations(rgb_small_frame)
                    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                    face_names = []
                    for face_encoding in face_encodings:
                        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                        
                        name = "Unknown"
                        
                        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                        best_match_index = np.argmin(face_distances)
                        if matches[best_match_index]:
                            name = known_face_names[best_match_index]
                        print("{}".format(name))
                        
                        face_names.append(name)

                process_this_frame = not process_this_frame

                cv2.imshow('Video', frame)

                if cv2.waitKey(1) & 0xFF == 27:
                    print("Good Bye~!!\nNext Command Input")
                    break
        cap.release()
        cv2.destroyAllWindows()
                
class Radar_tab(QWidget):
    def __init__(self):
        super().__init__()
        self.UIReset3()
        
    def UIReset3(self):
        self.text = '준비 중...'
        
    def paintEvent(self, event):
        paint = QPainter()
        paint.begin(self)
        self.drawText(event, paint)
        paint.end()
        
    def drawText(self, event, paint):
        paint.drawText(event.rect(), Qt.AlignCenter, self.text)
        
class Motor_tab(QWidget):
    def __init__(self):
        super().__init__()
        self.UIReset4()
        
    def UIReset4(self) :
        self.text_edit = QTextEdit()
        
        self.btn_clear = QPushButton('Clear')
        self.btn_clear.clicked.connect(self.clearText)

        self.btn_add = QPushButton('Start')
        self.btn_add.clicked.connect(self.addText)
                    
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.text_edit)
        self.vbox.addWidget(self.btn_add)
        self.vbox.addWidget(self.btn_clear)
        
        self.setLayout(self.vbox)
        
    def addText(self) :
        self.port = '/dev/ttyACM1'
        self.brate = 9600
        self.ser = serial.Serial(self.port, self.brate, timeout=None)
        cnt = 0
        while cnt < 10 :
            data = self.ser.readline()
            if data :
                self.text_edit.appendPlainText(data.decode()[:len(data)-1])
                cnt += 1
    def clearText(self) :
        self.text_edit.clear()
        
program = QApplication(sys.argv)
exec_inst = Robot_UI()
program.exec_()
            