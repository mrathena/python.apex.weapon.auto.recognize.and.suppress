import multiprocessing
import time
from multiprocessing import Process

import pynput  # conda install pynput

from toolkit import Mouse, Game

end = 'end'
fire = 'fire'
shake = 'shake'
speed = 'speed'
count = 'count'
switch = 'switch'
restart = 'restart'
restrain = 'restrain'
strength = 'strength'
init = {
    end: False,  # 退出标记, End 键按下后改为 True, 其他进程线程在感知到变更后结束自身
    switch: True,  # 检测和压枪开关
    fire: False,  # 开火状态
    shake: None,  # 抖枪参数
    restrain: None,  # 压枪参数
}


def listener(data):

    def down(x, y, button, pressed):
        if data.get(end):
            return False  # 结束监听线程
        if button == pynput.mouse.Button.right:
            if pressed:
                Game.detect(data)
        elif button == pynput.mouse.Button.left:
            data[fire] = pressed

    mouse = pynput.mouse.Listener(on_click=down)
    mouse.start()

    def release(key):
        if key == pynput.keyboard.Key.end:
            # 结束程序
            data[end] = True
            return False
        elif key == pynput.keyboard.Key.home:
            # 压枪开关
            data[switch] = not data.get(switch)
        elif key == pynput.keyboard.Key.esc:
            Game.detect(data)
        elif key == pynput.keyboard.Key.tab:
            Game.detect(data)
        elif key == pynput.keyboard.Key.alt_l:
            Game.detect(data)
        elif key == pynput.keyboard.KeyCode.from_char('1'):
            Game.detect(data)
        elif key == pynput.keyboard.KeyCode.from_char('2'):
            Game.detect(data)
        elif key == pynput.keyboard.KeyCode.from_char('3'):
            Game.detect(data)
        elif key == pynput.keyboard.KeyCode.from_char('e'):
            Game.detect(data)
        elif key == pynput.keyboard.KeyCode.from_char('r'):
            Game.detect(data)
        elif key == pynput.keyboard.KeyCode.from_char('v'):
            Game.detect(data)

    keyboard = pynput.keyboard.Listener(on_release=release)
    keyboard.start()
    keyboard.join()  # 卡住监听进程, 当键盘线程结束后, 监听进程才能结束


def suppress(data):
    while True:
        if data.get(end):
            break
        if data.get(restart):
            break
        if data.get(switch) is False:
            continue
        if data.get(fire):
            if data.get(restrain) is not None:
                for item in data.get(restrain):
                    if not data.get(fire):  # 停止开火
                        break
                    t1 = time.perf_counter_ns()
                    if not Game.game():  # 不在游戏中
                        break
                    if not Game.armed():  # 未持有武器
                        break
                    if Game.empty():  # 弹夹为空
                        break
                    t2 = time.perf_counter_ns()
                    # operation: # 1:移动 2:按下
                    operation = item[0]
                    if operation == 1:
                        temp, x, y, delay = item
                        Mouse.move(x, y)
                        time.sleep((delay - (t2 - t1) // 1000 // 1000) / 1000)
                    elif operation == 2:
                        temp, code, delay = item
                        Mouse.click(code)
                        time.sleep((delay - (t2 - t1) // 1000 // 1000) / 1000)
            elif data.get(shake) is not None:
                total = 0  # 总计时 ms
                delay = 1  # 延迟 ms
                pixel = 4  # 抖动像素
                while True:
                    if not data[fire]:  # 停止开火
                        break
                    if not Game.game():  # 不在游戏中
                        break
                    if not Game.armed():  # 未持有武器
                        break
                    if Game.empty():  # 弹夹为空
                        break
                    t = time.perf_counter_ns()
                    if total < data[shake][speed] * data[shake][count]:
                        Mouse.move(0, data[shake][strength])
                        time.sleep(delay / 1000)
                        total += delay
                    else:
                        Mouse.move(0, 1)
                        time.sleep(delay / 1000)
                        total += delay
                    # 抖枪
                    Mouse.move(pixel, 0)
                    time.sleep(delay / 1000)
                    total += delay
                    Mouse.move(-pixel, 0)
                    time.sleep(delay / 1000)
                    total += delay
                    total += (time.perf_counter_ns() - t) // 1000 // 1000


if __name__ == '__main__':
    multiprocessing.freeze_support()  # windows 平台使用 multiprocessing 必须在 main 中第一行写这个
    manager = multiprocessing.Manager()
    data = manager.dict()  # 创建进程安全的共享变量
    data.update(init)  # 将初始数据导入到共享变量
    # 将键鼠监听和压枪放到单独进程中跑
    p1 = Process(daemon=True, target=listener, args=(data,))  # 监听进程
    p2 = Process(target=suppress, args=(data,))  # 压枪进程
    p1.start()
    p2.start()
    p1.join()  # 卡住主进程, 当进程 listener 结束后, 主进程才会结束
