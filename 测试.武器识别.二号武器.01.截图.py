import time
import pynput
import winsound
import mss

from toolkit import Capturer

instance = Capturer.mss()


def click(x, y, button, pressed):
    if not pressed:
        if pynput.mouse.Button.x2 == button:  # 侧上键
            return False
        elif pynput.mouse.Button.right == button:
            region = (3145, 1379, 163, 25)
            img = Capturer.grab(instance, region, convert=False)
            mss.tools.to_png(img.rgb, img.size, output=rf'image/3440.1440/two/{time.time_ns()}.png')
            winsound.Beep(800, 200)


listener = pynput.mouse.Listener(on_click=click)
listener.start()
listener.join()
