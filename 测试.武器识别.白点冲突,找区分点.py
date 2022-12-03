import cv2
import numpy as np

img1 = cv2.imdecode(np.fromfile(r'image/3440.1440/two/P2020.png', dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
img2 = cv2.imdecode(np.fromfile(r'image/3440.1440/two/电能.png', dtype=np.uint8), cv2.IMREAD_GRAYSCALE)

height, width = img1.shape
counter = 0  # 统计纯白色点个数
for row in range(0, height):
    for col in range(0, width):
        if 255 == img1[row, col] and 255 != img2[row, col]:
            print(f'img1 可用点 {col, row}, 写到配置里要写 {row, col}')
        if 255 != img1[row, col] and 255 == img2[row, col]:
            print(f'img2 可用点 {col, row}, 写到配置里要写 {row, col}')

print(img1[4][104])
print(img1[3][84])
