from toolkit import Mouse
import pynput






def onClick(x, y, button, pressed):
    if not pressed:
        if pynput.mouse.Button.x2 == button:
            Mouse.move(100, 100)


mouseListener = pynput.mouse.Listener(on_click=onClick)
mouseListener.start()
mouseListener.join()



