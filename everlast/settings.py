class Settings:
    def __init__(self):
        self.is_on = True
        self.aim_strength = 0
        self.max_distance = 0
        self.target = "Head"  # Default target
        self.aim_key = "r"  # Default aim key
        self.detection_size = 200
        self.trigger_key = "x"  # Default trigger key

shared_settings = Settings()
