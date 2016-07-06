from ctypes  import windll
import win32con,win32gui
import time 
import random
from base import handle

user32 = windll.LoadLibrary('user32.dll')
kancolle_handle = handle.get_kancolle_handle()


def click(x,y):
    iparam=x + y * 65536
    user32.PostMessageW(kancolle_handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, iparam)
    time.sleep(0.1+random.random()*0.2) 
    user32.PostMessageW(kancolle_handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, iparam)
    time.sleep(0.1+random.random()*0.2)
    user32.PostMessageW(kancolle_handle, win32con.WM_LBUTTONUP,win32con.MK_LBUTTON, iparam)
    time.sleep(0.3+random.random()*0.2)
    
def get_color(x,y):
    hdc=win32gui.GetDC(kancolle_handle)
    return win32gui.GetPixel(hdc, x , y)

        
if __name__ == "__main__":
    print(get_color(205,251))