import ctypes
from ctypes import wintypes

import win32con
import win32gui

class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [
        ("biSize", wintypes.DWORD),
        ("biWidth", ctypes.c_long),
        ("biHeight", ctypes.c_long),
        ("biPlanes", wintypes.WORD),
        ("biBitCount", wintypes.WORD),
        ("biCompression", wintypes.DWORD),
        ("biSizeImage", wintypes.DWORD),
        ("biXPelsPerMeter", ctypes.c_long),
        ("biYPelsPerMeter", ctypes.c_long),
        ("biClrUsed", wintypes.DWORD),
        ("biClrImportant", wintypes.DWORD)
    ]


class BITMAPINFO(ctypes.Structure):
    _fields_ = [
        ("bmiHeader", BITMAPINFOHEADER)
    ]


user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32

w, h = 3440, 1440

hwndDC = user32.GetDC(None)
saveDC = gdi32.CreateCompatibleDC(hwndDC)
# Get bitmap
bmp = gdi32.CreateCompatibleBitmap(hwndDC, w, h)
gdi32.SelectObject(saveDC, bmp)

# Init bitmap info
# We grab the image in RGBX mode, so that each word is 32bit and
# we have no striding, then we transform to RGB
buffer_len = h * w * 4
bmi = BITMAPINFO()
bmi.bmiHeader.biSize = ctypes.sizeof(BITMAPINFOHEADER)
bmi.bmiHeader.biWidth = w
bmi.bmiHeader.biHeight = -h  # Why minus? See [1]
bmi.bmiHeader.biPlanes = 1  # Always 1
bmi.bmiHeader.biBitCount = 32
bmi.bmiHeader.biCompression = 0
# Blit
image = ctypes.create_string_buffer(buffer_len)
bits = gdi32.GetDIBits(saveDC, bmp, 0, h, image, bmi, 0)
assert bits == h
# Replace pixels values: BGRX to RGB
image2 = ctypes.create_string_buffer(h * w * 3)
image2[0::3] = image[2::4]
image2[1::3] = image[1::4]
image2[2::3] = image[0::4]

img = bytes(image)
print(type(img), len(img))
for i in range(60):
    print(img[i])
