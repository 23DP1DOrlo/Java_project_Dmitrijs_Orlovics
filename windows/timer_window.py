import json
import time
import csv
from datetime import datetime

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget,
    QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer

# Заглушка scramble (можно заменить на свой генератор)
def generate_scramble():
    return "R U R' U R U2 R'"

class TimerWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle("Cube Timer")
        self.setGeometry(500, 150, 700, 550)

        self.username = username
        self.timer_running = False
        self.hold_start_time = None
        self.start_time = None
        self.elapsed_time = 0.0
        self.json_path = "PYTHON_Project_Timer/Data/solves.json"

        self.layout = QVBoxLayout()

        self.scramble = generate_scramble()
        self.scramble_label = QLabel(f"<b>Scramble:</b> {self.scramble}")
        self.scramble_label.setAlignment(Qt.AlignCenter)

        self.time_label = QLabel("00.00")
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet("font-size: 36px; color: #2e8b57")

        self.info_label = QLabel("Hold SPACE for 0.5s to start. Press any key to stop.")
        self.info_label.setAlignment(Qt.AlignCenter)

        self.solve_list = QListWidget()
        self.solve_list.setMinimumHeight(200)

        self.ao5_label = QLabel("ao5: -")
        self.ao12_label = QLabel("ao12: -")

        # Кнопки
        self.new_solve_btn = QPushButton("New Solve")
        self.new_solve_btn.setFixedWidth(120)
        self.new_solve_btn.clicked.connect(self.reset_timer)

        self.delete_btn = QPushButton("Delete Selected")
        self.delete_btn.setFixedWidth(120)
        self.delete_btn.clicked.connect(self.delete_selected)

        self.export_btn = QPushButton("Export CSV")
        self.export_btn.setFixedWidth(120)
        self.export_btn.clicked.connect(self.export_to_csv)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.new_solve_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.export_btn)

        self.layout.addWidget(self.scramble_label)
        self.layout.addWidget(self.time_label)
        self.layout.addWidget(self.info_label)
        self.layout.addWidget(self.solve_list)
        self.layout.addWidget(self.ao5_label)
        self.layout.addWidget(self.ao12_label)
        self.layout.addLayout(btn_layout)

        self.setLayout(self.layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_display)

        self.load_user_solves()
        self.update_averages()

    def keyPressEvent(self, event):
        if not self.timer_running and event.key() == Qt.Key_Space:
            self.hold_start_time = time.time()

    def keyReleaseEvent(self, event):
        if self.timer_running:
            self.stop_timer()
        elif self.hold_start_time and event.key() == Qt.Key_Space:
            held_duration = time.time() - self.hold_start_time
            if held_duration >= 0.5:
                self.start_timer()
            else:
                self.info_label.setText("❌ Hold at least 0.5s to start timer")
            self.hold_start_time = None

    def start_timer(self):
        self.start_time = time.time()
        self.elapsed_time = 0.0
        self.timer_running = True
        self.timer.start(10)
        self.info_label.setText("⏱️ Timer started! Press any key to stop.")

    def stop_timer(self):
        self.timer.stop()
        self.timer_running = False
        self.elapsed_time = time.time() - self.start_time
        self.time_label.setText(f"{self.elapsed_time:.2f}")
        self.save_result(self.elapsed_time)
        self.update_averages()

    def update_display(self):
        if self.timer_running:
            current_time = time.time() - self.start_time
            self.time_label.setText(f"{current_time:.2f}")

    def reset_timer(self):
        self.timer.stop()
        self.timer_running = False
        self.scramble = generate_scramble()
        self.scramble_label.setText(f"<b>Scramble:</b> {self.scramble}")
        self.time_label.setText("00.00")
        self.info_label.setText("Hold SPACE for 0.5s to start. Press any key to stop.")

    def save_result(self, time_taken):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result = {
            "username": self.username,
            "time_taken": round(time_taken, 2),
            "date": now
        }

        try:
            with open(self.json_path, "r") as file:
                results = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            results = []

        results.append(result)

        with open(self.json_path, "w") as file:
            json.dump(results, file, indent=4)

        self.solve_list.addItem(f"{now} - {time_taken:.2f}s")

    def load_user_solves(self):
        self.solve_list.clear()
        try:
            with open(self.json_path, "r") as file:
                results = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            results = []

        for r in results:
            if r["username"] == self.username:
                self.solve_list.addItem(f"{r['date']} - {r['time_taken']:.2f}s")

    def update_averages(self):
        try:
            with open(self.json_path, "r") as file:
                results = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            results = []

        user_times = [r["time_taken"] for r in results if r["username"] == self.username]

        if len(user_times) >= 5:
            ao5 = sum(user_times[-5:]) / 5
            self.ao5_label.setText(f"ao5: {ao5:.2f}")
        else:
            self.ao5_label.setText("ao5: -")

        if len(user_times) >= 12:
            ao12 = sum(user_times[-12:]) / 12
            self.ao12_label.setText(f"ao12: {ao12:.2f}")
        else:
            self.ao12_label.setText("ao12: -")

    def delete_selected(self):
        selected = self.solve_list.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Warning", "No solve selected.")
            return

        try:
            with open(self.json_path, "r") as file:
                results = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            results = []

        # Filter user solves
        user_solves = [r for r in results if r["username"] == self.username]

        if selected >= len(user_solves):
            return

        del_index = results.index(user_solves[selected])
        del results[del_index]

        with open(self.json_path, "w") as file:
            json.dump(results, file, indent=4)

        self.load_user_solves()
        self.update_averages()

    def export_to_csv(self):
        try:
            with open(self.json_path, "r") as file:
                results = json.load(file)
        except:
            results = []

        user_solves = [r for r in results if r["username"] == self.username]
        filename = f"{self.username}_solves.csv"

        with open(filename, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["date", "time_taken"])
            writer.writeheader()
            for r in user_solves:
                writer.writerow({"date": r["date"], "time_taken": r["time_taken"]})

        QMessageBox.information(self, "Exported", f"Solves exported to {filename}")
