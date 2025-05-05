import time

class Timer:
    def __init__(self):
        self.start_time = None
        self.end_time = None

    def start(self):
        self.start_time = time.time()
        self.end_time = None

    def stop(self):
        if self.start_time is None:
            return 0.0
        self.end_time = time.time()
        duration = self.end_time - self.start_time
        self.start_time = None
        return duration
