import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QPushButton, QComboBox
from PyQt5.QtCore import Qt

# Assuming shared_settings is a module where settings are stored.
from .settings import shared_settings

class Gui(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Control Panel')
        self.setGeometry(1000, 500, 235, 265)  # Position and size of the window

        main_layout = QVBoxLayout()

        # Header
        header = QLabel("Everlast")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        main_layout.addWidget(header)

        # Aim Key Dropdown
        aim_key_layout = QHBoxLayout()
        self.aim_key_label = QLabel("Aim Key:")
        aim_key_layout.addWidget(self.aim_key_label)
        self.aim_key_combo = QComboBox()
        self.aim_key_combo.addItems([chr(key) for key in range(ord('a'), ord('z') + 1)])
        self.aim_key_combo.setCurrentIndex(ord('r') - ord('a'))  # default value 'r'
        self.aim_key_combo.currentTextChanged.connect(self.update_aim_key)
        aim_key_layout.addWidget(self.aim_key_combo)
        main_layout.addLayout(aim_key_layout)

        # trigger bot key
        trigger_key_layout = QHBoxLayout()
        self.trigger_key_label = QLabel("Trigger Key:")
        trigger_key_layout.addWidget(self.trigger_key_label)
        self.trigger_key_combo = QComboBox()
        self.trigger_key_combo.addItems([chr(key) for key in range(ord('a'), ord('z') + 1)])
        self.trigger_key_combo.setCurrentIndex(ord('x') - ord('a'))  # default value 'x'
        self.trigger_key_combo.currentTextChanged.connect(self.update_trigger_key)
        trigger_key_layout.addWidget(self.trigger_key_combo)
        main_layout.addLayout(trigger_key_layout)

        # Targeting Options Menu
        target_layout = QHBoxLayout()
        self.target_label = QLabel("Targeting:")
        target_layout.addWidget(self.target_label)
        self.target_menu = QComboBox()
        self.target_menu.addItems(["Head", "Body", "Head and Body"])
        self.target_menu.currentTextChanged.connect(self.update_target)
        target_layout.addWidget(self.target_menu)
        main_layout.addLayout(target_layout)

        # Detection Size Slider
        detection_layout = QHBoxLayout()
        self.detection_size_label = QLabel("Detection Size:")
        detection_layout.addWidget(self.detection_size_label)
        self.detection_size_slider = QSlider(Qt.Horizontal)
        self.detection_size_slider.setMinimum(50)
        self.detection_size_slider.setMaximum(500)
        self.detection_size_slider.valueChanged.connect(self.update_detection_size)
        detection_layout.addWidget(self.detection_size_slider)
        self.detection_size_value = QLabel("200")
        detection_layout.addWidget(self.detection_size_value)
        self.detection_size_slider.setValue(200)
        main_layout.addLayout(detection_layout)

        # Max Distance Slider
        distance_layout = QHBoxLayout()
        self.max_distance_label = QLabel("Max Distance:")
        distance_layout.addWidget(self.max_distance_label)
        self.max_distance_slider = QSlider(Qt.Horizontal)
        self.max_distance_slider.setMinimum(0)
        self.max_distance_slider.setMaximum(500)
        self.max_distance_slider.valueChanged.connect(self.update_max_distance)
        distance_layout.addWidget(self.max_distance_slider)
        self.max_distance_value = QLabel("0")
        distance_layout.addWidget(self.max_distance_value)
        main_layout.addLayout(distance_layout)

        # Aimbot Strength Slider
        aimbot_layout = QHBoxLayout()
        self.aimbot_strength_label = QLabel("Aimbot Strength:")
        aimbot_layout.addWidget(self.aimbot_strength_label)
        self.aim_strength_slider = QSlider(Qt.Horizontal)
        self.aim_strength_slider.setMinimum(0)
        self.aim_strength_slider.setMaximum(100)
        self.aim_strength_slider.valueChanged.connect(self.update_aim_strength)
        aimbot_layout.addWidget(self.aim_strength_slider)
        self.aim_strength_value = QLabel("0")
        aimbot_layout.addWidget(self.aim_strength_value)
        main_layout.addLayout(aimbot_layout)

        # Toggle Button
        self.toggle_btn = QPushButton("Off")
        self.toggle_btn.clicked.connect(self.toggle)
        self.is_on = False
        main_layout.addWidget(self.toggle_btn)

        self.setLayout(main_layout)

    def toggle(self):
        self.is_on = not self.is_on
        self.toggle_btn.setText("[ON]" if self.is_on else "[OFF]")
        shared_settings.is_on = self.is_on

    def update_aim_strength(self, value):
        shared_settings.aim_strength = value
        self.aim_strength_value.setText(str(value))

    def update_max_distance(self, value):
        shared_settings.max_distance = value
        self.max_distance_value.setText(str(value))

    def update_aim_key(self, value):
        shared_settings.aim_key = value
    
    def update_trigger_key(self, value):
        shared_settings.trigger_key = value

    def update_target(self, value):
        shared_settings.target = value

    def update_detection_size(self, value):
        shared_settings.detection_size = value
        self.detection_size_value.setText(str(value))
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Gui()
    ex.show()
    sys.exit(app.exec_())
