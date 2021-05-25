# -*- coding: utf-8 -*-

""" Graphical User Interface Components """

import os
import sys
import cv2
import time
import uuid
sys.path.append('../ur3e library/')
import ur_lib
import numpy as np
from detect import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtWidgets, QtCore
from PySide2.QtMultimedia import QCameraInfo
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread


LABELS = ["mov_up", "mov_dwn", "mov_lft", "mov_rght", "mov_frt", "mov_bck", "spin_l", "spin_r", "gr_open", "gr_close"]
PROMPT_TXT = ["DETECTING HAND GESTURE...",
              "Moving Up",
              "Moving Down",
              "Moving Left",
              "Moving Right",
              "Moving Forward",
              "Moving Backward",
              "SPINNING THE JOINT TO LEFT",
              "SPINNING THE JOINT TO RIGHT",
              "Opening Grip",
              "Closing Grip"]

"""
:VideoThread
===================================
    : setGesture : setter for the _current_gesture member
    : run : implement the running service for capturing camera frames
    : saveCapture : save current frame 
    : stop : terminate the video feed
"""
class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True
        self._current_gesture = ''
        self.cv_img = ''
        self.detected_label = ''

    def setGesture(self, idx):
        print('[*] Setting GESTURE :',LABELS[idx])
        self._current_gesture = LABELS[idx]

    def run(self):
        print('[*] LIVE Camera')
        for stream in detect():
            if stream[0] == "Busy Camera":
                self.cv_img = cv2.imread("../../img/offline.jpg")
                self.change_pixmap_signal.emit(self.cv_img)
                break
            else:
                self.cv_img = stream[1]
                self.change_pixmap_signal.emit(self.cv_img)
                self.detected_label = stream[0] 
                print("DETECTED=",stream[0])

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
        
    def getDetectedLabel(self):
        return self.detected_label

    def stop(self):
        print('[*] OFFLINE Camera')
        self._run_flag = False
        self.wait()

