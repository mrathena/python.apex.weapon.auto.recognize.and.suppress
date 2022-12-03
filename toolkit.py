import time
import cv2
import mss
import numpy as np
from win32api import GetSystemMetrics
from win32gui import GetDesktopWindow, GetWindowDC, DeleteObject, GetWindowText, GetForegroundWindow, GetDC, ReleaseDC, GetPixel
from win32con import SRCCOPY, SM_CXSCREEN, SM_CYSCREEN
from win32ui import CreateDCFromHandle, CreateBitmap


class Capturer:

    @staticmethod
    def grabWithWin(region):
        """
        region: tuple, (left, top, width, height)
        conda install pywin32, 用 pip 装的一直无法导入 win32ui 模块, 找遍各种办法都没用, 用 conda 装的一次成功
        """
        left, top, width, height = region
        hWin = GetDesktopWindow()
        hWinDC = GetWindowDC(hWin)
        srcDC = CreateDCFromHandle(hWinDC)
        memDC = srcDC.CreateCompatibleDC()
        bmp = CreateBitmap()
        bmp.CreateCompatibleBitmap(srcDC, width, height)
        memDC.SelectObject(bmp)
        memDC.BitBlt((0, 0), (width, height), srcDC, (left, top), SRCCOPY)
        array = bmp.GetBitmapBits(True)
        DeleteObject(bmp.GetHandle())
        memDC.DeleteDC()
        srcDC.DeleteDC()
        ReleaseDC(hWin, hWinDC)
        img = np.frombuffer(array, dtype='uint8')
        img.shape = (height, width, 4)
        return img

    @staticmethod
    def getMssInstance():
        return mss.mss()

    @staticmethod
    def grabWithMss(instance, region):
        """
        region: tuple, (left, top, width, height)
        pip install mss
        """
        left, top, width, height = region
        return instance.grab(monitor={'left': left, 'top': top, 'width': width, 'height': height})

    @staticmethod
    def grab(win=False, mss=False, instance=None, region=None, convert=False):
        """
        win:
            region: tuple, (left, top, width, height)
        mss:
            instance: mss instance
            region: tuple, (left, top, width, height)
        convert: 是否转换为 opencv 需要的 numpy BGR 格式, 转换结果可直接用于 opencv
        """
        # 补全范围
        if not region:
            w, h = Monitor.resolution()
            region = 0, 0, w, h
        # 范围截图
        if win:
            img = Capturer.grabWithWin(region)
        elif mss:
            img = Capturer.grabWithMss(instance, region)
        else:
            win = True
            img = Capturer.grabWithWin(region)
        # 图片转换
        if convert:
            if win:
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            elif mss:
                img = cv2.cvtColor(np.array(img), cv2.COLOR_BGRA2BGR)
        return img


class Monitor:

    @staticmethod
    def resolution():
        """
        显示分辨率
        """
        w = GetSystemMetrics(SM_CXSCREEN)
        h = GetSystemMetrics(SM_CYSCREEN)
        return w, h

    @staticmethod
    def pixel(x, y):
        """
        效率很低且不稳定, 单点检测都要耗时1-10ms
        获取颜色, COLORREF 格式, 0x00FFFFFF
        结果是int,
        可以通过 print(hex(color)) 查看十六进制值
        可以通过 print(color == 0x00FFFFFF) 进行颜色判断
        """
        hdc = GetDC(None)
        color = GetPixel(hdc, x, y)
        ReleaseDC(None, hdc)  # 一定要释放DC, 不然随着该函数调用次数增加会越来越卡, 表现就是不调用该函数, 系统会每两秒卡一下, 调用次数越多, 卡的程度越厉害
        return color


class Timer:

    @staticmethod
    def cost(interval):
        """
        转换耗时, 输入纳秒间距, 转换为合适的单位
        """
        if interval < 1000:
            return f'{interval}ns'
        elif interval < 1_000_000:
            return f'{round(interval / 1000, 3)}us'
        elif interval < 1_000_000_000:
            return f'{round(interval / 1_000_000, 3)}ms'
        else:
            return f'{round(interval / 1_000_000_000, 3)}s'


import cfg

