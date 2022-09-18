from ctypes import CDLL

try:
    gm = CDLL(r'mouse.device.ghub.dll')  # 在Python的string前面加上‘r’, 是为了告诉编译器这个string是个raw string(原始字符串),不要转义backslash(反斜杠) '\'
    ok = gm.device_open() == 1
    if not ok:
        print('未安装ghub或者lgs驱动!!!')
    else:
        print('初始化成功!')
except FileNotFoundError:
    print('缺少文件')

#按下鼠标按键
def press_mouse_button(button):
    if ok:
        gm.mouse_down(button)

#松开鼠标按键
def release_mouse_button(button):
    if ok:
        gm.mouse_up(button)

#点击鼠标
def click_mouse_button(button):
    press_mouse_button(button)
    release_mouse_button(button)

#按下键盘按键
def press_key(code):
    if ok:
        gm.key_down(code)

#松开键盘按键
def release_key(code):
    if ok:
        gm.key_up(code)

#点击键盘按键
def click_key(code):
    press_key(code)
    release_key(code)

# 鼠标移动
def mouse_xy(x, y, abs_move = False):
    if ok:
        gm.moveR(int(x), int(y), abs_move)


# click_mouse_button(3)  # 1:左键, 2:中键, 3:右键, 45:侧键