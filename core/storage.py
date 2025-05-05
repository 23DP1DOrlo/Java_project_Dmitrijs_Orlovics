import os
import json
from models.solve import Solve

class SolveStorage:
    def __init__(self, storage_dir="data"):
        self.storage_dir = storage_dir
        os.makedirs(self.storage_dir, exist_ok=True)

    def _get_file_path(self, username):
        return os.path.join(self.storage_dir, f"{username}_solves.json")

    def add_solve(self, solve):
        solves = self.get_user_solves(solve.user)
        solves.append(solve)
        self._save_solves(solve.user, solves)

    def get_user_solves(self, username):
        file_path = self._get_file_path(username)
        if not os.path.exists(file_path):
            return []
        with open(file_path, "r") as f:
            data = json.load(f)
            return [Solve.from_dict(item) for item in data]

    def _save_solves(self, username, solves):
        file_path = self._get_file_path(username)
        with open(file_path, "w") as f:
            json.dump([s.to_dict() for s in solves], f, indent=2)
