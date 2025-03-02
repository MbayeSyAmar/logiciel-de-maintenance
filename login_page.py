from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QFrame
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize

class LoginPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Left side with image
        image_container = QFrame()
        image_container.setObjectName("login-image-container")
        image_layout = QVBoxLayout(image_container)
        image_label = QLabel()
        pixmap = QPixmap("icons/login_background.jpg")
        image_label.setPixmap(pixmap.scaled(600, 900, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        image_layout.addWidget(image_label)
        layout.addWidget(image_container)

        # Right side with login form
        login_container = QFrame()
        login_container.setObjectName("login-form-container")
        login_layout = QVBoxLayout(login_container)
        login_layout.setContentsMargins(50, 50, 50, 50)

        title = QLabel("Welcome Back")
        title.setObjectName("login-title")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        
        subtitle = QLabel("Please enter your credentials to log in.")
        subtitle.setObjectName("login-subtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        
        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")
        self.username.setObjectName("login-input")
        
        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setObjectName("login-input")
        
        login_button = QPushButton("Login")
        login_button.setObjectName("login-button")
        login_button.clicked.connect(self.attempt_login)
        
        login_layout.addWidget(title)
        login_layout.addWidget(subtitle)
        login_layout.addSpacing(30)
        login_layout.addWidget(self.username)
        login_layout.addWidget(self.password)
        login_layout.addWidget(login_button)
        login_layout.addStretch()

        layout.addWidget(login_container)

    def attempt_login(self):
        if self.main_window.login(self.username.text(), self.password.text()):
            self.username.clear()
            self.password.clear()
        else:
            self.main_window.show_error("Login Failed", "Invalid username or password.")
