import sys
from PyQt5.QtWidgets import QApplication
from .gui import Gui
from .detection import Detector
from .aimbot import Aimbot
from .triggerbot import Triggerbot
import threading
import os

def main():
    # Detector and Aimbot setup
    detector = Detector()
    aimbot = Aimbot()
    triggerbot = Triggerbot()


    model_path = str(input('Enter full model path: '))
    detector.load_model(model_path, model_version="v5", do_force_reload=False)

    # Start the detector in a separate thread
    detection_thread = threading.Thread(target=detector.detect, daemon=True)
    detection_thread.start()

    # Start the aimbot in a separate thread
    aimbot_thread = threading.Thread(target=aimbot.loop, args=(detector,), daemon=True)
    aimbot_thread.start()

    triggerbot_thread = threading.Thread(target=triggerbot.loop, args=(detector,), daemon=True)
    triggerbot_thread.start()
    
    # Start PyQt5 GUI
    app = QApplication(sys.argv)
    ex = Gui()
    ex.show()

    # Execute the app, and exit the program once the GUI is closed
    sys.exit(app.exec_())

    # Wait for threads to finish (optional, depending on your app's design)
    detection_thread.join()
    aimbot_thread.join()
    triggerbot_thread.join()

if __name__ == "__main__":
    main()
