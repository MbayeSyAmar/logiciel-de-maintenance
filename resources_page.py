from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QDialog, QFormLayout, QLineEdit, QComboBox

class ResourcesPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout(self)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Name", "Type", "Status", "Location", "Actions"])

        add_resource_button = QPushButton("Add Resource")
        add_resource_button.clicked.connect(self.show_add_resource_dialog)

        layout.addWidget(self.table)
        layout.addWidget(add_resource_button)

        self.update_table()

    def update_table(self):
        self.table.setRowCount(0)
        resources = self.main_window.db.get_resources()
        for resource in resources:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            
            self.table.setItem(row_position, 0, QTableWidgetItem(resource[1]))
            self.table.setItem(row_position, 1, QTableWidgetItem(resource[2]))
            self.table.setItem(row_position, 2, QTableWidgetItem(resource[3]))
            self.table.setItem(row_position, 3, QTableWidgetItem(resource[4]))

            edit_button = QPushButton("Edit")
            edit_button.clicked.connect(lambda _, r=resource: self.edit_resource(r))
            self.table.setCellWidget(row_position, 4, edit_button)

    def show_add_resource_dialog(self):
        dialog = AddResourceDialog(self.main_window)
        if dialog.exec_() == QDialog.Accepted:
            self.update_table()

    def edit_resource(self, resource):
        dialog = EditResourceDialog(self.main_window, resource)
        if dialog.exec_() == QDialog.Accepted:
            self.update_table()

class AddResourceDialog(QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Add Resource")
        layout = QFormLayout(self)

        self.name_input = QLineEdit()
        self.type_input = QComboBox()
        self.type_input.addItems(["Equipment", "Tool", "Vehicle", "Other"])
        self.status_input = QComboBox()
        self.status_input.addItems(["Available", "In Use", "Maintenance", "Out of Service"])
        self.location_input = QLineEdit()

        submit_button = QPushButton("Add Resource")
        submit_button.clicked.connect(self.add_resource)

        layout.addRow("Name:", self.name_input)
        layout.addRow("Type:", self.type_input)
        layout.addRow("Status:", self.status_input)
        layout.addRow("Location:", self.location_input)
        layout.addRow(submit_button)

    def add_resource(self):
        name = self.name_input.text()
        resource_type = self.type_input.currentText()
        status = self.status_input.currentText()
        location = self.location_input.text()

        self.main_window.db.add_resource(name, resource_type, status, location)
        self.accept()

class EditResourceDialog(QDialog):
    def __init__(self, main_window, resource):
        super().__init__()
        self.main_window = main_window
        self.resource = resource
        self.setWindowTitle("Edit Resource")
        layout = QFormLayout(self)

        self.name_input = QLineEdit(resource[1])
        self.type_input = QComboBox()
        self.type_input.addItems(["Equipment", "Tool", "Vehicle", "Other"])
        self.type_input.setCurrentText(resource[2])
        self.status_input = QComboBox()
        self.status_input.addItems(["Available", "In Use", "Maintenance", "Out of Service"])
        self.status_input.setCurrentText(resource[3])
        self.location_input = QLineEdit(resource[4])

        submit_button = QPushButton("Update Resource")
        submit_button.clicked.connect(self.update_resource)

        layout.addRow("Name:", self.name_input)
        layout.addRow("Type:", self.type_input)
        layout.addRow("Status:", self.status_input)
        layout.addRow("Location:", self.location_input)
        layout.addRow(submit_button)

    def update_resource(self):
        name = self.name_input.text()
        resource_type = self.type_input.currentText()
        status = self.status_input.currentText()
        location = self.location_input.text()

        self.main_window.db.cursor.execute('''
        UPDATE resources 
        SET name = ?, type = ?, status = ?, location = ?
        WHERE id = ?
        ''', (name, resource_type, status, location, self.resource[0]))
        self.main_window.db.conn.commit()
        self.accept()