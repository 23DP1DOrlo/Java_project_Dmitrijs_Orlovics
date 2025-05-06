import time
import json
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, QTimer
from core.scramble_generator import generate_scramble  # Убедись, что этот импорт правильный

class TimerWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle("Cube Timer")
        self.setGeometry(500, 150, 600, 500)

        self.username = username
        self.timer_running = False  # Флаг работы таймера
        self.key_hold_start = None
        self.start_time = None
        self.elapsed_time = 0

        self.scramble = generate_scramble()  # Генерация первого скрамбла
        self.init_ui()

        # Таймер для обновления времени
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)  # Будет вызываться каждый раз, когда таймер "выполняет" timeout
        self.timer.start(10)  # Обновлять каждую 10 миллисекунд для сотых долей секунды

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setSpacing(12)

        self.scramble_label = QLabel(f"Scramble: {self.scramble}")  # Отображаем скрамбл
        self.scramble_label.setAlignment(Qt.AlignCenter)

        self.time_label = QLabel("00.00")  # Начальное значение таймера
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet("font-size: 32px; color: #2e8b57")

        self.info_label = QLabel("Hold SPACE for 0.5s to start. Press any key to stop.")
        self.info_label.setAlignment(Qt.AlignCenter)

        # Добавляем элементы для отображения AO5 и AO12
        self.ao5_label = QLabel("AO5: -")
        self.ao12_label = QLabel("AO12: -")
        self.ao5_label.setAlignment(Qt.AlignCenter)
        self.ao12_label.setAlignment(Qt.AlignCenter)

        self.start_button = QPushButton("New Solve")
        self.start_button.setFixedWidth(150)
        self.start_button.clicked.connect(self.prepare_new_solve)

        bottom_layout = QHBoxLayout()
        bottom_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding))
        bottom_layout.addWidget(self.start_button)
        bottom_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding))

        self.layout.addWidget(self.scramble_label)
        self.layout.addWidget(self.time_label)
        self.layout.addWidget(self.info_label)
        self.layout.addWidget(self.ao5_label)  # Добавляем AO5
        self.layout.addWidget(self.ao12_label)  # Добавляем AO12
        self.layout.addLayout(bottom_layout)
        self.setLayout(self.layout)

    def keyPressEvent(self, event):
        """Задержка удержания пробела, запускающая таймер"""
        if event.key() == Qt.Key_Space and not self.timer_running:
            if self.key_hold_start is None:
                # Начало отсчета, если пробел удерживается
                self.key_hold_start = time.time()

    def keyReleaseEvent(self, event):
        """Останавливаем таймер по отпусканию пробела или любой клавиши"""
        if event.key() == Qt.Key_Space:
            if self.key_hold_start is not None:
                duration = time.time() - self.key_hold_start
                self.key_hold_start = None

                if duration >= 0.5 and not self.timer_running:
                    # Таймер начинает отсчет после 0.5 секунд
                    self.timer_running = True
                    self.start_time = time.time() - self.elapsed_time  # продолжаем с последнего времени
                    self.info_label.setText("⏱️ Timer started! Press any key to stop.")
                else:
                    self.info_label.setText("❌ Hold at least 0.5s to start timer")

        # При отпускании пробела или любой клавиши останавливаем таймер
        elif (event.key() == Qt.Key_Space or event.key() != Qt.Key_Space) and self.timer_running:
            self.stop_timer()

    def update_timer(self):
        """Обновление времени таймера (сотые секунды)"""
        if self.timer_running:
            elapsed = time.time() - self.start_time
            self.time_label.setText(f"{elapsed:.2f} s")  # Отображаем время с сотыми долями секунды

    def stop_timer(self):
        """Остановка таймера и сохранение результата в JSON файл"""
        self.timer_running = False
        self.elapsed_time = time.time() - self.start_time
        self.time_label.setText(f"{self.elapsed_time:.2f} s")

        # Сохраняем результат в JSON
        self.save_result()

        # Генерация нового скрамбла для следующей сборки
        self.scramble = generate_scramble()
        self.scramble_label.setText(f"Scramble: {self.scramble}")  # Обновление метки скрамбла

        self.info_label.setText("Hold SPACE for 0.5s to start. Press any key to stop.")
        self.reset_timer()

        # Обновляем AO5 и AO12
        self.update_averages()

    def save_result(self):
        """Запись результата в JSON файл"""
        result = {
            "username": self.username,
            "scramble": self.scramble,
            "time_taken": round(self.elapsed_time, 2),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        # Чтение существующих данных из файла, если есть
        try:
            with open("Data/solves.json", "r") as file:
                results = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            results = []

        # Добавляем новый результат в список
        results.append(result)

        # Записываем данные обратно в файл
        with open("Data/solves.json", "w") as file:
            json.dump(results, file, indent=4)

    def prepare_new_solve(self):
        """Подготовка к новому решению"""
        self.time_label.setText("00.00")
        self.elapsed_time = 0
        self.info_label.setText("Hold SPACE for 0.5s to start. Press any key to stop.")
        
        self.scramble = generate_scramble()  # Генерация нового скрамбла
        self.scramble_label.setText(f"Scramble: {self.scramble}")  # Обновление метки скрамбла

    def reset_timer(self):
        """Сброс таймера после остановки"""
        self.elapsed_time = 0
        self.start_time = None
        self.timer_running = False

    def update_averages(self):
        """Обновление статистики AO5 и AO12"""
        try:
            with open("Data/solves.json", "r") as file:
                results = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            results = []

        user_times = [r["time_taken"] for r in results if r["username"] == self.username]

        # Рассчитываем AO5
        if len(user_times) >= 5:
            ao5 = sum(user_times[-5:]) / 5
            self.ao5_label.setText(f"ao5: {ao5:.2f}")
        else:
            self.ao5_label.setText("ao5: -")

        # Рассчитываем AO12
        if len(user_times) >= 12:
            ao12 = sum(user_times[-12:]) / 12
            self.ao12_label.setText(f"ao12: {ao12:.2f}")
        else:
            self.ao12_label.setText("ao12: -")

    def closeEvent(self, event):
        """Закрытие окна таймера"""
        event.accept()
