import cv2 as cv
import numpy as np

capture = cv.VideoCapture(0)


def _get_eucledian_distance(vect1, vect2):
    distant = vect1[0] - vect2[0]
    dist = np.sqrt(np.sum(np.square(distant)))

    return dist


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
# gesture_recognition_two()

cv.waitKey(0)
capture.release()
cv.destroyAllWindows()