import sys
from PyQt5.QtWidgets import QApplication, QWidget, QToolTip, \
     QPushButton,QMessageBox,QDesktopWidget, QLabel
from PyQt5.QtGui import QFont,QIcon,QPixmap,QImage
from PyQt5.QtCore import QTimer
import cv2
import picture as pic
import classify as cf
import numpy as np
import os
import win32gui
import win32con
import time
import pyautogui
class myWindow(QWidget):
    def __init__(self,parent = None):
        super(myWindow,self).__init__(parent)

        self.timer_camera = QTimer()
        self.cap = cv2.VideoCapture()
        self.initUI()
        self.slot_init()


    def initUI(self):

        self.mylabel()
        self.myButton()
        self.myLabelPic()
        #self.setFixedSize(670,520)
        self.setGeometry(1250, 500, 670, 520)
        #self.setGeometry(QRectrect)
        #self.center()
        self.setWindowIcon(QIcon('icon.jpg'))
        self.setWindowTitle('PandaAI')


    def mylabel(self):

        label_roi = QLabel('画像',self)
        label_roi.setStyleSheet("QLabel{font-size:18px;}")
        label_roi.resize(60,30)
        label_roi.move(120,15)

        label_res = QLabel('輪郭線', self)
        label_res.setStyleSheet("QLabel{font-size:18px;}")
        label_res.resize(60, 30)
        label_res.move(480, 15)

        label_pre = QLabel('予測', self)
        label_pre.setStyleSheet("QLabel{font-size:20px;}")
        label_pre.resize(50,30)
        label_pre.move(400,400)

        label_result = QLabel('結果', self)
        label_result.setStyleSheet("QLabel{font-size:20px;}")
        label_result.resize(50, 30)
        label_result.move(400,430)

    def myLabelPic(self):
        self.label_show_roi = QLabel(self)
        self.label_show_roi.setFixedSize(301,301)
        self.label_show_roi.move(20,50)
        self.label_show_roi.setStyleSheet("QLabel{background:white;}")
        self.label_show_roi.setAutoFillBackground(True)

        self.label_show_ret = QLabel(self)
        self.label_show_ret.setFixedSize(301, 301)
        self.label_show_ret.move(350, 50)
        self.label_show_ret.setStyleSheet("QLabel{background:white;}")
        self.label_show_ret.setAutoFillBackground(True)

        self.label_show_recognition = QLabel('0',self)
        self.label_show_recognition.setStyleSheet("QLabel{background:white;}")
        self.label_show_recognition.setStyleSheet("QLabel{font-size:25px;}")
        self.label_show_recognition.setFixedSize(200,100)
        self.label_show_recognition.move(450, 380)
        self.label_show_recognition.setAutoFillBackground(True)

    def myButton(self):
        QToolTip.setFont(QFont('SansSerif', 10))

        self.button_open_camera = QPushButton('カメラON', self)
        self.button_open_camera.setToolTip('按i,k,j,l可以进行上下左右调整')
        self.button_open_camera.resize(100,30)
        self.button_open_camera.move(100, 400)

        self.butoon_recognition = QPushButton('予測スタート', self)
        self.butoon_recognition.setFixedSize(100, 30)
        self.butoon_recognition.move(100, 450)


    def slot_init(self):
        self.button_open_camera.clicked.connect(self.button_open_camera_click)
        self.butoon_recognition.clicked.connect(self.button_recognition_click)
        #self.butoon_recognition.clicked.connect(self.recognition())
        self.timer_camera.timeout.connect(self.show_camera)

    def button_open_camera_click(self):
        if self.timer_camera.isActive() == False:
            self.cap.open(0)
            self.timer_camera.start(30)
            self.button_open_camera.setText(u'カメラOFF')
            #print('1')
        else:
            self.timer_camera.stop()
            self.cap.release()
            self.label_show_roi.clear()
            self.label_show_ret.clear()
            self.label_show_recognition.setText('0')
            self.button_open_camera.setText(u'カメラON')
            #print('2')

    def button_recognition_click(self):
        #while self.timer_camera.isActive() == True:
            descirptor_in_use = abs(self.fourier_result)
            fd_test = np.zeros((1, 31))

            temp = descirptor_in_use[1]
            for k in range(1, len(descirptor_in_use)):
                fd_test[0, k - 1] = int(100 * descirptor_in_use[k] / temp)
            efd_test = np.zeros((1, 15))
            for k in range(1, len(self.efd_result)):
                temp = np.sqrt(self.efd_result[k][0] ** 2 + self.efd_result[k][1] ** 2) + np.sqrt(
                    self.efd_result[k][2] ** 2 + self.efd_result[k][3] ** 2)
                efd_test[0, k - 1] = (int(1000 * temp))
            #print(fd_test)
            test_knn, test_svm = cf.test_fd(fd_test)
            print("test_knn =", test_knn)
            print("test_svm =", test_svm)
            test_knn_efd, test_svm_efd = cf.test_efd(efd_test)
            print("test_knn_efd =", test_knn_efd)
            print("test_svm_efd =", test_svm_efd)
            num = [0]*7
            num[test_knn[0]] += 1
            num[test_svm[0]] += 1
            num[test_knn_efd[0]] += 1
            num[test_svm_efd[0]] += 1
            res = 0
            for i in range(1, 7):
                if num[i] >= 3:
                    res = i
                    break
            if res == 1:
                self.label_show_recognition.setText('pptを開く')
                os.system('explorer Panda AI.pptx')
                time.sleep(2)
                hwnd_title = {}

                def get_all_hwnd(hwnd, mouse):
                    if (win32gui.IsWindow(hwnd)
                            and win32gui.IsWindowEnabled(hwnd)
                            and win32gui.IsWindowVisible(hwnd)):
                        hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})

                win32gui.EnumWindows(get_all_hwnd, 0)
                hwnd = win32gui.FindWindow(None, "Panda AI.pptx - PowerPoint")
                hwnd1 = win32gui.FindWindow(None, "PandaAI")
                win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                                      win32con.SWP_NOMOVE | win32con.SWP_NOACTIVATE | win32con.SWP_NOOWNERZORDER | win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE)
                win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                                      win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE | win32con.SWP_NOMOVE)
                win32gui.SetWindowPos(hwnd1, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                                      win32con.SWP_NOMOVE | win32con.SWP_NOACTIVATE | win32con.SWP_NOOWNERZORDER | win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE)
            elif res == 2:
                self.label_show_recognition.setText('スライドショー')
                hwnd_title = {}
                def get_all_hwnd(hwnd, mouse):
                    if (win32gui.IsWindow(hwnd)
                            and win32gui.IsWindowEnabled(hwnd)
                            and win32gui.IsWindowVisible(hwnd)):
                        hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})
                win32gui.EnumWindows(get_all_hwnd, 0)
                hwnd = win32gui.FindWindow(None, "Panda AI.pptx - PowerPoint")
                hwnd1 = win32gui.FindWindow(None, "PandaAI")
                win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                                      win32con.SWP_NOMOVE | win32con.SWP_NOACTIVATE | win32con.SWP_NOOWNERZORDER | win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE)
                win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                                      win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE | win32con.SWP_NOMOVE)
                win32gui.SetWindowPos(hwnd1, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                                      win32con.SWP_NOMOVE | win32con.SWP_NOACTIVATE | win32con.SWP_NOOWNERZORDER | win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE)
                pyautogui.hotkey('f5')
            elif res == 3:
                self.label_show_recognition.setText('次のスライド')
                hwnd_title = {}
                def get_all_hwnd(hwnd, mouse):
                    if (win32gui.IsWindow(hwnd)
                            and win32gui.IsWindowEnabled(hwnd)
                            and win32gui.IsWindowVisible(hwnd)):
                        hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})
                win32gui.EnumWindows(get_all_hwnd, 0)
                hwnd = win32gui.FindWindow(None, "PowerPoint スライド ショー - [Panda AI.pptx] - PowerPoint")
                hwnd1 = win32gui.FindWindow(None, "PandaAI")
                win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                                      win32con.SWP_NOMOVE | win32con.SWP_NOACTIVATE | win32con.SWP_NOOWNERZORDER | win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE)
                win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                                      win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE | win32con.SWP_NOMOVE)
                win32gui.SetWindowPos(hwnd1, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                                      win32con.SWP_NOMOVE | win32con.SWP_NOACTIVATE | win32con.SWP_NOOWNERZORDER | win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE)
                pyautogui.hotkey('down')

            elif res == 4:
                self.label_show_recognition.setText('前のスライド')
                hwnd_title = {}

                def get_all_hwnd(hwnd, mouse):
                    if (win32gui.IsWindow(hwnd)
                            and win32gui.IsWindowEnabled(hwnd)
                            and win32gui.IsWindowVisible(hwnd)):
                        hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})

                win32gui.EnumWindows(get_all_hwnd, 0)
                hwnd = win32gui.FindWindow(None, "PowerPoint スライド ショー - [Panda AI.pptx] - PowerPoint")
                hwnd1 = win32gui.FindWindow(None, "PandaAI")
                win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                                      win32con.SWP_NOMOVE | win32con.SWP_NOACTIVATE | win32con.SWP_NOOWNERZORDER | win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE)
                win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                                      win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE | win32con.SWP_NOMOVE)
                win32gui.SetWindowPos(hwnd1, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                                      win32con.SWP_NOMOVE | win32con.SWP_NOACTIVATE | win32con.SWP_NOOWNERZORDER | win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE)
                pyautogui.hotkey('up')

            elif res == 5:
                self.label_show_recognition.setText('スライドショーを終了')
                hwnd_title = {}

                def get_all_hwnd(hwnd, mouse):
                    if (win32gui.IsWindow(hwnd)
                            and win32gui.IsWindowEnabled(hwnd)
                            and win32gui.IsWindowVisible(hwnd)):
                        hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})

                win32gui.EnumWindows(get_all_hwnd, 0)
                hwnd = win32gui.FindWindow(None, "PowerPoint スライド ショー - [Panda AI.pptx] - PowerPoint")
                hwnd1 = win32gui.FindWindow(None, "PandaAI")
                win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                                      win32con.SWP_NOMOVE | win32con.SWP_NOACTIVATE | win32con.SWP_NOOWNERZORDER | win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE)
                win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                                      win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE | win32con.SWP_NOMOVE)
                win32gui.SetWindowPos(hwnd1, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                                      win32con.SWP_NOMOVE | win32con.SWP_NOACTIVATE | win32con.SWP_NOOWNERZORDER | win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE)
                pyautogui.hotkey('esc')

            elif res == 6:
                self.label_show_recognition.setText('閉める')
                hwnd_title = {}

                def get_all_hwnd(hwnd, mouse):
                    if (win32gui.IsWindow(hwnd)
                            and win32gui.IsWindowEnabled(hwnd)
                            and win32gui.IsWindowVisible(hwnd)):
                        hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})

                win32gui.EnumWindows(get_all_hwnd, 0)
                hwnd = win32gui.FindWindow(None, "Panda AI.pptx - PowerPoint")
                hwnd1 = win32gui.FindWindow(None, "PandaAI")
                win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                                      win32con.SWP_NOMOVE | win32con.SWP_NOACTIVATE | win32con.SWP_NOOWNERZORDER | win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE)
                win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                                      win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE | win32con.SWP_NOMOVE)
                win32gui.SetWindowPos(hwnd1, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                                      win32con.SWP_NOMOVE | win32con.SWP_NOACTIVATE | win32con.SWP_NOOWNERZORDER | win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE)
                pyautogui.hotkey('alt','f4')

            print(res)


    def show_camera(self):
        width, height = 300, 300  # 设置拍摄窗口大小
        x0, y0 = 300, 100  # 设置选取位置
        flag, frame = self.cap.read()
        roi, res, ret, self.fourier_result, self.efd_result = pic.binaryMask(frame, x0, y0, width, height)
        roi = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
        show_roi = QImage(roi.data, roi.shape[1], roi.shape[0], QImage.Format_RGB888)
        show_ret = QImage(ret.data, ret.shape[1], ret.shape[0], QImage.Format_Grayscale8)
        self.label_show_roi.setPixmap(QPixmap.fromImage(show_roi))
        self.label_show_ret.setPixmap(QPixmap.fromImage(show_ret))


    def closeEvent(self, QCloseEvent):
        reply = QMessageBox.question(self, 'メッセージ:',"閉めてよろしいですか？",
                                     QMessageBox.Yes |QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            if self.cap.isOpened():
                self.cap.release()
            if self.timer_camera.isActive():
                self.timer_camera.stop()
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = myWindow()
    #cam = win.button_open_camera_click()
    #win.show_camera()
    #win.timer_camera.timeout.connect(win.show_camera())
    win.show()

    while win.timer_camera.isActive() == True:

        win.label_show_recognition.setText('2s后预测')
        time.sleep(2)
        win.button_recognition_click()
        win.label_show_recognition.setText('4s后预测')
        time.sleep(2)
        if win.timer_camera.isActive() == False:
            print('退出')
            break
    #print('1')
    sys.exit(app.exec())