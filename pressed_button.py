import time


class ButtonPressTimer:
    def __init__(self):
        self.start_time = None

    def button_pressed(self):
        if self.start_time is None:
            self.start_time = time.time()

    def button_released(self):
        if self.start_time is not None:
            duration = time.time() - self.start_time
            self.start_time = None
            return duration
        else:
            return 0.0
