import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

#########图像读取部分
# cap = cv2.VideoCapture('2.wmv')  # 调用目录下的视频
from matplotlib.pyplot import gray

cap = cv.VideoCapture(0)  # 调用摄像头‘0’一般是打开电脑自带摄像头，‘1’是打开外部摄像头（只有一个摄像头的情况）
width = 300
height = 300
cap.set(cv.CAP_PROP_FRAME_WIDTH, width)  # 设置图像宽度
cap.set(cv.CAP_PROP_FRAME_HEIGHT, height)  # 设置图像高度

def gesture_recognition():
    while True:  # 显示图像
        ret, frame = cap.read()  # 读取图像(frame就是读取的视频帧，对frame处理就是对整个视频的处理)
        #print(ret)  #
        #######例如将图像灰度化处理，
        #img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 转灰度图
        fgbg = cv.createBackgroundSubtractorMOG2()
        fgmask = fgbg.apply(frame)
        kernel = np.ones((5, 5), np.uint8)
        fgmask = cv.erode(fgmask, kernel, iterations=1)
        res = cv.bitwise_and(frame, frame, mask=fgmask)
        ycrcb = cv.cvtColor(res, cv.COLOR_BGR2YCrCb)
        (_, cr, _) = cv.split(ycrcb)
        cr1 = cv.GaussianBlur(cr, (5, 5), 0)  # ガウスフィルタリング
        _, skin = cv.threshold(cr1, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

        gesture_roi = skin[0:350, 380:700]
        cv.imshow("dst_demo", skin)



       # cv.imshow("img", img)
        ########動画処理しない状態
        cv.imshow("frame", frame)

        keyword = cv.waitKey(1)
        if keyword == ord('s'):  # 按s保存当前图片
            cv.imwrite('D:/test/1.jpg', skin)
        elif keyword == ord('q'):  # 按q退出
            break

gesture_recognition()
cap.release()  # 释放摄像头
cv.destroyAllWindows()  # 销毁窗口