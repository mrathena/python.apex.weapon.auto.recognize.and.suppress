import time

import pynput  # conda install pynput

import toolkit

ExitFlag = False


def down(x, y, button, pressed):
    global ExitFlag
    if ExitFlag:
        print(ExitFlag)
        return False  # 结束监听线程
    if pressed:  # 按下
        if pynput.mouse.Button.right == button:
            t1 = time.perf_counter_ns()
            toolkit.Game.detect()
            t = (time.perf_counter_ns() - t1) // 1000000
            print(t)


mouseListener = pynput.mouse.Listener(on_click=down)
mouseListener.start()


def release(key):
    if key == pynput.keyboard.Key.end:
        print('end')
        global ExitFlag
        ExitFlag = True
        return False
    if key == pynput.keyboard.KeyCode.from_char('1'):
        toolkit.Game.detect()
    elif key == pynput.keyboard.KeyCode.from_char('2'):
        toolkit.Game.detect()
    elif key == pynput.keyboard.KeyCode.from_char('3'):
        toolkit.Game.detect()
    elif key == pynput.keyboard.KeyCode.from_char('e'):
        toolkit.Game.detect()
    elif key == pynput.keyboard.KeyCode.from_char('v'):
        toolkit.Game.detect()


keyboardListener = pynput.keyboard.Listener(on_release=release)
keyboardListener.start()
keyboardListener.join()
