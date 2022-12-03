import ctypes
import multiprocessing
import time
from multiprocessing import Process

import pynput
import winsound

end = 'end'
fire = 'fire'
init = {
    end: False,
    fire: False,
}


def mouse(data):

    def click(x, y, button, pressed):
        if button == pynput.mouse.Button.x2:  # 侧上键
            winsound.Beep(400, 200)
            data[end] = True
            return False
        elif button == pynput.mouse.Button.left:  # 左键开火
            data[fire] = pressed

    with pynput.mouse.Listener(on_click=click) as m:
        m.join()


def test(data):

    from toolkit import Apex

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

    warmup = 0  # 预热时间
    interval = 59  # 首先假设一个武器射击间隔, 毫秒
    count = 27  # 间隔个数, 如果弹夹有28发子弹, 则射击间隔只有27个

    while True:
        if data[end]:
            break
        if not Apex.game():
            continue
        if data[fire]:  # 检测到按下左键时, 开始休眠, 醒来时立刻大幅度移动鼠标, 如果移动瞬间刚好子弹打完, 说明射击间隔比较准, 否则继续调整射击间隔并测试
            total = warmup * 1_000_000 + interval * 1_000_000 * count
            begin = time.perf_counter_ns()
            while time.perf_counter_ns() - begin < total:
                pass
            move(10000, 0)
            time.sleep(1)  # 防止一轮循环结束立马重新进来


if __name__ == '__main__':
    multiprocessing.freeze_support()
    manager = multiprocessing.Manager()
    data = manager.dict()
    data.update(init)
    pm = Process(target=mouse, args=(data,))
    pt = Process(target=test, args=(data,))
    pm.start()
    pt.start()
    pt.join()
    pm.terminate()
