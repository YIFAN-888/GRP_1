import os
import win32gui
import win32con
import time
import pyautogui

os.system('explorer ppt.pptx')
time.sleep(1)
hwnd_title = {}
def get_all_hwnd(hwnd, mouse):
    if (win32gui.IsWindow(hwnd)
            and win32gui.IsWindowEnabled(hwnd)
            and win32gui.IsWindowVisible(hwnd)):
        hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})
win32gui.EnumWindows(get_all_hwnd, 0)
for h, t in hwnd_title.items():
    if t :
        print (h, t)
#置顶窗口
print("置顶窗口")
hwnd = win32gui.FindWindow(None, "Panda AI.pptx - PowerPoint")
hwnd1 = win32gui.FindWindow(None, "DATA (D:)")
win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
# ctypes.windll.user32.ShowWindow(hwnd, 3)
win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                              win32con.SWP_NOMOVE | win32con.SWP_NOACTIVATE | win32con.SWP_NOOWNERZORDER | win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE)
win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,win32con.SWP_SHOWWINDOW|win32con.SWP_NOSIZE|win32con.SWP_NOMOVE)

win32gui.ShowWindow(hwnd1, win32con.SW_SHOWNORMAL)
win32gui.SetWindowPos(hwnd1, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                              win32con.SWP_NOMOVE | win32con.SWP_NOACTIVATE | win32con.SWP_NOOWNERZORDER | win32con.SWP_SHOWWINDOW | win32con.SWP_NOSIZE)
win32gui.SetWindowPos(hwnd1, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,win32con.SWP_SHOWWINDOW|win32con.SWP_NOSIZE|win32con.SWP_NOMOVE)
time.sleep(1)
pyautogui.hotkey('f5')
time.sleep(1)
pyautogui.click()
time.sleep(1)
pyautogui.click()
''' f'''