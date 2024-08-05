# Everlast

An AI-powered aimbot and triggerbot system for Counter-Strike 2, leveraging YOLOv5/YOLOv8 object detection models. Written in Python, this project combines real-time screen capture, object detection, and precise mouse control to create an assistance tool for CS2.

## Features

- **AI-Powered Detection**: Utilizes YOLO (You Only Look Once) models for real-time object detection, capable of identifying player models in the game environment.
- **Customizable Targeting**: Offers options to target the head, body, or both, allowing for flexible aiming strategies.
- **Adjustable Settings**: Includes sliders for detection size, maximum distance, and aimbot strength, providing fine-tuned control over the assistance level.
- **Triggerbot Functionality**: Automatically fires when an enemy is detected in the crosshair, enhancing reaction times.
- **User-Friendly GUI**: Features a PyQt5-based graphical interface for easy configuration and control.
- **Hotkey Support**: Implements customizable hotkeys for activating aimbot and triggerbot functions.
- **Real-Time Performance**: Displays FPS (Frames Per Second) in the console title for monitoring system performance.

## Showcase

![Everlast Showcase](https://i.imgur.com/QHK30ws.png)

## Usage

1. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

2. Install pywin-mkb:
   - You can find pywin-mkb at [https://github.com/444995/pywin-mkb](https://github.com/444995/pywin-mkb)

3. Run Everlast:
   ```
   everlast
   ```

4. When prompted, enter the path to a YOLO model.
   - Pre-made models can be found in the `models/` directory.

5. Use the GUI to adjust settings and activate the aimbot/triggerbot as needed.

## Disclaimer

This project is for educational purposes only. Using this software in online games may violate terms of service and result in account bans. Use at your own risk.