class Apex:
    """
    游戏工具
    """

    @staticmethod
    def key():
        w, h = Monitor.resolution()
        return f'{w}:{h}'

    @staticmethod
    def game():
        """
        是否游戏窗体在最前
        """
        return 'Apex Legends' in GetWindowText(GetForegroundWindow())

    @staticmethod
    def play():
        """
        是否正在玩
        """
        # 是在游戏中, 再判断下是否有血条和生存物品包
        data = cfg.detect.get(Apex.key()).get(cfg.play)
        for item in data:
            x, y = item.get(cfg.point)
            if Monitor.pixel(x, y) != item.get(cfg.color):
                return False
        return True

    @staticmethod
    def weapon():
        """
        先识别激活的武器 None:未持有武器, 1:1号武器, 2:2号武器
        再识别武器名称
        """
        data = cfg.detect.get(Apex.key()).get(cfg.name)
        x, y = data.get(cfg.point)
        color = Monitor.pixel(x, y)
        if data.get(cfg.color) == color:  # 灰色, 无武器
            return None
        else:  # 非灰色, 判断是1还是2
            index = cfg.one if color == Monitor.pixel(x, y + 1) else cfg.two
            data = data.get(index)  # 取到配置数据
            region = data.get(cfg.region)  # 取到截图范围
            img = Capturer.grab(win=True, region=region, convert=True)  # 截图
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 灰度化
            height, width = img.shape
            counter = 0  # 统计纯白色点个数
            for row in range(0, height):
                for col in range(0, width):
                    if 255 == img[row, col]:
                        counter += 1
            name = data.get(counter)  # 取到武器名称
            if not name:  # 武器识别失败
                return None
            if isinstance(name, list):  # 如果白点数有冲突
                for item in name:  # 遍历冲突的武器名称, 拿到二级验证点继续判断
                    point = data.get(item)
                    if 255 == img[point]:
                        return item
            return name


    @staticmethod
    def mode():
        """
        武器模式
        :return:  1:全自动, 2:半自动, None:其他
        """
        data = cfg.detect.get(Apex.key()).get(cfg.mode)
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
    def empty():
        """
        是否空弹夹
        """
        data = cfg.detect.get(Apex.key()).get(cfg.empty)
        color = data.get(cfg.color)
        x, y = data.get('1')
        if color == Monitor.pixel(x, y):
            return False
        x, y = data.get('2')
        return color == Monitor.pixel(x, y)

    @staticmethod
    def attachment(config, name):
        """
        配件检测
        传入配置和名称, 判断是否需要做对应配件检测, 需要的话再判断是否有对应配件
        """
        data = config
        if name not in data.keys():
            return False
        color = data.get(cfg.color)
        x, y = data.get(name)
        return color == Monitor.pixel(x, y)

    @staticmethod
    def turbo(name):
        """
        传入名称, 判断是否需要做涡轮检测, 需要的话再判断是否有涡轮
        """
        data = cfg.detect.get(Apex.key()).get(cfg.turbo)
        return Apex.attachment(data, name)

    @staticmethod
    def trigger(name):
        """
        传入名称, 判断是否需要做双发扳机检测, 需要的话再判断是否有双发扳机
        """
        data = cfg.detect.get(Apex.key()).get(cfg.trigger)
        return Apex.attachment(data, name)

    @staticmethod
    def thermite(name):
        """
        传入名称, 判断是否需要做铝热剂检测, 需要的话再判断是否有铝热剂
        """
        data = cfg.detect.get(Apex.key()).get(cfg.thermite)
        return Apex.attachment(data, name)

    @staticmethod
    def detect(data):
        """
        决策是否需要压枪, 向信号量写数据
        """
        t1 = time.perf_counter_ns()
        if data.get(cfg.switch) is False:
            data[cfg.weapon] = None  # 清空武器数据
            t2 = time.perf_counter_ns()
            print(f'耗时: {Timer.cost(t2 - t1)}, 开关已关闭')
            return
        if Apex.play() is False:
            data[cfg.weapon] = None
            t2 = time.perf_counter_ns()
            print(f'耗时: {Timer.cost(t2 - t1)}, 不在对局中')
            return
        name = Apex.weapon()
        if not name or isinstance(name, list):
            data[cfg.weapon] = None
            t2 = time.perf_counter_ns()
            print(f'耗时: {Timer.cost(t2 - t1)}, 没有武器/识别武器失败')
            return
        # if Game.mode() is None:
        #     data[cfg.restrain] = None
        #     t2 = time.perf_counter_ns()
        #     print(f'耗时: {Timer.cost(t2 - t1)}, 不是自动/半自动模式')
        #     return
        # 检测通过, 额外判断涡轮与双发扳机与火力全开(暴走)
        turbo = Apex.turbo(name)
        trigger = Apex.trigger(name)
        thermite = Apex.thermite(name)
        # 拿对应压枪参数
        if turbo:
            name += ' (涡轮)'
        if trigger:
            name += ' (双发扳机)'
        if thermite:
            name += ' (火力全开)'
        data[cfg.weapon] = cfg.weapons.get(name)  # 记录当前武器压制参数
        t2 = time.perf_counter_ns()
        print(f'{name}, {Timer.cost(t2 - t1)}')
