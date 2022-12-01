import time

import cv2
import mss
import numpy as np
import pynput

# 识别数据
data = {
    161: '3030',
    109: 'CAR',
    150: 'EVA8',
    197: 'G7',
    367: 'LSTAR',
    271: ['P2020', '电能'],
    282: 'R301',
    276: 'R99',
    330: 'RE45',
    311: '三重',
    241: '专注',
    339: '克雷贝尔',
    307: '刀刃',
    293: '和平',
    251: '哈沃克',
    327: '哨兵',
    239: '喷火',
    199: '小帮手',
    157: '平行',
    91: '暴走',
    186: '波塞克',
    194: '滋崩',
    259: '猎兽',
    224: '獒犬',
    217: '莫桑比克',
    323: '赫姆洛克',
    350: '转换者',
    54: '长弓',
}


def mouse():

    sct = mss.mss()

    def grab(region):
        left, top, width, height = region
        return sct.grab(monitor={'left': left, 'top': top, 'width': width, 'height': height})

    def recognize(img):
        """
        入参图片需为 OpenCV 格式
        """
        # 截图灰度化
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 数纯白色点
        height, width = img.shape
        counter = 0
        for row in range(0, height):
            for col in range(0, width):
                if 255 == img[row, col]:
                    counter += 1
        return data.get(counter)

    def cost(interval):
        """
        输入纳秒间距, 转换为合适的单位
        """
        if interval < 1000:
            return f'{interval}ns'
        elif interval < 1_000_000:
            return f'{interval / 1000}us'
        elif interval < 1_000_000_000:
            return f'{interval / 1_000_000}ms'
        else:
            return f'{interval / 1_000_000_000}s'

    def show():
        region = (3145, 1379, 163, 25)
        t1 = time.perf_counter_ns()
        img = grab(region)
        img = cv2.cvtColor(np.array(img), cv2.COLOR_BGRA2BGR)
        name = recognize(img)
        t2 = time.perf_counter_ns()
        print('----------')
        print(f'{name}, {cost(t2 - t1)}')

    def down(x, y, button, pressed):
        if pressed:
            # 鼠标, 侧上键:结束, 侧下键:识别
            if button == pynput.mouse.Button.x2:
                return False
            elif button == pynput.mouse.Button.right:
                show()

    with pynput.mouse.Listener(on_click=down) as m:
        m.join()


mouse()
