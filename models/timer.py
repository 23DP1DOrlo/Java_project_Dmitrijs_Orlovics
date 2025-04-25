import time
from pynput import keyboard

class Timer:
    def __init__(self):
        self.space_pressed_time = None
        self.solve_start_time = None
        self.last_solve_time = None

    def on_press(self, key):
        if key == keyboard.Key.space and self.space_pressed_time is None:
            self.space_pressed_time = time.time()
            print("⏳ Holding space...")

    def on_release(self, key):
        if key == keyboard.Key.space:
            hold_duration = time.time() - self.space_pressed_time
            self.space_pressed_time = None

            if hold_duration >= 0.6:
                print(f"✅ Space held {hold_duration:.2f}s. Timer started!")
                self.solve_start_time = time.time()
                input("▶️  Press Enter to stop timer...")
                self.stop_timer()
            else:
                print(f"❌ Held only {hold_duration:.2f}s — too short.")
            return False  

    def stop_timer(self):
        end = time.time()
        duration = round(end - self.solve_start_time, 2)
        self.last_solve_time = duration
        print(f"⏱️  Solve time: {duration}s")

    def start_timer(self):
        print("👉 Hold SPACE for at least 0.6 seconds to start the timer.")
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()
        return self.last_solve_time
