import cv2
import fourierDescriptor as fd
import efd

MIN_DESCRIPTOR = 500
NUMBER_OF_HARMONICS = 20
# 二值化处理
def binaryMask(frame, x0, y0, width, height):
    cv2.rectangle(frame, (x0, y0), (x0 + width, y0 + height), (0, 255, 0))  # 画出截取的手势框图
    roi = frame[y0:y0 + height, x0:x0 + width]  # 获取手势框图
    res = skinMask(roi)  # 进行肤色检测
    # roi = topolar(roi)
    # cv2.imshow("roi", roi) #显示手势框图
    # cv2.imshow("res", res) #显示肤色检测后的图像
    ret, fourier_result = fd.fourierDesciptor(res)
    efd_result, K, T = efd.elliptic_fourier_descriptors(res)
    return roi, res, ret, fourier_result, efd_result
    # 肤色检测
####YCrCb颜色空间的Cr分量+Otsu法阈值分割算法
def skinMask(roi):
    YCrCb = cv2.cvtColor(roi, cv2.COLOR_BGR2YCR_CB)  # 转换至YCrCb空间
    (y, cr, cb) = cv2.split(YCrCb)  # 拆分出Y,Cr,Cbの値
    cr1 = cv2.GaussianBlur(cr, (5, 5), 0)
    _, skin = cv2.threshold(cr1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)  # Ostu处理
    res = cv2.bitwise_and(roi, roi, mask=skin)
    return res