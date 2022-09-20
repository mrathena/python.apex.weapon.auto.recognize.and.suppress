import time

import mss  # pip install mss
import ctypes

from ctypes import CDLL

import cfg
from cfg import detect, weapon

# 全局 dll
user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32

try:
    driver = CDLL(r'mouse.device.lgs.dll')  # 在Python的string前面加上‘r’, 是为了告诉编译器这个string是个raw string(原始字符串),不要转义backslash(反斜杠) '\'
    ok = driver.device_open() == 1
    if not ok:
        print('初始化失败, 未安装lgs/ghub驱动')
except FileNotFoundError:
    print('初始化失败, 缺少文件')


class Mouse:

    @staticmethod
    def point():
        return user32.GetCursorPos()

    @staticmethod
    def move(x, y, absolute=False):
        if ok:
            if (x == 0) & (y == 0):
                return
            mx, my = x, y
            if absolute:
                ox, oy = user32.GetCursorPos()
                mx = x - ox
                my = y - oy
            driver.moveR(mx, my, True)

    @staticmethod
    def moveHumanoid(x, y, absolute=False):
        """
        仿真移动(还没做好)
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
        hdc = user32.GetDC(None)
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
            hdc = user32.GetDC(None)
            w = gdi32.GetDeviceCaps(hdc, 118)
            h = gdi32.GetDeviceCaps(hdc, 117)
            return w, h


class Game:
    """
    游戏工具
    """

    @staticmethod
    def game():
        """
        是否游戏窗体在最前
        """
        # 先判断是否是游戏窗口
        hwnd = user32.GetForegroundWindow()
        length = user32.GetWindowTextLengthW(hwnd)
        buffer = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buffer, length + 1)
        if 'Apex Legends' != buffer.value:
            return False
        return True

    @staticmethod
    def play():
        """
        是否正在玩
        """
        # 是在游戏中, 再判断下是否有血条和生存物品包
        w, h = Monitor.Resolution.display()
        data = detect.get(f'{w}:{h}').get(cfg.game)
        for item in data:
            x, y = item.get(cfg.point)
            if Monitor.pixel(x, y) != item.get(cfg.color):
                return False
        return True

    @staticmethod
    def index():
        """
        武器索引和子弹类型索引
        :return: 武器位索引, 1:1号位, 2:2号位, None:无武器, 拳头(这个暂时无法判断)
                 子弹类型索引, 1:轻型, 2:重型, 3:能量, 4:狙击, 5:霰弹, 6:空投, None:无武器
        """
        w, h = Monitor.Resolution.display()
        data = detect.get(f'{w}:{h}').get(cfg.pack)
        x, y = data.get(cfg.point)
        color = Monitor.pixel(x, y)
        if data.get(cfg.color) == color:
            return None, None
        else:
            bullet = data.get(hex(color))
            return (1, bullet) if color == Monitor.pixel(x, y + 1) else (2, bullet)

    @staticmethod
    def weapon(index, bullet):
        """
        通过武器位和子弹类型识别武器, 参考:config.detect.name
        :param index: 武器位, 1:1号位, 2:2号位
        :param bullet: 子弹类型, 1:轻型, 2:重型, 3:能量, 4:狙击, 5:霰弹, 6:空投
        :return:
        """
        w, h = Monitor.Resolution.display()
        data = detect.get(f'{w}:{h}').get(cfg.name)
        color = data.get(cfg.color)
        if index == 1:
            lst = data.get(str(index)).get(str(bullet))
            for i in range(len(lst)):
                x, y = lst[i]
                if color == Monitor.pixel(x, y):
                    return i + 1
        elif index == 2:
            differ = data.get(str(index)).get(cfg.differ)
            lst = data.get(str(1)).get(str(bullet))
            for i in range(len(lst)):
                x, y = lst[i]
                if color == Monitor.pixel(x + differ, y):
                    return i + 1
        return None

    @staticmethod
    def mode():
        """
        武器模式
        :return:  1:全自动, 2:半自动, None:其他
        """
        w, h = Monitor.Resolution.display()
        data = detect.get(f'{w}:{h}').get(cfg.mode)
        color = data.get(cfg.color)
        x, y = data.get('1')
        if color == Monitor.pixel(x, y):
            return 1
        x, y = data.get('2')
        if color == Monitor.pixel(x, y):
            return 2
        return None

    @staticmethod
    def turbo(bullet, arms):
        w, h = Monitor.Resolution.display()
        data = detect.get(f'{w}:{h}').get(cfg.turbo)
        color = data.get(cfg.color)
        data = data.get(str(bullet))
        if data is None:
            return False
        data = data.get(str(arms))
        if data is None:
            return False
        x, y = data
        return color == Monitor.pixel(x, y)

    @staticmethod
    def detect(data):
        """
        决策是否需要压枪, 向信号量写数据
        """
        if data.get(cfg.switch) is False:
            print('开关已关闭')
            return
        t1 = time.perf_counter_ns()
        if Game.game() is False:
            print('不在游戏中')
            data[cfg.shake] = None
            return
        if Game.play() is False:
            print('不在游戏中')
            data[cfg.shake] = None
            return
        index, bullet = Game.index()
        if (index is None) | (bullet is None):
            print('没有武器')
            data[cfg.shake] = None
            return
        if Game.mode() is None:
            print('不是自动/半自动武器')
            data[cfg.shake] = None
            return
        arms = Game.weapon(index, bullet)
        if arms is None:
            print('识别武器失败')
            data[cfg.shake] = None
            return
        # 检测通过, 需要压枪
        gun = weapon.get(str(bullet)).get(str(arms))
        data[cfg.shake] = gun.get(cfg.shake)  # 记录当前武器抖动参数
        data[cfg.restrain] = gun.get(cfg.restrain)  # 记录当前武器压制参数
        # 检测涡轮
        data[cfg.turbo] = Game.turbo(bullet, arms)
        t2 = time.perf_counter_ns()
        print(f'耗时:{t2-t1}ns, 约{(t2-t1)//1000000}ms, {gun.get(cfg.name)}{"(涡轮)" if data.get(cfg.turbo) else ""}')