"""
:Ui_MainWindow
===================================
    : setupUi : create UI layout
    : retranslateUi : set UI elements name
    : selectButton : 
    : setPrompt :
    : setOfflineCamera :
    : update_image : updates the image_label with a new opencv image
    : convert_cv_qt : convert from an opencv image to QPixmap
"""
class Ui_MainWindow(object):

    _in_use_btn = None

    def setupUi(self, MainWindow):

        # Create Robot instance
        self.robot = ''
        # self.robot = ur_lib.UR3_Robot()

        # Main Window Settings
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(870, 460)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        # Prompt Messages Frame
        self.textBrowser = QtWidgets.QTextBrowser(self.frame)
        self.textBrowser.setGeometry(QtCore.QRect(480, 0, 371, 291))
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser.setText( PROMPT_TXT[0] )
        self.textBrowser.setAlignment(Qt.AlignCenter)
        header_font=QtGui.QFont('Arial', 20)
        header_font.setBold(True)
        self.textBrowser.setFont(header_font) 
        self.textBrowser.setStyleSheet("QTextBrowser { background: #ffffff; padding-top: 110 }")

        # Controll Buttons
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(480, 300, 131, 41))
        self.pushButton.setObjectName( LABELS[0] )
        self.pushButton.clicked.connect(lambda: self.selectButton(self.pushButton))
        self.pushButton.setStyleSheet("background-color: #e1e1e1")
        self.pushButton_2 = QtWidgets.QPushButton(self.frame)
        self.pushButton_2.setGeometry(QtCore.QRect(610, 300, 121, 41))
        self.pushButton_2.setObjectName( LABELS[1] )
        self.pushButton_2.clicked.connect(lambda: self.selectButton(self.pushButton_2))
        self.pushButton_2.setStyleSheet("background-color: #e1e1e1")
        self.pushButton_3 = QtWidgets.QPushButton(self.frame)
        self.pushButton_3.setGeometry(QtCore.QRect(730, 300, 121, 41))
        self.pushButton_3.setObjectName( LABELS[2] )
        self.pushButton_3.clicked.connect(lambda: self.selectButton(self.pushButton_3))
        self.pushButton_3.setStyleSheet("background-color: #e1e1e1")
        self.pushButton_4 = QtWidgets.QPushButton(self.frame)
        self.pushButton_4.setGeometry(QtCore.QRect(480, 340, 131, 41))
        self.pushButton_4.setObjectName( LABELS[3] )
        self.pushButton_4.clicked.connect(lambda: self.selectButton(self.pushButton_4))
        self.pushButton_4.setStyleSheet("background-color: #e1e1e1")
        self.pushButton_5 = QtWidgets.QPushButton(self.frame)
        self.pushButton_5.setGeometry(QtCore.QRect(610, 340, 121, 41))
        self.pushButton_5.setObjectName( LABELS[4] )
        self.pushButton_5.clicked.connect(lambda: self.selectButton(self.pushButton_5))
        self.pushButton_5.setStyleSheet("background-color: #e1e1e1")
        self.pushButton_6 = QtWidgets.QPushButton(self.frame)
        self.pushButton_6.setGeometry(QtCore.QRect(730, 340, 121, 41))
        self.pushButton_6.setObjectName( LABELS[5] )
        self.pushButton_6.clicked.connect(lambda: self.selectButton(self.pushButton_6))
        self.pushButton_6.setStyleSheet("background-color: #e1e1e1")
        self.pushButton_7 = QtWidgets.QPushButton(self.frame)
        self.pushButton_7.setGeometry(QtCore.QRect(480, 380, 201, 41))
        self.pushButton_7.setObjectName( LABELS[6] )
        self.pushButton_7.clicked.connect(lambda: self.selectButton(self.pushButton_7))
        self.pushButton_7.setStyleSheet("background-color: #e1e1e1")
        self.pushButton_8 = QtWidgets.QPushButton(self.frame)
        self.pushButton_8.setGeometry(QtCore.QRect(680, 380, 171, 41))
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_8.clicked.connect(lambda: self.selectButton(self.pushButton_8))
        self.pushButton_8.setStyleSheet("background-color: #e1e1e1")

        # Live Camera Frame
        self.label = QtWidgets.QLabel(self.frame)
        self.video_width = 470
        self.video_height = 420
        self.label.resize(self.video_width, self.video_height)

        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # Start Video Thread
        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):

        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

        # Set Buttons Name
        self.pushButton.setText(_translate("MainWindow", "Move Up"))
        self.pushButton_2.setText(_translate("MainWindow", "Move Down"))
        self.pushButton_3.setText(_translate("MainWindow", "Move Left"))
        self.pushButton_4.setText(_translate("MainWindow", "Move Right"))
        self.pushButton_5.setText(_translate("MainWindow", "Move Forward"))
        self.pushButton_6.setText(_translate("MainWindow", "Move Backward"))
        self.pushButton_7.setText(_translate("MainWindow", "<--------------"))
        self.pushButton_8.setText(_translate("MainWindow", "-------------->"))

    def selectButton(self, btn):

        if self._in_use_btn != None:
            self._in_use_btn.setStyleSheet("background-color: #e1e1e1")

        self._in_use_btn = btn
        btn.setStyleSheet("background-color: #8fb4cf")
        print('[*] Button',btn.text(),"was pressed")
        if btn.text()[::-1][0].isdigit():
            self.setPrompt( PROMPT_TXT[int(btn.text()[::-1][0])] )
        elif btn.text() == '<--------------':
            self.setPrompt( PROMPT_TXT[7] )
        else:
            self.setPrompt( PROMPT_TXT[8] )

    def setPrompt(self, data):
        self.textBrowser.setText( data )
        self.textBrowser.setAlignment(Qt.AlignCenter)

    def setOfflineCamera(self):
        self.label.setPixmap(QtGui.QPixmap("img/offline.jpg"))

    def update_image(self, cv_img):
        qt_img = self.convert_cv_qt(cv_img)
        self.label.setPixmap(qt_img)

        # update prompt txt based on detection
        data = self.thread.getDetectedLabel()
        if data and data != '0':
            if data[::-1][0] == 's':
                data = data[:len(data)-1] # strip s from end
            self.setPrompt(PROMPT_TXT[LABELS.index(data)+1])
            if data == "mov_up":
                self.selectButton(self.pushButton)
                self.send_command("u")
            elif data == "mov_dwn":
                self.selectButton(self.pushButton_2)
                self.send_command("d")
            elif data == "mov_lft":
                self.selectButton(self.pushButton_3)
                self.send_command("l")
            elif data == "mov_rght":
                self.selectButton(self.pushButton_4)
                self.send_command("r")
            elif data == "mov_frt":
                self.selectButton(self.pushButton_5)
                self.send_command("f")
            elif data == "mov_bck":
                self.selectButton(self.pushButton_6)
                self.send_command("b")
            elif data == "spin_l":
                self.selectButton(self.pushButton_7)
                self.send_command("sl")
            elif data == "spin_r":
                self.selectButton(self.pushButton_8)
                self.send_command("sr")
            elif data == "gr_open":
                self.selectButton(self.pushButton_8)
                self.send_command("o")
            elif data == "gr_close":
                self.selectButton(self.pushButton_8)
                self.send_command("c")
        else:
            # unselect buttons
            self.setPrompt(PROMPT_TXT[0])
            if self._in_use_btn != None:
                self._in_use_btn.setStyleSheet("background-color: #e1e1e1")
    
    def send_command(self, CMD):
        if self.robot:
            self.robot.move_direction(CMD)
            pass

    def convert_cv_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.video_width, self.video_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

