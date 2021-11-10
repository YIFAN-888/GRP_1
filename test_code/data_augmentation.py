import random
import cv2

path = './' + 'test_image' + '/'
# 旋转
def rotate(image, scale=0.9):
    angle = random.randrange(-90, 90)  # random角度
    w = image.shape[1]
    h = image.shape[0]
    M = cv2.getRotationMatrix2D((w / 2, h / 2), angle, scale)
    image = cv2.warpAffine(image, M, (w, h))
    return image

if __name__ == "__main__":
    for i in range(1, 6):
        cnt = 1  # 计数
        for j in range(1,6):
            roi = cv2.imread(path + str(i) + '_' + str(j) + '.png')
            for k in range(2):
                img_rotation = rotate(roi)  # 旋转
                cv2.imwrite(path + str(i) + '_' + str(cnt) + '.png', img_rotation)
                cnt += 1
                img_flip = cv2.flip(img_rotation, 1)  # 翻转
                cv2.imwrite(path + str(i) + '_' + str(cnt) + '.png', img_flip)
                cnt += 1
            print(i, '_', j, '完成')