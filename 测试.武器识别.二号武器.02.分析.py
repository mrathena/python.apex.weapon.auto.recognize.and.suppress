import os

import cv2
import numpy as np


def load(directory):
    """
    递归载入指定路径下的所有图片(灰度化二值化), 按照 (name, img) 的格式组合成为列表并返回
    """
    imgs = []
    for item in os.listdir(directory):
        # item, 不包含路径前缀
        # path, 完整路径
        path = os.path.join(directory, item)
        if os.path.isdir(path):
            temp = load(path)
            imgs.extend(temp)
        elif os.path.isfile(path):
            # 读取图片并灰度化
            img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
            imgs.append((os.path.splitext(item)[0], img))
    return imgs if imgs else None


rets = load(r'image/3440.1440/two')
data = dict()
repeat = []
for name, img in rets:
    height, width = img.shape
    counter = 0
    for row in range(0, height):
        for col in range(0, width):
            if 255 == img[row, col]:
                counter += 1
    prev = data.get(counter)
    if prev is None:
        data[counter] = name
    else:
        repeat.append([prev, name])
        if isinstance(prev, list):
            prev.append(name)
        else:
            data[counter] = [prev, name]


print('---------- ---------- ---------- ---------- ----------')
for k, v in data.items():
    name = f'{v}' if isinstance(v, list) else f"'{v}'"
    print(f'\t{k}: {name},')
print('---------- ---------- ---------- ---------- ----------')
print(repeat)
