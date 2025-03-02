from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHeaderView, QDialog, QFormLayout, QLineEdit, QComboBox

class UsersPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout(self)
        
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Username", "Role", "Validated", "Actions"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        add_user_button = QPushButton("Add User")
        add_user_button.clicked.connect(self.show_add_user_form)
        
        layout.addWidget(self.table)
        layout.addWidget(add_user_button)

        self.update_table()

    def update_table(self):
        self.table.setRowCount(0)
        users = self.main_window.db.get_users()
        
        for user in users:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            
            self.table.setItem(row_position, 0, QTableWidgetItem(user[1]))
            self.table.setItem(row_position, 1, QTableWidgetItem(user[2]))
            self.table.setItem(row_position, 2, QTableWidgetItem("Yes" if user[3] else "No"))
            
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            if not user[3]:
                validate_button = QPushButton("Validate")
                validate_button.clicked.connect(lambda _, u=user: self.validate_user(u))
                actions_layout.addWidget(validate_button)
            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(lambda _, u=user: self.delete_user(u))
            actions_layout.addWidget(delete_button)
            self.table.setCellWidget(row_position, 3, actions_widget)

    def show_add_user_form(self):
        form = AddUserForm(self.main_window)
        if form.exec_() == QDialog.Accepted:
            self.update_table()

    def validate_user(self, user):
        self.main_window.db.validate_user(user[0])
        self.update_table()

    def delete_user(self, user):
        reply = self.main_window.show_confirmation(
            "Delete User", 
            f"Are you sure you want to delete user {user[1]}?"
        )
        if reply:
            self.main_window.db.cursor.execute("DELETE FROM users WHERE id = ?", (user[0],))
            self.main_window.db.conn.commit()
            self.update_table()

class AddUserForm(QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Add User")
        self.setGeometry(200, 200, 400, 250)
        
        layout = QFormLayout(self)
        
        self.username_input = QLineEdit()
        layout.addRow("Username:", self.username_input)
        
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addRow("Password:", self.password_input)
        
        self.role_input = QComboBox()
        self.role_input.addItems(["User", "Admin", "Super Admin"])
        layout.addRow("Role:", self.role_input)
        
        submit_button = QPushButton("Add User")
        submit_button.clicked.connect(self.add_user)
        layout.addRow(submit_button)

    def add_user(self):
        username = self.username_input.text()
        password = self.password_input.text()
        role = self.role_input.currentText()
        
        if not all([username, password]):
            self.main_window.show_error("Invalid Input", "Username and password are required.")
            return
        
        if self.main_window.db.add_user(username, password, role):
            self.accept()
        else:
            self.main_window.show_error("Error", "Username already exists.")