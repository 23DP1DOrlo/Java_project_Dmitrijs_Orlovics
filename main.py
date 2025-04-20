from models.solve import Solve
from models.storage import SolveStorage
from models.timer import Timer
from datetime import datetime

class TimerApp:
    def __init__(self):
        self.storage = SolveStorage()
        self.timer = Timer()

    def run(self):
        while True:
            print("\n1. New Solve\n2. Show All\n3. Best Solve\n4. Exit")
            choice = input("Choose: ")

            if choice == '1':
                self.time_new_solve()
            elif choice == '2':
                self.list_solves()
            elif choice == '3':
                self.show_best()
            elif choice == '4':
                break

    def time_new_solve(self):
        time_taken = self.timer.start_timer()
        print(f"Solve: {time_taken}s")

        penalty = input("Penalty? (+2 / DNF / Enter for OK): ").strip().upper()
        if penalty not in ["+2", "DNF"]:
            penalty = "OK"

        solve = Solve(time_taken, datetime.now().strftime("%Y-%m-%d %H:%M"), penalty=penalty)
        self.storage.add_solve(solve)

        print("Saved.")
        self.show_average(5)
        self.show_average(12)

    def list_solves(self):
        for i, s in enumerate(self.storage.solves, 1):
            print(f"{i}. {s.date} | {s.cube_type} | {s.time_taken}s | {s.penalty}")

    def show_average(self, n):
        times = [s.get_effective_time() for s in self.storage.solves if s.get_effective_time() is not None]
        if len(times) >= n:
            avg = sum(times[-n:]) / n
            print(f"Ao{n}: {round(avg, 2)}s")

    def show_best(self):
        valid_times = [s.get_effective_time() for s in self.storage.solves if s.get_effective_time() is not None]
        if valid_times:
            best = min(valid_times)
            print(f"Best: {best}s")
        else:
            print("No valid solves yet.")

if __name__ == "__main__":
    app = TimerApp()
    app.run()
