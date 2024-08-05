import ctypes
import win32api, win32con, win32gui
import time
from pywin_mkb.mouse import MouseController, Button
from .settings import shared_settings
import keyboard


def get_screensize():
    return ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)

def get_mps():
    screensize = get_screensize()
    return screensize[0]//2, screensize[1]//2

def get_window_dims(mpx, mpy, size):
    return {"top": mpy - (size // 2), "left": mpx - (size // 2), "width": size, "height": size}


MPX, MPY = get_mps()


class Aimbot:
    def __init__(self):
        self.mouse = MouseController()
        self.mpx, self.mpy = get_mps()

    def is_ingame(self):
        user32 = ctypes.windll.user32
        hwnd = user32.GetForegroundWindow()
        title_length = user32.GetWindowTextLengthW(hwnd)
        title_buffer = ctypes.create_unicode_buffer(title_length + 1)
        user32.GetWindowTextW(hwnd, title_buffer, title_length + 1)
        return True if title_buffer.value == "Counter-Strike 2" else False

    def is_lmb_pressed(self):
        return win32api.GetAsyncKeyState(win32con.VK_LBUTTON) < 0

    def calculate_closest_enemy(self, enemies):
        closest_enemy = None
        min_distance = float('inf')
        mid_x = shared_settings.detection_size / 2
        mid_y = shared_settings.detection_size / 2

        for enemy in enemies:
            x1, y1, x2, y2 = enemy
            # calculate the mid point of the enemy
            enemy_mid_x = (x2 - x1) / 2 + x1
            enemy_mid_y = (y2 - y1) / 2 + y1

            # euclidean distance from midpoint of enemy to mid_x, mid_y of the screen
            distance = ((mid_x - enemy_mid_x) ** 2 + (mid_y - enemy_mid_y) ** 2) ** 0.5
            #print(f"distance: {distance}")
            #print(f"min_distance: {shared_settings.max_distance}")
            if distance > shared_settings.max_distance:
                continue

            if distance < min_distance:
                min_distance = distance
                closest_enemy = enemy
        
        return closest_enemy

    def move(self, x1, y1, x2, y2):
        monitor = get_window_dims(mpx=MPX, mpy=MPY, size=shared_settings.detection_size)
        x1 = monitor['left'] + x1
        x2 = monitor['left'] + x2
        y1 = monitor['top'] + y1
        y2 = monitor['top'] + y2

        mid_point_x = round(float(((x2 - x1) / 2) + x1))
        mid_point_y = round(float(((y2 - y1) / 2) + y1))

        strength = shared_settings.aim_strength*0.01 if shared_settings.aim_strength != 0 else 0
        final_x, final_y = round(((mid_point_x - self.mpx) * 0.6) * strength), round(((mid_point_y - self.mpy) *0.6 )* strength)

        self.mouse.move_relative(final_x, final_y)


    def loop(self, detector):
        # check if ingame 
        while True:
            if not self.is_ingame():
                time.sleep(0.1)
                continue

            if not shared_settings.is_on:
                time.sleep(0.1)
                continue

            # get screencap
            while keyboard.is_pressed(shared_settings.aim_key):
                enemies = detector.enemies

                if len(enemies) > 0:
                    preferred_enemy = self.calculate_closest_enemy(enemies)
                    if preferred_enemy is not None:
                        x1, y1, x2, y2 = preferred_enemy
                        self.move(x1=x1, y1=y1, x2=x2, y2=y2)
                
                time.sleep(0.1)


