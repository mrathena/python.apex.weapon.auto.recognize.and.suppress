import ctypes
import time
from ctypes import wintypes

import win32con
import win32gui

user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32


class BITMAP(ctypes.Structure):
    _fields_ = [
        ("bmType", ctypes.c_long),
        ("bmWidth", ctypes.c_long),
        ("bmHeight", ctypes.c_long),
        ("bmWidthBytes", ctypes.c_long),
        ("bmPlanes", wintypes.DWORD),
        ("bmBitsPixel", wintypes.DWORD),
        ("bmBits", ctypes.c_void_p)
    ]


t1 = time.perf_counter_ns()

hdc = user32.GetDC(None)
hbmp = win32gui.GetCurrentObject(hdc, win32con.OBJ_BITMAP)
bmp = win32gui.GetObject(hbmp)
print(bmp)

# https://blog.csdn.net/alphabuilder/article/details/7555063
# http://timgolden.me.uk/pywin32-docs/win32gui__GetCurrentObject_meth.html
# http://timgolden.me.uk/pywin32-docs/win32gui__GetObject_meth.html
# http://timgolden.me.uk/pywin32-docs/PyBITMAP.html

user32.ReleaseDC(None, hdc)

t2 = time.perf_counter_ns()

print(f'耗时 {t2 - t1} ns')
