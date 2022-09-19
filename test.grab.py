import datetime
import time

import cv2  # conda install cv2
import numpy as np
import pynput  # conda install pynput

from toolkit import Monitor, Game
import cfg
from cfg import detect


def onClick(x, y, button, pressed):
    if not pressed:
        if pynput.mouse.Button.x2 == button:
            return False
        if pynput.mouse.Button.x1 == button:
            # img = Monitor.grab([2944, 1377, 175, 30])
            # img = np.array(img)
            # img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            # now = datetime.datetime.now()
            # cv2.imwrite(f'C:\\Users\\mrathena\\Desktop\\{now.strftime("%Y%m%d %H%M%S.png")}', img, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])

            # t1 = time.perf_counter_ns()
            # print(hex(Monitor.pixel(2900, 1372)))
            # print(Game.game())
            # print(Game.index())
            # print(Game.mode())
            # print(Game.bullet())
            index = Game.index()
            bullet = Game.bullet()
            print(Game.name(index, bullet))
            # t2 = time.perf_counter_ns()
            # print((t2 - t1)//1000000)




mouseListener = pynput.mouse.Listener(on_click=onClick)
mouseListener.start()
mouseListener.join()


