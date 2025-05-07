import time
import json
import math
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidgetItem, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QAbstractItemView, QMessageBox, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, QTimer
from core.scramble_generator import generate_scramble

class TimerWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle("Cube Timer")
        self.setGeometry(500, 150, 600, 500)

        self.session_times = [] 
        self.username = username 
        self.timer_running = False 
        self.key_hold_start = None
        self.start_time = None
        self.elapsed_time = 0
        self.scramble = generate_scramble() 
        self.init_ui()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer) 
        self.timer.start(10) 

    def update_username(self, new_username):
        self.username = new_username
        self.username_label.setText(f"Logged in as: {self.username}")

    def init_ui(self):
        self.timer_layout = QVBoxLayout()
        self.timer_layout.setSpacing(12)

        self.scramble_label = QLabel(f"Scramble: {self.scramble}")
        self.scramble_label.setAlignment(Qt.AlignCenter)

        self.time_label = QLabel("0.00") 
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet("font-size: 32px; color: #2e8b57")

        self.info_label = QLabel("Hold SPACE for 0.5s to start. Press any key to stop.")
        self.info_label.setAlignment(Qt.AlignCenter)

        self.ao5_label = QLabel("ao5: -")
        self.ao12_label = QLabel("ao12: -")
        self.ao5_label.setAlignment(Qt.AlignCenter)
        self.ao12_label.setAlignment(Qt.AlignCenter)

        self.start_button = QPushButton("New Solve")
        self.start_button.setFixedWidth(150)
        self.start_button.clicked.connect(self.prepare_new_solve)

        bottom_layout = QHBoxLayout()
        bottom_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding))
        bottom_layout.addWidget(self.start_button)
        bottom_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding))
        
        self.logout_button = QPushButton("Logout")
        self.logout_button.setFixedWidth(150)
        self.logout_button.clicked.connect(self.logout)

        logout_layout = QHBoxLayout()
        logout_layout.addSpacerItem(QSpacerItem(100, 20, QSizePolicy.Expanding))
        logout_layout.addWidget(self.logout_button)
        logout_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding))

        self.timer_layout.addLayout(logout_layout)

        self.timer_layout.addWidget(self.scramble_label)
        self.timer_layout.addWidget(self.time_label)
        self.timer_layout.addWidget(self.info_label)
        self.timer_layout.addWidget(self.ao5_label)
        self.timer_layout.addWidget(self.ao12_label)
        self.timer_layout.addLayout(bottom_layout)

        # Solve  list
        self.session_list = QListWidget()
        self.session_list.setSelectionMode(QAbstractItemView.SingleSelection)

        self.delete_button = QPushButton("Delete Selected Solve")
        self.delete_button.clicked.connect(self.delete_selected_solve)

        side_layout = QVBoxLayout()
        side_layout.addWidget(QLabel("Session Solves:"))
        side_layout.addWidget(self.session_list)
        side_layout.addWidget(self.delete_button)

        main_layout = QHBoxLayout()
        main_layout.addLayout(self.timer_layout)
        main_layout.addLayout(side_layout)

        self.setLayout(main_layout)

        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()

        # Sorting
        filter_sort_layout = QHBoxLayout()

        self.sort_button = QPushButton("Sort")
        self.sort_button.clicked.connect(self.sort_session_list)

        self.min_time_input = QLineEdit()
        self.min_time_input.setPlaceholderText("Min.(s)")

        self.max_time_input = QLineEdit()
        self.max_time_input.setPlaceholderText("Max.(s)")

        self.filter_button = QPushButton("Filter")
        self.filter_button.clicked.connect(self.filter_session_list)

        filter_sort_layout.addWidget(self.sort_button)
        filter_sort_layout.addWidget(self.min_time_input)
        filter_sort_layout.addWidget(self.max_time_input)
        filter_sort_layout.addWidget(self.filter_button)

        side_layout.insertLayout(1, filter_sort_layout)
    def keyPressEvent(self, event):
        # Timer start
        if event.key() == Qt.Key_Space and not self.timer_running:
            if self.key_hold_start is None:
                self.key_hold_start = time.time()

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Space:
            if self.key_hold_start is not None:
                duration = time.time() - self.key_hold_start
                self.key_hold_start = None

                if duration >= 0.5 and not self.timer_running:
                    self.timer_running = True
                    self.start_time = time.time() - self.elapsed_time
                    self.info_label.setText("Timer started! Press SPACE to stop.")
                else:
                    self.info_label.setText("Hold at least 0.5s to start timer")
            elif self.timer_running:
                self.stop_timer()


    def sort_session_list(self):
        # sorting
        times = self.session_times[:]
        times_sorted = sorted(times)

        if self.sort_button.text() == "Sort":
            self.sort_button.setText("Descending")
        elif self.sort_button.text() == "Descending":
            times_sorted = list(reversed(times_sorted))
            self.sort_button.setText("Ascending")
        else:
            self.sort_button.setText("Sort")

        self.session_list.clear()
        for t in times_sorted:
            self.session_list.addItem(f"{round(t, 2)} s")

    def filter_session_list(self):
        min_time = self.min_time_input.text()
        max_time = self.max_time_input.text()

        try:
            min_val = float(min_time) if min_time else 0
            max_val = float(max_time) if max_time else float('inf')
        except ValueError:
            QMessageBox.warning(self, "Error", "Input right format of time.")
            return

        self.session_list.clear()
        for t in self.session_times:
            if min_val <= t <= max_val:
                self.session_list.addItem(f"{round(t, 2)} s")

    def update_timer(self):
        if self.timer_running:
            elapsed = time.time() - self.start_time
            self.time_label.setText(f"{elapsed:.2f} s") 

    def stop_timer(self):
        self.timer_running = False
        self.elapsed_time = time.time() - self.start_time
        final_time = math.floor(self.elapsed_time * 100) / 100

        if final_time > 0:
            self.session_times.append(final_time)
            self.save_result(final_time)
            self.scramble = generate_scramble()
            self.scramble_label.setText(f"Scramble: {self.scramble}")
            self.info_label.setText("Hold SPACE for 0.5s to start. Press any key to stop.")
            self.reset_timer()
            new_item = QListWidgetItem(f"{final_time:.2f} s")
            self.session_list.addItem(new_item)
            self.update_averages()
        else:
            self.info_label.setText("Timer didn't start properly.")
            print("Timer didn't start properly!")

    def save_result(self, time_taken):
        result = {
            "username": self.username,
            "scramble": self.scramble,
            "time_taken": round(time_taken, 2),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        try:
            with open("Data/solves.json", "r") as file:
                results = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            results = []

        results.append(result)

        with open("Data/solves.json", "w") as file:
            json.dump(results, file, indent=4)

    def delete_selected_solve(self):
        selected = self.session_list.currentRow()
        if selected != -1:
            confirm = QMessageBox.question(self, "Delete Solve", "Are you sure you want to delete this solve?", QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                self.session_list.takeItem(selected)
                del self.session_times[selected]
                self.update_averages()
                
    def prepare_new_solve(self):
        self.time_label.setText("00.00")
        self.elapsed_time = 0
        self.info_label.setText("Hold SPACE for 0.5s to start. Press any key to stop.")
        
        self.scramble = generate_scramble()  # New scramble gener
        self.scramble_label.setText(f"Scramble: {self.scramble}")  # Renew scramble
        
        self.setFocus()

    def reset_timer(self):
        # Timer reset after stop
        self.elapsed_time = 0
        self.start_time = None
        self.timer_running = False

    def update_averages(self):
        def calculate_wca_average(times, count):
            if len(times) < count:
                return "-"
            last_n = times[-count:]
            trimmed = sorted(last_n)[1:-1]
            average = sum(trimmed) / len(trimmed)
            return f"{average:.2f}"

        self.ao5_label.setText(f"ao5: {calculate_wca_average(self.session_times, 5)}")
        self.ao12_label.setText(f"ao12: {calculate_wca_average(self.session_times, 12)}")

    def logout(self):
        from windows.login_window import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()
        
    def closeEvent(self, event):
        event.accept()