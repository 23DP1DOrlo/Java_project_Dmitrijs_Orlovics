class Solve:
    def __init__(self, time_taken, date, cube_type="3x3", comment="", user=""):
        self.time_taken = time_taken
        self.date = date
        self.cube_type = cube_type
        self.comment = comment
        self.user = user

    def to_dict(self):
        return {
            "time": self.time_taken,
            "date": self.date,
            "cube_type": self.cube_type,
            "comment": self.comment,
            "user": self.user
        }

    @staticmethod
    def from_dict(data):
        return Solve(
            time_taken=data["time"],
            date=data["date"],
            cube_type=data.get("cube_type", "3x3"),
            comment=data.get("comment", ""),
            user=data.get("user", "")
        )