import time

import cv2  # conda install cv2
import numpy as np
import pynput  # conda install pynput

from toolkit import Monitor, Game
import cfg
from cfg import config


def onClick(x, y, button, pressed):
    if not pressed:
        if pynput.mouse.Button.x2 == button:
            return False
        if pynput.mouse.Button.x1 == button:
            w, h = Monitor.Resolution.display()
            # print(config.get(f'{w}:{h}').get(cfg.grab).get(cfg.arms1))
            # img = Monitor.grab(ver[f'{w}:{h}'][ver.grab][ver.arms1])
            # img = np.array(img)
            # img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            # cv2.imshow('', img)
            # cv2.waitKey(0)
            # t1 = time.perf_counter_ns()
            # print(hex(Monitor.pixel(2900, 1372)))
            # print(Game.game())
            print(Game.index())
            # t2 = time.perf_counter_ns()
            # print((t2 - t1)//1000000)




mouseListener = pynput.mouse.Listener(on_click=onClick)
mouseListener.start()
mouseListener.join()
