import ctypes
import multiprocessing
import time
import winsound
from multiprocessing import Process

import pynput

from toolkit import Timer, Apex

ads = 'ads'
end = 'end'
fire = 'fire'
count = 'count'
switch = 'switch'
detect = 'detect'
weapon = 'weapon'
interval = 'interval'
category = 'category'
vertical = 'vertical'
timestamp = 'timestamp'
horizontal = 'horizontal'
init = {
    end: False,  # 退出标记, End 键按下后改为 True, 其他进程线程在感知到变更后结束自身
    switch: True,  # 检测和压枪开关, 侧上键
    detect: 0,  # 检测信号, 非0触发主循环检测, 检测完置0
    weapon: None,  # 武器数据
    fire: False,  # 开火状态
    timestamp: None,  # 按下左键开火时的时间戳
    ads: 1.5,  # 基准倍数
}


def mouse(data):

    def click(x, y, button, pressed):
        if Apex.game():
            if button == pynput.mouse.Button.x2:  # 侧上键
                if pressed:
                    data[switch] = not data.get(switch)
                    winsound.Beep(800 if data[switch] else 400, 200)
            if button == pynput.mouse.Button.right:
                if pressed:
                    data[detect] = 1
            elif button == pynput.mouse.Button.left:
                data[fire] = pressed
                if pressed:
                    data[timestamp] = time.time_ns()

    with pynput.mouse.Listener(on_click=click) as m:
        m.join()


def keyboard(data):

    def release(key):
        if key == pynput.keyboard.Key.end:
            winsound.Beep(400, 200)
            data[end] = True
            return False  # 结束监听线程
        if Apex.game():
            if key == pynput.keyboard.Key.home:
                data[switch] = not data.get(switch)
                winsound.Beep(800 if data[switch] else 400, 200)
            elif key == pynput.keyboard.Key.esc:
                data[detect] = 1
            elif key == pynput.keyboard.Key.tab:
                data[detect] = 1
            elif key == pynput.keyboard.Key.alt_l:
                data[detect] = 1
            elif key == pynput.keyboard.KeyCode.from_char('1'):
                data[detect] = 1
            elif key == pynput.keyboard.KeyCode.from_char('2'):
                data[detect] = 1
            elif key == pynput.keyboard.KeyCode.from_char('3'):
                data[detect] = 1
            elif key == pynput.keyboard.KeyCode.from_char('e'):
                data[detect] = 1
            elif key == pynput.keyboard.KeyCode.from_char('r'):
                data[detect] = 1
            elif key == pynput.keyboard.KeyCode.from_char('v'):
                data[detect] = 1

    with pynput.keyboard.Listener(on_release=release) as k:
        k.join()


def suppress(data):

    try:
        driver = ctypes.CDLL('logitech.driver.dll')
        # 该驱动每个进程可打开一个实例
        ok = driver.device_open() == 1
        if not ok:
            print('Error, GHUB or LGS driver not found')
    except FileNotFoundError:
        print('Error, DLL file not found')

    def move(x, y):
        if ok:
            driver.moveR(x, y, True)

    winsound.Beep(800, 200)

    while True:

        if data.get(end):
            break
        if not Apex.game():  # 如果不在游戏中
            continue
        if not data.get(switch):  # 如果开关关闭
            continue
        if data[detect] != 0:  # 触发武器检测
            data[detect] = 0
            time.sleep(0.2)  # 防止UI还没有改变
            Apex.detect(data)
        if data.get(fire):
            gun = data.get(weapon)  # 获取当前武器数据
            if not gun:  # 如果没有数据则不压枪
                print('武器无需压枪')
                continue
            clazz = gun.get(category)
            if not clazz:  # 数据没有 category 字段
                print('数据不正确')
                continue
            if Apex.empty():  # 弹夹为空
                print('武器弹夹空')
                continue
            if not Apex.armed():  # 未持有武器
                print('未持有武器')
                continue
            # print('----------')
            # 数据分种类
            # 301 这种射击间隔稳定的枪
            # 哈沃克 这种初始需要预热然后射击间隔稳定的枪(装备涡轮后变成301这种)
            # 专注 这种初始几枪射击间隔逐渐缩小后续保持稳定的枪(装备涡轮后缩小前几枪的射击间隔)
            if clazz == 1:
                cost = time.time_ns() - data[timestamp]  # 开火时长
                base = gun[interval] * 1_000_000  # 基准间隔时间转纳秒
                i = cost // base  # 本回合的压枪力度数值索引
                v = int(data[ads] * gun[vertical][i])  # 垂直
                h = int(data[ads] * gun[horizontal][i])  # 水平
                print(f'开火时长:{Timer.cost(cost)}, {i + 2}, 压制力度:{v}')
                cost = time.time_ns() - data[timestamp]
                left = base - cost % base  # 本回合剩余时间纳秒
                if v == 0:
                    begin = time.perf_counter_ns()
                    while time.perf_counter_ns() - begin < left:
                        pass
                else:
                    mean = left / v  # 平缓压枪每个实际力度的延时
                    for i in range(0, v):
                        begin = time.perf_counter_ns()
                        while time.perf_counter_ns() - begin < mean:
                            pass
                        move(0, 1)


if __name__ == '__main__':
    multiprocessing.freeze_support()  # windows 平台使用 multiprocessing 必须在 main 中第一行写这个
    manager = multiprocessing.Manager()
    data = manager.dict()  # 创建进程安全的共享变量
    data.update(init)  # 将初始数据导入到共享变量
    # 将键鼠监听和压枪放到单独进程中跑
    pm = Process(target=mouse, args=(data,))
    pk = Process(target=keyboard, args=(data,))
    ps = Process(target=suppress, args=(data,))
    pm.start()
    pk.start()
    ps.start()
    pk.join()  # 不写 join 的话, 使用 dict 的地方就会报错 conn = self._tls.connection, AttributeError: 'ForkAwareLocal' object has no attribute 'connection'
    pm.terminate()  # 鼠标进程无法主动监听到终止信号, 所以需强制结束
