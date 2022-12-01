import time

import cv2
import mss
import numpy as np
import pynput

# 识别数据
data = {
    166: '3030',
    111: 'CAR',
    163: 'EVA8',
    196: 'G7',
    379: 'LSTAR',
    274: 'P2020',
    294: 'R301',
    290: 'R99',
    362: 'RE45',
    306: '三重',
    256: '专注',
    358: '克雷贝尔',
    288: '刀刃',
    325: '和平',
    232: '哈沃克',
    308: '哨兵',
    254: '喷火',
    217: '小帮手',
    179: '平行',
    95: '暴走',
    172: '波塞克',
    197: '滋崩',
    273: '猎兽',
    255: '獒犬',
    301: '电能',
    188: '莫桑比克',
    280: '赫姆洛克',
    351: '转换者',
    56: '长弓',
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
        region = (2950, 1379, 163, 25)
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
