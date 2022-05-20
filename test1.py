from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import os

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.btn_start = QPushButton('start')
        self.btn_start.clicked.connect(self.addText)
        
        self.btn_stop = QPushButton('stop')
        self.btn_start.clicked.connect(self.stopText)
        self.tb = QTextBrowser()        

        vbox = QVBoxLayout()
        vbox.addWidget(self.btn_start)
        vbox.addWidget(self.btn_stop)
        vbox.addWidget(self.tb)

        self.setLayout(vbox)
        
        self.setWindowTitle('test')
        self.setGeometry(500, 500, 500, 600)
        self.show()
        
    def addText(self) :
        while (True) :
            self.result = os.system("C:/opencv/development/face/dist/test.exe")
            self.tb.append(self.result)
            if self.btn_stop :
                self.stopText()
            
    def stopText(self) :
        self.tb.clear()

app = QApplication(sys.argv)
inst = MainWindow()
app.exec_()