import cv2 as cv
import numpy as np
import math
import time
import serial

capture = cv.VideoCapture(0)

def _get_eucledian_distance(vect1, vect2):
    distant = vect1[0] - vect2[0]
    dist = np.sqrt(np.sum(np.square(distant)))

    return dist


def gesture_recognition():

    while True:
        ret, frame = capture.read()  # カメラ
        fgbg = cv.createBackgroundSubtractorMOG2()
        fgmask = fgbg.apply(frame)
        kernel = np.ones((5, 5), np.uint8)
        fgmask = cv.erode(fgmask, kernel, iterations=1)
        res = cv.bitwise_and(frame, frame, mask=fgmask)
        ycrcb = cv.cvtColor(res, cv.COLOR_BGR2YCrCb)
        (_, cr, _) = cv.split(ycrcb)
        cr1 = cv.GaussianBlur(cr, (5, 5), 0)  # ガウスフィルタリング
        _, skin = cv.threshold(cr1, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)  # OTSU图像二值化

        gesture_roi = skin[0:350, 380:700]
        cv.imshow("dst_demo", skin)
        # cv.imshow("gesture_roi", gesture_roi)
        contours, heriachy = cv.findContours(gesture_roi, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)  # 获取轮廓点集(坐标)

        for i, contour in enumerate(contours):  # ヴィットーリプロフィール
            cv.drawContours(frame[0:350, 380:700], contours, i, (255, 0, 0), 1)

            x, y, w, h = cv.boundingRect(contour)

            cv.rectangle(frame[0:350, 380:700], (x, y), (x + w, y + h), (100, 100, 0), 1)
        hull = cv.convexHull(contour, True, returnPoints=False)
        defects = cv.convexityDefects(contour, hull)

        ndefects = 0
        if defects is not None:  # 重要!

            for i in range(defects.shape[0]):
                s, e, f, d = defects[i, 0]

                start = tuple(contour[s][0])  #スタート
                end = tuple(contour[e][0])  # 终点
                far = tuple(contour[f][0])  # 遠い点
                a = _get_eucledian_distance(start, end)
                b = _get_eucledian_distance(start, far)
                c = _get_eucledian_distance(end, far)
                angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))
                cv.line(frame[0:350, 380:700], start, end, [255, 255, 0], 2)
                cv.circle(frame[0:350, 380:700], far, 5, [0, 0, 255], -1)
                if angle <= math.pi / 5:  # <30度:
                    ndefects = ndefects + 1
                print("数字 = %f" % ndefects)

        cv.imshow("video", frame)
        c = cv.waitKey(50)
        if c == 27:

            break


def gesture_recognition_two():
    img = cv.imread("E:/pictureprocessing/practice/picture/practice_one.png")
    img = cv.flip(img, 1)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    dst = cv.GaussianBlur(binary, (1, 1), 0)

    contours, heriachy = cv.findContours(dst, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    for i, contour in enumerate(contours):
        cv.drawContours(img, contours, i, (0, 255, 0), 3)
        print(i)

    cv.imshow("img_demo", img)


cv.namedWindow("video")
gesture_recognition()
# gesture_recognition_two()

cv.waitKey(0)
capture.release()
cv.destroyAllWindows()
