class Solve:
    def __init__(self, time_taken, date, cube_type="3x3", penalty="OK"):
        self.time_taken = time_taken
        self.date = date
        self.cube_type = cube_type
        self.penalty = penalty

    def get_effective_time(self):
        if self.penalty == "DNF":
            return None
        elif self.penalty == "+2":
            return self.time_taken + 2
        return self.time_taken

    def to_dict(self):
        return {
            "time_taken": self.time_taken,
            "date": self.date,
            "cube_type": self.cube_type,
            "penalty": self.penalty,
        }

    @staticmethod
    def from_dict(data):
        return Solve(
            time_taken=data["time_taken"],
            date=data["date"],
            cube_type=data.get("cube_type", "3x3"),
            penalty=data.get("penalty", "OK")
        )
