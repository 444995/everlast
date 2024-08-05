import torch
from PIL import ImageGrab
import ctypes
from mss import mss
import numpy as np
import cv2
from .settings import shared_settings
import time
import threading
from ultralytics import YOLO

def get_screensize():
    return ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)

def get_mps():
    screensize = get_screensize()
    return screensize[0]//2, screensize[1]//2

def get_window_dims(mpx, mpy, size):
    return {"top": mpy - (size // 2), "left": mpx - (size // 2), "width": size, "height": size}


MPX, MPY = get_mps()


class Detector:
    def __init__(self):
        self.enemies = []
        self.screengrab = None

    def load_model(self, model_path, model_version="v5", do_force_reload=False):
        if model_version == "v5": self.model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, force_reload=do_force_reload)
        elif model_version == "v8": self.model = YOLO(model_path, verbose=False)
        else: raise ValueError("Invalid model version")

        self.model_version = model_version

    def grab_screencap(self):
        while True:
            with mss() as sct:
                screenshot = sct.grab(get_window_dims(mpx=MPX, mpy=MPY, size=shared_settings.detection_size))
                self.screengrab = np.array(screenshot)

    def detect(self):
        screenshot_thread = threading.Thread(target=self.grab_screencap, args=())
        screenshot_thread.daemon = True
        screenshot_thread.start()

        prev_time = time.time()
        while True:
            if not shared_settings.is_on:
                time.sleep(0.1)
                continue

            if self.screengrab is None:
                continue

            conv_img = cv2.cvtColor(self.screengrab, cv2.COLOR_BGR2RGB)
            #results = self.model(conv_img)
            if self.model_version == "v5":
                results = self.model(conv_img)  # YOLOv5 uses the converted image
            elif self.model_version == "v8":
                results = self.model.predict(conv_img)  # YOLOv8 uses the original image
            else:
                raise ValueError("Invalid model version")

            enemies = []
            boxes = results.xyxy[0] if self.model_version == "v5" else results[0].boxes

            for box in boxes:
                if self.model_version == "v8":
                    xyxy = box.xyxy[0]  # YOLOv8 specific format
                    conf = box.conf[0]
                    cls = box.cls[0]
                else:
                    *xyxy, conf, cls = box  # YOLOv5 format

                label = self.model.names[int(cls)]
                x1, y1, x2, y2 = map(float, xyxy)
                target_labels = []

                # Define target labels based on a configuration
                if shared_settings.target == "Head":
                    target_labels = ["ct_head", "t_head"]
                elif shared_settings.target == "Body":
                    target_labels = ["ct_body", "t_body"]
                elif shared_settings.target == "Head and Body":
                    target_labels = ["ct_head", "t_head", "ct_body", "t_body"]

                # Check if the detected object is a target
                if label in target_labels:
                    enemies.append((round(x1), round(y1), round(x2), round(y2)))
                    cv2.rectangle(self.screengrab, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)
                    cv2.rectangle(self.screengrab, (int((x1 - shared_settings.max_distance) * 1.05), int((y1 - shared_settings.max_distance) * 1.05)), 
                                (int((x2 + shared_settings.max_distance) * 0.95), int((y2 + shared_settings.max_distance) * 0.95)), (0, 255, 0), 2)

            self.enemies = enemies

            
            current_time = time.time()
            fps = 1.0 / (current_time - prev_time)
            prev_time = current_time

            ctypes.windll.kernel32.SetConsoleTitleW(f"fps: {fps:.2f}")
            
            #cv2.imshow('Frame', self.screengrab)

            #if cv2.waitKey(1) & 0xFF == ord('q'):
            #    break

        #cv2.destroyAllWindows()