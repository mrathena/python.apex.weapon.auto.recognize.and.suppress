import multiprocessing
import time
from multiprocessing import Process

import pynput  # conda install pynput

import toolkit


end = 'end'
fire = 'fire'
shake = 'shake'
switch = 'switch'
init = {
    switch: True,  # 压枪开关
    end: False,  # 退出标记, End 键按下后改为 True, 其他进程线程在感知到变更后结束自身
    shake: None,  # 抖枪参数
    fire: False,  # 开火状态
}


def listener(data):

    def down(x, y, button, pressed):
        nonlocal data
        if data.get(end):
            return False  # 结束监听线程
        if button == pynput.mouse.Button.right:
            if pressed:
                toolkit.Game.detect(data)
        elif button == pynput.mouse.Button.left:
            data[fire] = pressed

    mouse = pynput.mouse.Listener(on_click=down)
    mouse.start()

    def release(key):
        nonlocal data
        if key == pynput.keyboard.Key.end:
            # 结束程序
            data[end] = True
            return False
        elif key == pynput.keyboard.Key.home:
            # 压枪开关
            pass
        elif key == pynput.keyboard.Key.tab:
            toolkit.Game.detect(data)
        elif key == pynput.keyboard.KeyCode.from_char('1'):
            toolkit.Game.detect(data)
        elif key == pynput.keyboard.KeyCode.from_char('2'):
            toolkit.Game.detect(data)
        elif key == pynput.keyboard.KeyCode.from_char('3'):
            toolkit.Game.detect(data)
        elif key == pynput.keyboard.KeyCode.from_char('e'):
            toolkit.Game.detect(data)
        elif key == pynput.keyboard.KeyCode.from_char('v'):
            toolkit.Game.detect(data)

    keyboard = pynput.keyboard.Listener(on_release=release)
    keyboard.start()
    keyboard.join()  # 卡住进程 listener, 当线程 keyboard 结束后, 进程 listener 才能结束


def suppress(data):
    while True:
        if data[end]:
            break
        if data[switch] is False:
            continue
        if data[fire] & (data[shake] is not None):
            while True:
                if not data[fire]:
                    break
                toolkit.Mouse.move(4, 0)
                time.sleep(0.01)
                toolkit.Mouse.move(-4, 0)
                time.sleep(0.01)
                toolkit.Mouse.move(0, 5)
                time.sleep(0.01)


if __name__ == '__main__':
    multiprocessing.freeze_support()  # windows 平台使用 multiprocessing 必须在 main 中第一行写这个
    manager = multiprocessing.Manager()
    data = manager.dict()  # 创建进程安全的共享变量
    data.update(init)  # 将初始数据导入到共享变量
    # 将键鼠监听和压枪放到单独进程中跑
    p1 = Process(target=listener, args=(data,))  # 监听进程
    p2 = Process(target=suppress, args=(data,))  # 压枪进程
    p1.start()
    p2.start()
    p1.join()  # 卡住主进程, 当进程 listener 结束后, 主进程才会结束
