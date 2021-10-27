import cv2
import numpy as np
import matplotlib.pyplot as plt

BLUR = 21
CANNY_THRESH_1 = 10
CANNY_THRESH_2 = 200
MASK_DILATE_ITER = 10
MASK_ERODE_ITER = 10
MASK_COLOR = (0.0, 0.0, 1.0)  # In BGR format
# (1:画像を読む)
img = cv2.imread('22.jpg')
#cv2.imwrite('WeChat1.jpg', img)

# (2:画像を白黒（グレースケール）に変換する)

# plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# (3:検査)
edges = cv2.Canny(gray, CANNY_THRESH_1, CANNY_THRESH_2)
edges = cv2.dilate(edges, None)
edges = cv2.erode(edges, None)

# (4:輪郭抽出)
contour_info = []
contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

for c in contours:
    contour_info.append((
        c,
        cv2.isContourConvex(c),
        cv2.contourArea(c),
    ))
contour_info = sorted(contour_info, key=lambda c: c[2], reverse=True)
max_contour = contour_info[0]
# (5:最大の輪郭を持つマスクを作成します)
mask = np.zeros(edges.shape)
cv2.fillConvexPoly(mask, max_contour[0], (255))
# (6:スムーズ)
mask = cv2.dilate(mask, None, iterations=MASK_DILATE_ITER)
mask = cv2.erode(mask, None, iterations=MASK_ERODE_ITER)
mask = cv2.GaussianBlur(mask, (BLUR, BLUR), 0)
mask_stack = np.dstack([mask] * 3)  # Create 3-channel alpha mask
plt.imshow(mask_stack, cmap='gray')
plt.show()

# (7:背景を消す)
mask_stack = mask_stack.astype('float32') / 255.0  # Use float matrices,
img = img.astype('float32') / 255.0  # for easy blending

masked = (mask_stack * img) + ((1 - mask_stack) * MASK_COLOR)  # Blend
masked = (masked * 255).astype('uint8')  # Convert back to 8-bit

c_blue, c_green, c_red = cv2.split(img)

img_a = cv2.merge((c_red, c_green, c_blue, mask.astype('float32') / 255.0))


# plt.imshow(img_a)
# plt.show()

#以上のコードを総合する
def remove_bg(
        path,
        BLUR=21,
        CANNY_THRESH_1=10,
        CANNY_THRESH_2=200,
        MASK_DILATE_ITER=10,
        MASK_ERODE_ITER=10,
        MASK_COLOR=(0.0, 0.0, 1.0),):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray, CANNY_THRESH_1, CANNY_THRESH_2)
    edges = cv2.dilate(edges, None)
    edges = cv2.erode(edges, None)

    contour_info = []
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    for c in contours:
        contour_info.append((
            c,
            cv2.isContourConvex(c),
            cv2.contourArea(c),
        ))
    contour_info = sorted(contour_info, key=lambda c: c[2], reverse=True)
    max_contour = contour_info[0]

    mask = np.zeros(edges.shape)
    cv2.fillConvexPoly(mask, max_contour[0], (255))

    mask = cv2.dilate(mask, None, iterations=MASK_DILATE_ITER)
    mask = cv2.erode(mask, None, iterations=MASK_ERODE_ITER)
    mask = cv2.GaussianBlur(mask, (BLUR, BLUR), 0)
    mask_stack = np.dstack([mask] * 3)

    mask_stack = mask_stack.astype('float32') / 255.0
    img = img.astype('float32') / 255.0

    masked = (mask_stack * img) + ((1 - mask_stack) * MASK_COLOR)
    masked = (masked * 255).astype('uint8')

    c_blue, c_green, c_red = cv2.split(img)

    img_a = cv2.merge((c_red, c_green, c_blue, mask.astype('float32') / 255.0))

    plt.imshow(img_a)
    plt.show()
    return img_a

img_fin = remove_bg(
    path = '22.jpg',
    BLUR = 21,
    CANNY_THRESH_1 = 5,
    CANNY_THRESH_2 = 70,
    MASK_DILATE_ITER = 135,
    MASK_ERODE_ITER = 0,)
fig = plt.figure(frameon=False)
ax = plt.Axes(fig, [0.1, 0., 1., 1.])
ax.set_axis_off()
fig.add_axes(ax)
ax = plt.Axes(fig, [0., 0., 1., 1.])
ax.set_axis_off()
fig.add_axes(ax)
ax.imshow(img_fin)
fig.savefig('fin.png')

