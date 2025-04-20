import json
import os
from models.solve import Solve

class SolveStorage:
    def __init__(self, filepath="PYTHON_Project_Timer/Data/solves.json"):
        self.filename = filepath
        self.solves = []
        self.load()

    def add_solve(self, solve):
        self.solves.append(solve)
        self.save()

    def save(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump([s.to_dict() for s in self.solves], f, ensure_ascii=False, indent=2)

    def load(self):
        if not os.path.exists(self.filename):
            return
        with open(self.filename, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                self.solves = [Solve.from_dict(s) for s in data]
            except Exception as e:
                print("Error loading solves.json:", e)
