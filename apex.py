import ctypes
import multiprocessing
import time
import winsound
from multiprocessing import Process

import pynput

from toolkit import Apex

ads = 'ads'
end = 'end'
fire = 'fire'
count = 'count'
switch = 'switch'
detect = 'detect'
weapon = 'weapon'
timestamp = 'timestamp'
init = {
    end: False,  # 退出标记, End 键按下后改为 True, 其他进程线程在感知到变更后结束自身
    switch: True,  # 检测和压枪开关, 侧上键
    detect: 0,  # 检测信号, 非0触发主循环检测, 检测完置0
    weapon: None,  # 压枪参数
    fire: False,  # 开火状态
    timestamp: None,  # 按下左键开火时的时间戳
    ads: 2,  # 基准倍数
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
            if data.get(weapon) is not None:
                for item in data.get(weapon):
                    if not data.get(fire):  # 停止开火
                        break
                    t1 = time.perf_counter_ns()
                    if not Apex.game():  # 不在游戏中
                        break
                    if not Apex.armed():  # 未持有武器
                        break
                    if Apex.empty():  # 弹夹为空
                        break
                    t2 = time.perf_counter_ns()
                    # operation: # 1:移动 2:按下
                    operation = item[0]
                    if operation == 1:
                        temp, x, y, delay = item
                        move(x, y)
                        delay = (delay - (t2 - t1) // 1000 // 1000) / 1000
                        if delay > 0:
                            time.sleep(delay)
                    elif operation == 2:
                        temp, code, delay = item
                        # click(code)
                        delay = (delay - (t2 - t1) // 1000 // 1000) / 1000
                        if delay > 0:
                            time.sleep(delay)


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
