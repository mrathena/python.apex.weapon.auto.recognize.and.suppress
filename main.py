from PIL import ImageGrab, Image
import time
import numpy as np
import easyocr
import winsound
import ctypes
from ctypes import wintypes

# 轻型
# RE-45 自动手枪, P2020手枪, R301 卡宾枪, 喷火轻机枪, R-99 冲锋枪, 转换者冲锋枪, G7侦查枪
# 重型
# CAR, 30-30, 猎兽冲锋枪, 赫姆洛克突击步枪, 平行步枪
# 能量
# 电能冲锋枪, 三重式狙击枪, 专注轻机枪, 哈沃克步枪, L-STAR 能量机枪
# 狙击
# 哨兵狙击步枪, 辅助手枪, 充能步枪, 长弓
# 霰弹
# 莫桑比克, 和平捍卫这霰弹枪, EVE-8
# 空投
# 暴走, 波塞克, 敖犬霰弹枪, 克雷贝尔狙击枪

# 初始化 ctypes
user32 = ctypes.WinDLL('user32', use_last_error = True)
user32.GetDC.restype = wintypes.HDC
user32.GetDC.argtypes = (wintypes.HWND,)
gdi32 = ctypes.WinDLL('gdi32', use_last_error = True)
gdi32.GetPixel.restype = wintypes.COLORREF
gdi32.GetPixel.argtypes = (wintypes.HDC, ctypes.c_int, ctypes.c_int)
# 初始化 easyocr
reader = easyocr.Reader(['ch_sim', 'en'])

# 抖动, 参数1:按下鼠标左键的总持续时间, 参数2:下移像素
data = {
    "电能冲锋枪" : {
        'shake': [
            [100, 6], [400, 7], [600, 3], [1000, 0], [9999, 1]
        ]
    },
    "专注轻机枪" : {
        'shake': [
            [100, 8], [600, 5], [9999, 1]
        ]
    },
    "哈沃克步枪" : {
        'shake': [
            [100, 6], [300, 4], [600, 2], [9999, 1]
        ]
    },
    "L-STAR 能量机枪" : {
        'shake': [
            [100, 6], [300, 4], [600, 2], [9999, 1]
        ]
    },
    "LSTAR 能量机枪" : {
        'shake': [
            [100, 6], [300, 4], [600, 2], [1000, 4], [9999, 1]
        ]
    },
    "暴走" : {
        'shake': [
            [100, 3], [300, 2], [600, 1], [9999, 1]
        ]
    },
    "CAR" : {
        'shake': [
            [100, 6], [400, 8], [600, 4], [1000, 0], [9999, 1]
        ]
    },
    "猎兽冲锋枪" : {
        'shake': [
            [100, 6], [400, 8], [600, 4], [1000, 0], [9999, 1]
        ]
    },
    "赫姆洛克突击步枪" : {
        'shake': [
            [100, 6], [300, 4], [600, 2], [9999, 1]
        ]
    },
    "平行步枪" : {
        'shake': [
            [100, 6], [300, 4], [600, 2], [9999, 1]
        ]
    },
    "RE-45 自动手枪" : {
        'shake': [
            [100, 6], [400, 4], [1000, 2], [9999, 1]
        ]
    },
    "喷火轻机枪" : {
        'shake': [
            [100, 6], [300, 4], [600, 2], [9999, 1]
        ]
    },
    "R-301卡宾枪" : {
        'shake': [
            [100, 6], [300, 4], [600, 2], [9999, 1]
        ]
    },
    "转换者冲锋枪" : {
        'shake': [
            [100, 8], [300, 6], [500, 4], [1000, 3], [9999, 1]
        ]
    },
    "R-99冲锋枪" : {
        'shake': [
            [100, 6], [400, 8], [600, 4], [1000, 0], [9999, 1]
        ]
    }
}

def grab(x, y, width, height):
    return ImageGrab.grab((x, y, x + width, y + height))

def isNotInGame():
    hdc = user32.GetDC(None)
    return 16777215 != gdi32.GetPixel(hdc, 236, 1344) and 16777215 != gdi32.GetPixel(hdc, 3367, 67)

# 获取当前装备的枪, 0:没有枪, 1:1号枪, 2:2号枪
def getGunIndex():
    hdc = user32.GetDC(None)
    color = gdi32.GetPixel(hdc, 2900, 1372)
    if color == 8421504:
        return 0
    else:
        color2 = gdi32.GetPixel(hdc, 2900, 1373)
        return 1 if color2 == color else 2

# 获取枪的名字
def getGunName(x, y, width, height):
    result = reader.readtext(np.array(grab(x, y, width, height)), detail=0)
    return None if len(result) == 0 else result[0]


# main
winsound.Beep(2000, 100)

while True:
    time.sleep(1)
    if isNotInGame():
        print('wait join game')
        continue

    index = getGunIndex()
    if index == 0:
        # no gun, clear macro script
        file = open("C://apex.lua", "w")
        file.writelines("")
        file.close()
    else:
        name = getGunName(2946 if index == 1 else 3141, 1381, 170, 26)
        print(name)
        temp = data.get(name)
        if (temp is None):
            # gun data not found, clear macro script
            file = open("C://apex.lua", "w")
            file.writelines("")
            file.close()
            continue
        file = open("C://apex.lua", "w")
        file.writelines("enable = true\n")
        for key in temp:
            file.writelines(key + " = " + str(temp.get(key)).lower().replace('[', '{').replace(']', '}') + "\n")
        file.close()







