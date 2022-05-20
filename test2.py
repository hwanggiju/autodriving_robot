import sys
from PyQt5.QtWidgets import *

class MyWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):    
        btn = QPushButton("버튼", self)
        btn.clicked.connect(self.surprise)

    def surprise(self):
        print("으엌! 깜짝이야!!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()
    
#해당 코드 실행 시 부터 이벤트 루프 발생 (즉, 이 코드 아래로는 이벤트 발생 전까지 안내려감)
app.exec_()

print("루프 밖")