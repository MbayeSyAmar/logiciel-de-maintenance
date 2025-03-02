from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QDialog, QFormLayout, QLineEdit, QComboBox, QDateEdit, QTextEdit

class WorkOrdersPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout(self)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["Title", "Description", "Status", "Priority", "Assigned To", "Due Date", "Actions"])

        add_work_order_button = QPushButton("Add Work Order")
        add_work_order_button.clicked.connect(self.show_add_work_order_dialog)

        layout.addWidget(self.table)
        layout.addWidget(add_work_order_button)

        self.update_table()

    def update_table(self):
        self.table.setRowCount(0)
        work_orders = self.main_window.db.get_work_orders()
        for work_order in work_orders:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            
            self.table.setItem(row_position, 0, QTableWidgetItem(work_order[1]))
            self.table.setItem(row_position, 1, QTableWidgetItem(work_order[2]))
            self.table.setItem(row_position, 2, QTableWidgetItem(work_order[3]))
            self.table.setItem(row_position, 3, QTableWidgetItem(work_order[4]))
            assigned_to = self.main_window.db.get_users(work_order[5])[0] if work_order[5] else "Unassigned"
            self.table.setItem(row_position, 4, QTableWidgetItem(assigned_to[1] if isinstance(assigned_to, tuple) else assigned_to))
            self.table.setItem(row_position, 5, QTableWidgetItem(work_order[6]))

            edit_button = QPushButton("Edit")
            edit_button.clicked.connect(lambda _, wo=work_order: self.edit_work_order(wo))
            self.table.setCellWidget(row_position, 6, edit_button)

    def show_add_work_order_dialog(self):
        dialog = AddWorkOrderDialog(self.main_window)
        if dialog.exec_() == QDialog.Accepted:
            self.update_table()

    def edit_work_order(self, work_order):
        dialog = EditWorkOrderDialog(self.main_window, work_order)
        if dialog.exec_() == QDialog.Accepted:
            self.update_table()

class AddWorkOrderDialog(QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Add Work Order")
        layout = QFormLayout(self)

        self.title_input = QLineEdit()
        self.description_input = QTextEdit()
        self.status_input = QComboBox()
        self.status_input.addItems(["Open", "In Progress", "Completed", "On Hold"])
        self.priority_input = QComboBox()
        self.priority_input.addItems(["Low", "Medium", "High", "Critical"])
        self.assigned_to_input = QComboBox()
        users = self.main_window.db.get_users()
        self.assigned_to_input.addItem("Unassigned", None)
        for user in users:
            self.assigned_to_input.addItem(user[1], user[0])
        self.due_date_input = QDateEdit()

        submit_button = QPushButton("Add Work Order")
        submit_button.clicked.connect(self.add_work_order)

        layout.addRow("Title:", self.title_input)
        layout.addRow("Description:", self.description_input)
        layout.addRow("Status:", self.status_input)
        layout.addRow("Priority:", self.priority_input)
        layout.addRow("Assigned To:", self.assigned_to_input)
        layout.addRow("Due Date:", self.due_date_input)
        layout.addRow(submit_button)

    def add_work_order(self):
        title = self.title_input.text()
        description = self.description_input.toPlainText()
        status = self.status_input.currentText()
        priority = self.priority_input.currentText()
        assigned_to = self.assigned_to_input.currentData()
        due_date = self.due_date_input.date().toString("yyyy-MM-dd")

        self.main_window.db.add_work_order(title, description, status, priority, assigned_to, due_date)
        self.accept()

class EditWorkOrderDialog(QDialog):
    def __init__(self, main_window, work_order):
        super().__init__()
        self.main_window = main_window
        self.work_order = work_order
        self.setWindowTitle("Edit Work Order")
        layout = QFormLayout(self)

        self.title_input = QLineEdit(work_order[1])
        self.description_input = QTextEdit(work_order[2])
        self.status_input = QComboBox()
        self.status_input.addItems(["Open", "In Progress", "Completed", "On Hold"])
        self.status_input.setCurrentText(work_order[3])
        self.priority_input = QComboBox()
        self.priority_input.addItems(["Low", "Medium", "High", "Critical"])
        self.priority_input.setCurrentText(work_order[4])
        self.assigned_to_input = QComboBox()
        users = self.main_window.db.get_users()
        self.assigned_to_input.addItem("Unassigned", None)
        for user in users:
            self.assigned_to_input.addItem(user[1], user[0])
        self.assigned_to_input.setCurrentIndex(self.assigned_to_input.findData(work_order[5]))
        self.due_date_input = QDateEdit()
        self.due_date_input.setDate(QDate.fromString(work_order[6], "yyyy-MM-dd"))

        submit_button = QPushButton("Update Work Order")
        submit_button.clicked.connect(self.update_work_order)

        layout.addRow("Title:", self.title_input)
        layout.addRow("Description:", self.description_input)
        layout.addRow("Status:", self.status_input)
        layout.addRow("Priority:", self.priority_input)
        layout.addRow("Assigned To:", self.assigned_to_input)
        layout.addRow("Due Date:", self.due_date_input)
        layout.addRow(submit_button)

    def update_work_order(self):
        title = self.title_input.text()
        description = self.description_input.toPlainText()
        status = self.status_input.currentText()
        priority = self.priority_input.currentText()
        assigned_to = self.assigned_to_input.currentData()
        due_date = self.due_date_input.date().toString("yyyy-MM-dd")

        self.main_window.db.cursor.execute('''
        UPDATE work_orders 
        SET title = ?, description = ?, status = ?, priority = ?, assigned_to = ?, due_date = ?
        WHERE id = ?
        ''', (title, description, status, priority, assigned_to, due_date, self.work_order[0]))
        self.main_window.db.conn.commit()
        self.accept()