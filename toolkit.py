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
    def key():
        w, h = Monitor.Resolution.display()
        return f'{w}:{h}'

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
        data = detect.get(Game.key()).get(cfg.game)
        for item in data:
            x, y = item.get(cfg.point)
            if Monitor.pixel(x, y) != item.get(cfg.color):
                return False
        return True

    @staticmethod
    def index():
        """
        武器索引和子弹类型索引
        :return: 武器位索引, 1:1号位, 2:2号位, None:无武器
                 子弹类型索引, 1:轻型, 2:重型, 3:能量, 4:狙击, 5:霰弹, 6:空投, None:无武器
        """
        data = detect.get(Game.key()).get(cfg.pack)
        x, y = data.get(cfg.point)
        color = Monitor.pixel(x, y)
        if data.get(cfg.color) == color:
            return None, None
        else:
            bi = data.get(hex(color))
            return (1, bi) if color == Monitor.pixel(x, y + 1) else (2, bi)

    @staticmethod
    def weapon(pi, bi):
        """
        通过武器位和子弹类型识别武器, 参考:config.detect.name
        :param pi: 武器位, 1:1号位, 2:2号位
        :param bi: 子弹类型, 1:轻型, 2:重型, 3:能量, 4:狙击, 5:霰弹, 6:空投
        :return:
        """
        data = detect.get(Game.key()).get(cfg.name)
        color = data.get(cfg.color)
        if pi == 1:
            lst = data.get(str(pi)).get(str(bi))
            for i in range(len(lst)):
                x, y = lst[i]
                if color == Monitor.pixel(x, y):
                    return i + 1
        elif pi == 2:
            differ = data.get(str(pi)).get(cfg.differ)
            lst = data.get(str(1)).get(str(bi))
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
        data = detect.get(Game.key()).get(cfg.mode)
        color = data.get(cfg.color)
        x, y = data.get('1')
        if color == Monitor.pixel(x, y):
            return 1
        x, y = data.get('2')
        if color == Monitor.pixel(x, y):
            return 2
        return None

    @staticmethod
    def armed():
        """
        是否持有武器
        """
        return True

    @staticmethod
    def turbo(bi, wi):
        """
        判断是否有涡轮, 只有配置了检测涡轮的武器才会做取色判断
        :return: (False, None), (True, differ), 有涡轮的话, 额外返回涡轮索引偏移
        """
        data = detect.get(Game.key()).get(cfg.turbo)
        color = data.get(cfg.color)
        data = data.get(str(bi))
        if data is None:
            return False, None
        differ = data.get(cfg.differ)
        data = data.get(str(wi))
        if data is None:
            return False, None
        x, y = data
        result = color == Monitor.pixel(x, y)
        return (True, differ) if result else (False, None)

    @staticmethod
    def trigger(bi, wi):
        """
        判断是否有双发扳机, 只有配置了检测双发扳机的武器才会做取色判断
        :return: (False, None), (True, differ), 有双发扳机的话, 额外返回双发扳机索引偏移
        """
        data = detect.get(Game.key()).get(cfg.trigger)
        color = data.get(cfg.color)
        data = data.get(str(bi))
        if data is None:
            return False, None
        differ = data.get(cfg.differ)
        data = data.get(str(wi))
        if data is None:
            return False, None
        x, y = data
        result = color == Monitor.pixel(x, y)
        return (True, differ) if result else (False, None)

    @staticmethod
    def detect(data):
        """
        决策是否需要压枪, 向信号量写数据
        """
        t1 = time.perf_counter_ns()
        if data.get(cfg.switch) is False:
            t2 = time.perf_counter_ns()
            print(f'耗时: {t2 - t1}ns, 约{(t2 - t1) // 1000000}ms, 开关已关闭')
            return
        if Game.game() is False:
            data[cfg.shake] = None
            data[cfg.restrain] = None
            t2 = time.perf_counter_ns()
            print(f'耗时: {t2 - t1}ns, 约{(t2 - t1) // 1000000}ms, 不在游戏中')
            return
        if Game.play() is False:
            data[cfg.shake] = None
            data[cfg.restrain] = None
            t2 = time.perf_counter_ns()
            print(f'耗时: {t2 - t1}ns, 约{(t2 - t1) // 1000000}ms, 不在游戏中')
            return
        pi, bi = Game.index()
        if (pi is None) | (bi is None):
            data[cfg.shake] = None
            data[cfg.restrain] = None
            t2 = time.perf_counter_ns()
            print(f'耗时: {t2 - t1}ns, 约{(t2 - t1) // 1000000}ms, 没有武器')
            return
        # if Game.mode() is None:
        #     data[cfg.shake] = None
        #     data[cfg.restrain] = None
        #     t2 = time.perf_counter_ns()
        #     print(f'耗时: {t2 - t1}ns, 约{(t2 - t1) // 1000000}ms, 不是自动/半自动武器')
        #     return
        wi = Game.weapon(pi, bi)
        if wi is None:
            data[cfg.shake] = None
            data[cfg.restrain] = None
            t2 = time.perf_counter_ns()
            print(f'耗时: {t2 - t1}ns, 约{(t2 - t1) // 1000000}ms, 识别武器失败')
            return
        # 检测通过, 需要压枪
        # 检测涡轮
        result, differ = Game.turbo(bi, wi)
        if result is False:
            # 检测双发扳机
            result, differ = Game.trigger(bi, wi)
        # 拿对应参数
        gun = weapon.get(str(bi)).get(str((wi + differ) if result else wi))
        data[cfg.shake] = gun.get(cfg.shake)  # 记录当前武器抖动参数
        data[cfg.restrain] = gun.get(cfg.restrain)  # 记录当前武器压制参数
        t2 = time.perf_counter_ns()
        print(f'耗时: {t2-t1}ns, 约{(t2-t1)//1000000}ms, {gun.get(cfg.name)}')
