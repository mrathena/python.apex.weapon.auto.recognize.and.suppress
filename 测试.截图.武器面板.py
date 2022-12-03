import time

import pynput
import cv2
import winsound

from toolkit import Capturer

instance = Capturer.getMssInstance()

def click(x, y, button, pressed):
    if not pressed:
        if pynput.mouse.Button.x2 == button:  # 侧上键
            return False
        elif pynput.mouse.Button.right == button:
            region = (2885, 1272, 487, 139)
            img = Capturer.grab(instance, region)
            cv2.line(img, (0, 101), (500, 101), (255, 255, 255), 1)
            cv2.line(img, (66, 0), (66, 200), (255, 255, 255), 1)
            cv2.imwrite(f'{time.time_ns()}.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
            winsound.Beep(800, 200)


listener = pynput.mouse.Listener(on_click=click)
listener.start()
listener.join()
