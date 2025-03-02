from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget, QFrame
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor, QLinearGradient
from PyQt5.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve

from database import Database
from login_page import LoginPage
from dashboard_page import DashboardPage
from machines_page import MachinesPage
from users_page import UsersPage
from calendar_page import CalendarPage
from inspections_page import InspectionsPage
from resources_page import ResourcesPage
from work_orders_page import WorkOrdersPage
from inventory_page import InventoryPage
from notifications import NotificationSystem

class MainWindow(QMainWindow):
    def __init__(self):
        
        super().__init__()
        self.db = Database()
        self.notification_system = NotificationSystem()
        self.add_test_user()
        self.current_user = None
        self.setWindowTitle("Advanced Dashboard")
        self.setGeometry(100, 100, 1400, 900)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QHBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(250)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(0, 0, 0, 0)
        self.sidebar_layout.setSpacing(0)
        
        self.content = QStackedWidget()
        self.content.setObjectName("content")
        
        self.layout.addWidget(self.sidebar)
        self.layout.addWidget(self.content)
        
        self.setup_sidebar()
        self.setup_pages()
        
        self.apply_styles()

    def setup_sidebar(self):
        logo = QLabel("Dashboard")
        logo.setObjectName("logo")
        logo.setAlignment(Qt.AlignCenter)
        self.sidebar_layout.addWidget(logo)
        
        self.sidebar_buttons = []
        buttons = [
            ("Dashboard", "dashboard.png"),
            ("Machines", "machine.png"),
            ("Users", "users.png"),
            ("Calendar", "calendar.png"),
            ("Inspections", "inspection.png"),
            ("Resources", "resources.png"),
            ("Work Orders", "work_order.png"),
            ("Inventory", "inventory.png")
        ]
        for button_text, icon_name in buttons:
            button = QPushButton(QIcon(f"icons/{icon_name}"), button_text)
            button.setObjectName("sidebar-button")
            button.setIconSize(QSize(24, 24))
            button.setCheckable(True)
            self.sidebar_layout.addWidget(button)
            button.clicked.connect(lambda checked, text=button_text: self.change_page(text))
            self.sidebar_buttons.append(button)
        
        self.sidebar_layout.addStretch()
        
        self.logout_button = QPushButton("Logout")
        self.logout_button.setObjectName("logout-button")
        self.logout_button.clicked.connect(self.logout)
        self.sidebar_layout.addWidget(self.logout_button)
        
        theme_switch = QPushButton("Toggle Theme")
        theme_switch.setObjectName("theme-switch")
        theme_switch.clicked.connect(self.toggle_theme)
        self.sidebar_layout.addWidget(theme_switch)

    def setup_pages(self):
        self.login_page = LoginPage(self)
        self.dashboard_page = DashboardPage(self)
        self.machines_page = MachinesPage(self)
        self.users_page = UsersPage(self)
        self.calendar_page = CalendarPage(self)
        self.inspections_page = InspectionsPage(self)
        self.resources_page = ResourcesPage(self)
        self.work_orders_page = WorkOrdersPage(self)
        self.inventory_page = InventoryPage(self)
        
        self.content.addWidget(self.login_page)
        self.content.addWidget(self.dashboard_page)
        self.content.addWidget(self.machines_page)
        self.content.addWidget(self.users_page)
        self.content.addWidget(self.calendar_page)
        self.content.addWidget(self.inspections_page)
        self.content.addWidget(self.resources_page)
        self.content.addWidget(self.work_orders_page)
        self.content.addWidget(self.inventory_page)
        
        self.content.setCurrentWidget(self.login_page)

    def change_page(self, page_name):
        if not self.current_user:
            return
        
        page_map = {
            "Dashboard": self.dashboard_page,
            "Machines": self.machines_page,
            "Users": self.users_page,
            "Calendar": self.calendar_page,
            "Inspections": self.inspections_page,
            "Resources": self.resources_page,
            "Work Orders": self.work_orders_page,
            "Inventory": self.inventory_page
        }
        
        if page_name in page_map:
            if page_name == "Users" and self.current_user[3] != "Super Admin":
                self.notification_system.show_warning(self, "Access Denied", "You don't have permission to access this page.")
            else:
                self.content.setCurrentWidget(page_map[page_name])
                for button in self.sidebar_buttons:
                    button.setChecked(button.text() == page_name)

    def login(self, username, password):
        user = self.db.authenticate_user(username, password)
        if user:
            self.current_user = user
            self.content.setCurrentWidget(self.dashboard_page)
            self.update_sidebar_visibility(True)
            self.change_page("Dashboard")
            return True
        return False

    def logout(self):
        self.current_user = None
        self.content.setCurrentWidget(self.login_page)
        self.update_sidebar_visibility(False)

    def update_sidebar_visibility(self, visible):
        for button in self.sidebar_buttons:
            button.setVisible(visible)
        self.logout_button.setVisible(visible)

    def toggle_theme(self):
        if self.styleSheet() == self.light_style:
            self.setStyleSheet(self.dark_style)
        else:
            self.setStyleSheet(self.light_style)

    def apply_styles(self):
        self.light_style = """
        QWidget {
            font-family: 'Segoe UI', sans-serif;
            font-size: 14px;
        }
        QMainWindow {
            background-color: #f0f4f8;
        }
        #sidebar {
            background-color: #1a237e;
            border-right: 1px solid #3949ab;
        }
        #logo {
            font-size: 28px;
            color: white;
            padding: 20px;
            font-weight: bold;
            background-color: #0d47a1;
        }
        #sidebar-button {
            background-color: transparent;
            border: none;
            color: white;
            text-align: left;
            padding: 15px;
            font-size: 16px;
            border-left: 5px solid transparent;
        }
        #sidebar-button:hover {
            background-color: #283593;
            border-left: 5px solid #5c6bc0;
        }
        #sidebar-button:checked {
            background-color: #3949ab;
            border-left: 5px solid #8c9eff;
        }
        QPushButton {
            background-color: #3949ab;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 5px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #5c6bc0;
        }
        QLineEdit {
            padding: 10px;
            border: 2px solid #bdc3c7;
            border-radius: 5px;
            background-color: white;
        }
        QLineEdit:focus {
            border: 2px solid #3949ab;
        }
        QTableWidget {
            border: none;
            gridline-color: #e0e0e0;
            background-color: white;
        }
        QHeaderView::section {
            background-color: #f5f5f5;
            color: #333;
            padding: 5px;
            border: 1px solid #e0e0e0;
            font-weight: bold;
        }
        #content {
            background-color: white;
            border-radius: 10px;
            margin: 10px;
        }
        #dashboard-header {
            color: #1a237e;
            margin-bottom: 20px;
            font-size: 32px;
            font-weight: bold;
        }
        #dashboard-scroll-area {
            background-color: transparent;
            border: none;
        }
        #stat-widget {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 20px;
            margin: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        #stat-value {
            font-size: 48px;
            font-weight: bold;
            color: #3949ab;
        }
        #stat-description {
            font-size: 18px;
            color: #546e7a;
        }
        #activities-widget, #maintenance-widget {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 20px;
            margin: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        #widget-header {
            font-size: 24px;
            font-weight: bold;
            color: #1a237e;
            margin-bottom: 15px;
        }
        #activity-item, #maintenance-item {
            padding: 10px 0;
            border-bottom: 1px solid #e0e0e0;
            font-size: 16px;
            color: #37474f;
        }
        """
        
        self.dark_style = """
        QWidget {
            font-family: 'Segoe UI', sans-serif;
            font-size: 14px;
        }
        QMainWindow {
            background-color: #121212;
        }
        #sidebar {
            background-color: #1f1f1f;
            border-right: 1px solid #2c2c2c;
        }
        #logo {
            font-size: 28px;
            color: #ffffff;
            padding: 20px;
            font-weight: bold;
            background-color: #2c2c2c;
        }
        #sidebar-button {
            background-color: transparent;
            border: none;
            color: #ffffff;
            text-align: left;
            padding: 15px;
            font-size: 16px;
            border-left: 5px solid transparent;
        }
        #sidebar-button:hover {
            background-color: #2c2c2c;
            border-left: 5px solid #3949ab;
        }
        #sidebar-button:checked {
            background-color: #3949ab;
            border-left: 5px solid #8c9eff;
        }
        QPushButton {
            background-color: #3949ab;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 5px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #5c6bc0;
        }
        QLineEdit {
            padding: 10px;
            border: 2px solid #3c3c3c;
            border-radius: 5px;
            background-color: #2c2c2c;
            color: #ffffff;
        }
        QLineEdit:focus {
            border: 2px solid #3949ab;
        }
        QTableWidget {
            border: none;
            gridline-color: #3c3c3c;
            background-color: #1f1f1f;
            color: #ffffff;
        }
        QHeaderView::section {
            background-color: #2c2c2c;
            color: #ffffff;
            padding: 5px;
            border: 1px solid #3c3c3c;
            font-weight: bold;
        }
        #content {
            background-color: #1f1f1f;
            border-radius: 10px;
            margin: 10px;
        }
        #dashboard-header {
            color: #ffffff;
            margin-bottom: 20px;
            font-size: 32px;
            font-weight: bold;
        }
        #dashboard-scroll-area {
            background-color: transparent;
            border: none;
        }
        #stat-widget {
            background-color: #2c2c2c;
            border-radius: 10px;
            padding: 20px;
            margin: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }
        #stat-value {
            font-size: 48px;
            font-weight: bold;
            color: #8c9eff;
        }
        #stat-description {
            font-size: 18px;
            color: #b0bec5;
        }
        #activities-widget, #maintenance-widget {
            background-color: #2c2c2c;
            border-radius: 10px;
            padding: 20px;
            margin: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }
        #widget-header {
            font-size: 24px;
            font-weight: bold;
            color: #ffffff;
            margin-bottom: 15px;
        }
        #activity-item, #maintenance-item {
            padding: 10px 0;
            border-bottom: 1px solid #3c3c3c;
            font-size: 16px;
            color: #b0bec5;
        }
        """
        
        self.setStyleSheet(self.light_style)

    def add_test_user(self):
        if not self.db.authenticate_user("admin", "password"):
            self.db.add_user("admin", "password", "Super Admin")
            self.db.validate_user(1)  # Validate the user (assuming it's the first user)

    # Wrapper methods for NotificationSystem
    def show_notification(self, title, message):
        self.notification_system.show_notification(self, title, message)

    def show_warning(self, title, message):
        self.notification_system.show_warning(self, title, message)

    def show_error(self, title, message):
        self.notification_system.show_error(self, title, message)

    def show_confirmation(self, title, message):
        return self.notification_system.show_confirmation(self, title, message)

