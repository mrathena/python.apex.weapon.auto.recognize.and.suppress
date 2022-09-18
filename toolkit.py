import mss  # pip install mss
import ctypes
import time

from ctypes import CDLL

import cfg
from cfg import config

# 全局 dll
user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32
hdc = user32.GetDC(None)

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
                ox, oy = user32.GetCursorPos()
                mx = x - ox
                my = y - oy
            driver.moveR(mx, my, True)

    @staticmethod
    def moveHumanoid(x, y, absolute=False):
        """
        仿真移动
        """
        if ok:
            ox, oy = user32.GetCursorPos()  # 原鼠标位置
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
        键盘按键函数中，传入的参数采用的是键盘按键对应的键码
        :param code: 'a'-'z':A键-Z键, '0'-'9':0-9, 其他的没猜出来
        :return:
        """
        if ok:
            driver.key_down(code)
            driver.key_up(code)


class Monitor:
    """
    显示器
    """
    sct = mss.mss()

    @staticmethod
    def grab(region):
        """
        region: tuple, (left, top, width, height)
        pip install mss
        """
        left, top, width, height = region
        return Monitor.sct.grab(monitor={'left': left, 'top': top, 'width': width, 'height': height})

    @staticmethod
    def pixel(x, y):
        """
        效率很低且不稳定, 单点检测都要耗时1-10ms
        获取颜色, COLORREF 格式, 0x00FFFFFF
        结果是int,
        可以通过 print(hex(color)) 查看十六进制值
        可以通过 print(color == 0x00FFFFFF) 进行颜色判断
        """
        # hdc = user32.GetDC(None)
        return gdi32.GetPixel(hdc, x, y)

    class Resolution:
        """
        分辨率
        """

        @staticmethod
        def display():
            """
            显示分辨率
            """
            w = user32.GetSystemMetrics(0)
            h = user32.GetSystemMetrics(1)
            return w, h

        @staticmethod
        def virtual():
            """
            多屏幕组合的虚拟显示器分辨率
            """
            w = user32.GetSystemMetrics(78)
            h = user32.GetSystemMetrics(79)
            return w, h

        @staticmethod
        def physical():
            """
            物理分辨率
            """
            # hdc = user32.GetDC(None)
            w = gdi32.GetDeviceCaps(hdc, 118)
            h = gdi32.GetDeviceCaps(hdc, 117)
            return w, h


class Game:
    """
    游戏工具
    """

    @staticmethod
    def inGame():
        t1 = time.perf_counter_ns()
        w, h = Monitor.Resolution.display()
        t2 = time.perf_counter_ns()
        lst = config.get(f'{w}:{h}').get(cfg.cheat).get(cfg.detect).get(cfg.game)
        t3 = time.perf_counter_ns()
        for item in lst:
            x, y = item.get(cfg.point)
            if Monitor.pixel(x, y) != item.get(cfg.color):
                return False
        print(t2 - t1)
        print(t3 - t2)
        print(time.perf_counter_ns() - t3)
        return True
