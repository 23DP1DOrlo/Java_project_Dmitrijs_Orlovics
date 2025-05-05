class Solve:
    def __init__(self, time_taken, date, user=None):
        self.time_taken = time_taken
        self.date = date
        self.user = user

    def to_dict(self):
        return {
            "time_taken": self.time_taken,
            "date": self.date,
            "user": self.user
        }

    @staticmethod
    def from_dict(data):
        return Solve(
            time_taken=data["time_taken"],
            date=data["date"],
            user=data.get("user")
        )
