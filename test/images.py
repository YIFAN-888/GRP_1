import cv2
import random

from data_augmentation import rotate, path

img_path = 'test.jpg'
image = cv2.imread(filename=img_path)
rows,cols = image.shape[:2]
#第一个参数旋转中心，第二个参数旋转角度，第三个参数：缩放比例
M = cv2.getRotationMatrix2D((cols/1.6,rows/3.7), 35, 0.5)
#第三个参数：变换后的图像大小
new_image = cv2.warpAffine(image,M,(rows,cols))

smaller_image = cv2.resize(src=image,dsize=None,fx=2,fy=1)

#cv2.imshow('raw image',image)

#Graphics=cv2.imshow(winname='smaller image',mat=smaller_image)
Graphics=cv2.imshow('new_image',new_image,)
print(Graphics)

#cv2.imshow('new_image',new_image,)

#winname弹出窗口的名字，mat为传入的图片对象

#cv2.imshow(winname='show the image',mat=image)

#窗口默认一直处于弹出窗状态
cv2.waitKey()
#按任意键盘，销毁窗口
cv2.destroyAllWindows()
