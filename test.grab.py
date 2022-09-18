import cv2  # conda install cv2
import numpy as np
import pynput  # conda install pynput

from configuration import ver
from toolkit import Monitor


def onClick(x, y, button, pressed):
    if not pressed:
        if pynput.mouse.Button.x1 == button:
            w, h = Monitor.Resolution.display()
            print(ver)
            print(f'{w}:{h}')
            print(Monitor.Resolution.virtual())
            print(ver[f'{w}:{h}'])
            # print(ver[f'{w}:{h}'][ver.grab][ver.arms1])
            # img = Monitor.grab(ver[f'{w}:{h}'][ver.grab][ver.arms1])
            # img = np.array(img)
            # img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            # cv2.imshow('', img)
            # cv2.waitKey(0)


mouseListener = pynput.mouse.Listener(on_click=onClick)
mouseListener.start()
mouseListener.join()
