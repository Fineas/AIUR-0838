import os
import sys
import cv2
import time
import uuid
import numpy as np
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtWidgets, QtCore
from PySide2.QtMultimedia import QCameraInfo
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread

IMAGES_PATH = "../../train_data/images/categorized/"
LABELS = ["mov_up", "mov_dwn", "mov_lft", "mov_rght", "mov_frt", "mov_bck", "spin_l", "spin_r", "gr_open", "gr_close"]
PREVIEW_TXT = "Pick a gesture you want to capture"
DESCRIPTION = "Press c to save the frame or ESC to exit the program."
CAPTURE_FAIL = "Please select a gesture from the buttons below."
CAPTURE_SUCCESS = "Capture saved successfully!"
BTNS_TXT = ["Recording Move Up", 
            "Recording Move Down",
            "Recording Move Left",
            "Recording Move Right",
            "Recording Move Forward",
            "Recording Move Backward",
            "Recording Gripper Close",
            "Recording Gripper Open",
            "Recording SPIN LEFT",
            "Recording SPIN RIGHT",]

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True
        self._current_gesture = ''

    def setGesture(self, idx):
        print('[*] Setting GESTURE=',LABELS[idx])
        self._current_gesture = LABELS[idx]

    def run(self):
        # capture from web cam
        cap = cv2.VideoCapture(0)
        while self._run_flag:
            ret, self.cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(self.cv_img)

        # shut down capture system
        cap.release()

    def saveCapture(self):
        if self._current_gesture == "":
            print("[*] Error saving capture, please specify a gesture")
            return 0
        else:
            print('[*] Saving Capture to PATH')
            
            folder_path = IMAGES_PATH + '/' + self._current_gesture + '/'
            frame_name = self._current_gesture + '.' + '{}.jpg'.format(str(uuid.uuid1()))

            if not os.path.exists(folder_path):
                print("[*] Creating Directory:", folder_path+frame_name)
                os.makedirs(folder_path)

            cv2.imwrite(folder_path + frame_name, self.cv_img)

            return 1
        

    # Sets run flag to False and waits for thread to finish
    def stop(self):
        self._run_flag = False
        self.wait()


class App(QWidget):

    # init App Window Frame
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data Sample Generator")
        self.window_width = 800
        self.window_height = 730
        self.resize(self.window_width, self.window_height)
        
        # initiate all window components
        self.initAppComponents()

        # create the video capture thread
        self.thread = VideoThread()
        
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        
        # start the thread
        self.thread.start()


    # init App Window Components
    def initAppComponents(self):
        # create the label that holds the image
        self.image_label = QLabel(self)
        self.video_width = 800
        self.video_height = 780
        self.image_label.resize(self.video_width, self.video_height)
        
        # create a text label
        self.textLabel = QLabel( PREVIEW_TXT )
        self.textLabel.setAlignment(Qt.AlignCenter)
        header_font=QtGui.QFont('Arial', 20)
        header_font.setBold(True)
        self.textLabel.setFont(header_font) 

        # create description label
        self.description_label = QLabel( DESCRIPTION )
        self.description_label.setAlignment(Qt.AlignCenter)
        red = QtGui.QColor(255, 0, 0)
        green = QtGui.QColor(34, 139, 34)
        black = QtGui.QColor(0, 0, 0)
        alpha  = 200
        self.red_color = "{r}, {g}, {b}, {a}".format(r = red.red(),
                g = red.green(),
                b = red.blue(),
                a = alpha )
        self.green_color = "{r}, {g}, {b}, {a}".format(r = green.red(),
                g = green.green(),
                b = green.blue(),
                a = alpha )    
        self.black_color = "{r}, {g}, {b}, {a}".format(r = black.red(),
                g = black.green(),
                b = black.blue(),
                a = alpha )        
        self.description_label.setStyleSheet("QLabel { color: rgba("+self.red_color+"); }")

        # create a buttons
        btn_j1 = QPushButton( 'Move Up' ); btn_j1.clicked.connect(lambda: self.btnHandler(1))
        btn_j2 = QPushButton( 'Move Down' ); btn_j2.clicked.connect(lambda: self.btnHandler(2))
        btn_j3 = QPushButton( 'Move Left' ); btn_j3.clicked.connect(lambda: self.btnHandler(3))
        btn_j4 = QPushButton( 'Move Right' ); btn_j4.clicked.connect(lambda: self.btnHandler(4))
        btn_j5 = QPushButton( 'Move Forward' ); btn_j5.clicked.connect(lambda: self.btnHandler(5))
        btn_j6 = QPushButton( 'Move Backward' ); btn_j6.clicked.connect(lambda: self.btnHandler(6))
        btn_stop = QPushButton( 'Gripper Close' ); btn_stop.clicked.connect(lambda: self.btnHandler(7))
        btn_confirm = QPushButton( 'Gripper Open' ); btn_confirm.clicked.connect(lambda: self.btnHandler(9))
        btn_spinL = QPushButton( 'Spin Left' ); btn_spinL.clicked.connect(lambda: self.btnHandler(10))
        btn_spinR = QPushButton( 'Spin Right' ); btn_spinR.clicked.connect(lambda: self.btnHandler(11))

        # create layout for buttons set1 
        window_layout1 = QHBoxLayout()
        window_layout1.addWidget(btn_j1)
        window_layout1.addWidget(btn_j2)
        window_layout1.addWidget(btn_j3)
        window_layout1.addWidget(btn_j4)
        window_layout1.addWidget(btn_j5)
        window_layout1.addWidget(btn_j6)

        # create layout for buttons set2
        window_layout2 = QHBoxLayout()
        window_layout2.addWidget(btn_stop)
        window_layout2.addWidget(btn_confirm)
        window_layout2.addWidget(btn_spinL)
        window_layout2.addWidget(btn_spinR)

        # create main layout to hold both buttons layout + text widget + video
        vertical_layout = QVBoxLayout( self )
        vertical_layout.addWidget(self.textLabel) # text
        vertical_layout.addLayout(window_layout1) # buttons set1
        vertical_layout.addLayout(window_layout2) # buttons set2
        vertical_layout.addWidget(self.image_label) # video
        vertical_layout.addWidget(self.description_label) # description
        self.setLayout(vertical_layout)

    # handle button press
    def btnHandler(self, idx):
        self.thread.setGesture(idx-1)
        self.textLabel.setText(BTNS_TXT[idx-1])
        self.textLabel.setStyleSheet("QLabel { color: rgba("+self.black_color+"); }")

    def keyPressEvent(self, event):
        key = event.key()

        if key & 0xff == 0:
            print('[*] Exiting')
            sys.exit(0)

        elif key == 67:
            # capture frame
            ret = self.thread.saveCapture()
            if ret == 0:
                self.textLabel.setText(CAPTURE_FAIL)
                self.textLabel.setStyleSheet("QLabel { color: rgba("+self.red_color+"); }")
            else:
                self.textLabel.setStyleSheet("QLabel { color: rgba("+self.green_color+"); }")

        else:
            print('[*]',key)

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    # updates the image_label with a new opencv image
    def update_image(self, cv_img):
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)
    
    # convert from an opencv image to QPixmap
    def convert_cv_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.video_width, self.video_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
    


if __name__=="__main__":
    app = QApplication(sys.argv)
    a = App()
    a.show()
    sys.exit(app.exec_())