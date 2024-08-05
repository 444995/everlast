from pywin_mkb.mouse import MouseController, Button
import time
import win32api
import win32con
from .settings import shared_settings
import ctypes
import keyboard

def get_screensize():
    return ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)

def get_mps():
    screensize = get_screensize()
    return screensize[0]//2, screensize[1]//2
class Triggerbot:
    def __init__(self):
        self.mouse = MouseController()
        self.mpx, self.mpy = get_mps()

    def is_lmb_pressed(self):
        return win32api.GetAsyncKeyState(win32con.VK_LBUTTON) < 0

    def is_ingame(self):
        user32 = ctypes.windll.user32
        hwnd = user32.GetForegroundWindow()
        title_length = user32.GetWindowTextLengthW(hwnd)
        title_buffer = ctypes.create_unicode_buffer(title_length + 1)
        user32.GetWindowTextW(hwnd, title_buffer, title_length + 1)
        return True if title_buffer.value == "Counter-Strike 2" else False

    def is_in_crosshair(self, x1, y1, x2, y2):        
        mpx, mpy = shared_settings.detection_size // 2, shared_settings.detection_size // 2
        if mpx >= x1 and mpx <= x2 and mpy >= y1 and mpy <= y2:
            print('in crosshair')
            return True

    def loop(self, detector):
        while True:
            if not self.is_ingame():
                time.sleep(0.1)
                continue

            if not shared_settings.is_on:
                time.sleep(0.1)
                continue

            if self.is_lmb_pressed():
                continue

            enemies = detector.enemies

            # check if any of the enemies are in the crosshair
            if keyboard.is_pressed(shared_settings.trigger_key):
                for enemy in enemies:
                    x1, y1, x2, y2 = enemy
                    if self.is_in_crosshair(x1, y1, x2, y2):
                        self.mouse.click(Button.left)
                        break
            
            time.sleep(0.01)
