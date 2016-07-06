#!user/bin/env python3  
# coding=utf-8

import win32api,win32gui,win32con 
from cmath import rect
from base import tools

child_list=[]
HANDLE=None

def get_kancolle_ex_handle():
    hWndList = []  
    win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), hWndList)
    hWndList=filter_window_with_rect(hWndList)
    for hWnd in hWndList:
        title =  win32gui.GetWindowText(hWnd)
        if "提督業も忙しい" in title:
            return hWnd
        if "KanColleViewer" in title:
            return hWnd
        if "七四式電子" in title:
            return hWnd
    return None
    
def filter_window_with_rect(hWnd_list):
    for hWnd in hWnd_list:
        rect = win32gui.GetWindowRect(hWnd)
        if rect[2] - rect[0] <800 or rect[3] - rect[1] < 480:
            hWnd_list.remove(hWnd)
    return hWnd_list

def filter_child_with_rect(child_list):
    return_list = []
    for hWnd in child_list:
        rect = win32gui.GetWindowRect(hWnd)
        if rect[2] - rect[0] == 800 and rect[3] - rect[1] == 480:
            return_list.append(hWnd)
    return return_list

def find_child_handle(hWnd):
    child_list = win32gui.EnumChildWindows(hWnd,call_back,None)
    return child_list

def call_back(hwnd,param):
    global child_list
    child_list.append(hwnd)
    return True

def get_kancolle_handle():
    global HANDLE
    if HANDLE:
        return HANDLE
    else:
        HANDLE=get_handle()
        return HANDLE

def get_handle():
    global child_list
    ex_handle  = get_kancolle_ex_handle()
    find_child_handle(ex_handle)
    child_list=filter_child_with_rect(child_list)
    if not child_list:
        tools.messege_exit("could not found handle, please restart")
    return child_list[-1]

if __name__ == "__main__":
    print(get_kancolle_handle())

    

