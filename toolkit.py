import time
from ctypes import CDLL

import win32api  # conda install pywin32


try:
    driver = CDLL(r'mouse.device.lgs.dll')  # 在Python的string前面加上‘r’, 是为了告诉编译器这个string是个raw string(原始字符串),不要转义backslash(反斜杠) '\'
    ok = driver.device_open() == 1
    if not ok:
        print('初始化失败, 未安装lgs/ghub驱动')
except FileNotFoundError:
    print('初始化失败, 缺少文件')


class Mouse:

    @staticmethod
    def move(x, y, absolute=False):
        if ok:
            mx, my = x, y
            if absolute:
                ox, oy = win32api.GetCursorPos()
                mx = x - ox
                my = y - oy
            driver.moveR(mx, my, True)

    @staticmethod
    def moveHumanoid(x, y, absolute=False):
        """
        仿真移动
        """
        if ok:
            ox, oy = win32api.GetCursorPos()  # 原鼠标位置
            mx, my = x, y  # 相对移动距离
            if absolute:
                mx = x - ox
                my = y - oy
            tx, ty = ox + mx, oy + my
            print(f'({ox},{oy}), ({tx},{ty}), x:{mx},y:{my}')
            # 以绝对位置方式移动(防止相对位置丢失精度)
            adx, ady = abs(mx), abs(my)
            if adx <= ady:
                # 水平方向移动的距离短
                for i in range(1, adx):
                    ix = i if mx > 0 else -i
                    temp = int(ady / adx * abs(ix))
                    iy = temp if my > 0 else -temp
                    Mouse.move(ox + ix, oy + iy, absolute=True)
                    # time.sleep(0.001)
            else:
                # 垂直方向移动的距离短
                for i in range(1, ady):
                    iy = i if my > 0 else -i
                    temp = int(adx / ady * abs(iy))
                    ix = temp if mx > 0 else -temp
                    Mouse.move(ox + ix, oy + iy, absolute=True)
                    # time.sleep(0.001)

    @staticmethod
    def down(code):
        if ok:
            driver.mouse_down(code)

    @staticmethod
    def up(code):
        if ok:
            driver.mouse_up(code)

    @staticmethod
    def click(code):
        """
        :param code: 1:左键, 2:中键, 3:右键, 4:侧下键, 5:侧上键, 6:DPI键
        :return:
        """
        if ok:
            driver.mouse_down(code)
            driver.mouse_up(code)


class Keyboard:

    @staticmethod
    def press(code):
        if ok:
            driver.key_down(code)

    @staticmethod
    def release(code):
        if ok:
            driver.key_up(code)

    @staticmethod
    def click(code):
        """
        :param code: 'a'-'z':A键-Z键, '0'-'9':0-9, 其他的没猜出来
        :return:
        """
        if ok:
            driver.key_down(code)
            driver.key_up(code)
