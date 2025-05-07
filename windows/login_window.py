from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from core.auth import AuthManager
from windows.timer_window import TimerWindow

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(600, 300, 400, 250)
        self.auth = AuthManager()

        layout = QVBoxLayout()
        layout.setSpacing(15)

        label = QLabel("<h2>Login to Cube Timer</h2>")
        label.setAlignment(Qt.AlignCenter)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_btn = QPushButton("Login")
        self.signup_btn = QPushButton("Sign Up")

        layout.addWidget(label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_btn)
        layout.addWidget(self.signup_btn)

        self.setLayout(layout)

        self.login_btn.clicked.connect(self.handle_login)
        self.signup_btn.clicked.connect(self.handle_signup)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not self.validate_password(password):
            QMessageBox.warning(self, "Invalid Password", 
                "Password must start with an uppercase letter and be at least 6 characters long.")
            return

        success, msg = self.auth.login(username, password)
        if success:
            self.open_timer_window(username)
        else:
            QMessageBox.warning(self, "Login Failed", msg)


    def handle_signup(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not self.validate_password(password):
            QMessageBox.warning(self, "Invalid Password", 
                "Password must start with an uppercase letter and be at least 6 characters long.")
            return

        success, msg = self.auth.sign_up(username, password)
        QMessageBox.information(self, "Sign Up", msg)

    def validate_password(self, password):
        return (
            len(password) >= 6 and 
            password[0].isupper()
        )

    def open_timer_window(self, username):
        self.hide()
        self.timer_window = TimerWindow(username)
        self.timer_window.show()
