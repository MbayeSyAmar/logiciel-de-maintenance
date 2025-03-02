from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHeaderView, QHBoxLayout, QDialog, QFormLayout, QLineEdit, QDateEdit, QComboBox, QSpinBox
from PyQt5.QtCore import QDate
from datetime import datetime, timedelta

class MachinesPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout(self)
        
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Name", "Type", "Status", "Next Maintenance", "Location", "Actions"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        add_button = QPushButton("Add Machine")
        add_button.clicked.connect(self.show_add_machine_form)
        
        layout.addWidget(self.table)
        layout.addWidget(add_button)

        self.update_table()

    def update_table(self):
        self.table.setRowCount(0)
        machines = self.main_window.db.get_machines()
        
        for machine in machines:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            
            self.table.setItem(row_position, 0, QTableWidgetItem(machine[1]))
            self.table.setItem(row_position, 1, QTableWidgetItem(machine[2]))
            self.table.setItem(row_position, 2, QTableWidgetItem(machine[7]))
            
            next_maintenance = self.calculate_next_maintenance(machine[4], machine[5], machine[6])
            self.table.setItem(row_position, 3, QTableWidgetItem(next_maintenance))
            
            self.table.setItem(row_position, 4, QTableWidgetItem(machine[3]))
            
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            edit_button = QPushButton("Edit")
            edit_button.clicked.connect(lambda _, m=machine: self.edit_machine(m))
            actions_layout.addWidget(edit_button)
            maintenance_button = QPushButton("Log Maintenance")
            maintenance_button.clicked.connect(lambda _, m=machine: self.log_maintenance(m))
            actions_layout.addWidget(maintenance_button)
            self.table.setCellWidget(row_position, 5, actions_widget)

    def calculate_next_maintenance(self, installation_date, frequency, last_maintenance):
        if last_maintenance:
            last_date = datetime.strptime(last_maintenance, '%Y-%m-%d')
        else:
            last_date = datetime.strptime(installation_date, '%Y-%m-%d')
        
        next_date = last_date + timedelta(days=frequency)
        return next_date.strftime('%Y-%m-%d')

    def show_add_machine_form(self):
        form = AddMachineForm(self.main_window)
        if form.exec_() == QDialog.Accepted:
            self.update_table()

    def edit_machine(self, machine):
        form = EditMachineForm(self.main_window, machine)
        if form.exec_() == QDialog.Accepted:
            self.update_table()

    def log_maintenance(self, machine):
        form = LogMaintenanceForm(self.main_window, machine)
        if form.exec_() == QDialog.Accepted:
            self.update_table()

class AddMachineForm(QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Add Machine")
        self.setGeometry(200, 200, 400, 300)
        
        layout = QFormLayout(self)
        
        self.name_input = QLineEdit()
        layout.addRow("Name:", self.name_input)
        
        self.type_input = QComboBox()
        self.type_input.addItems(["Type A", "Type B", "Type C"])
        layout.addRow("Type:", self.type_input)
        
        self.location_input = QLineEdit()
        layout.addRow("Location:", self.location_input)
        
        self.installation_date_input = QDateEdit()
        self.installation_date_input.setDate(QDate.currentDate())
        layout.addRow("Installation Date:", self.installation_date_input)
        
        self.maintenance_frequency_input = QSpinBox()
        self.maintenance_frequency_input.setRange(1, 365)
        layout.addRow("Maintenance Frequency (days):", self.maintenance_frequency_input)
        
        submit_button = QPushButton("Add Machine")
        submit_button.clicked.connect(self.add_machine)
        layout.addRow(submit_button)

    def add_machine(self):
        name = self.name_input.text()
        machine_type = self.type_input.currentText()
        location = self.location_input.text()
        installation_date = self.installation_date_input.date().toString("yyyy-MM-dd")
        maintenance_frequency = self.maintenance_frequency_input.value()
        
        if not all([name, machine_type, location, installation_date, maintenance_frequency]):
            self.main_window.show_error("Invalid Input", "All fields are required.")
            return
        
        self.main_window.db.add_machine(name, machine_type, location, installation_date, maintenance_frequency)
        self.accept()

class EditMachineForm(QDialog):
    def __init__(self, main_window, machine):
        super().__init__()
        self.main_window = main_window
        self.machine = machine
        self.setWindowTitle("Edit Machine")
        self.setGeometry(200, 200, 400, 300)
        
        layout = QFormLayout(self)
        
        self.name_input = QLineEdit(machine[1])
        layout.addRow("Name:", self.name_input)
        
        self.type_input = QComboBox()
        self.type_input.addItems(["Type A", "Type B", "Type C"])
        self.type_input.setCurrentText(machine[2])
        layout.addRow("Type:", self.type_input)
        
        self.location_input = QLineEdit(machine[3])
        layout.addRow("Location:", self.location_input)
        
        self.installation_date_input = QDateEdit()
        self.installation_date_input.setDate(QDate.fromString(machine[4], "yyyy-MM-dd"))
        layout.addRow("Installation Date:", self.installation_date_input)
        
        self.maintenance_frequency_input = QSpinBox()
        self.maintenance_frequency_input.setRange(1, 365)
        self.maintenance_frequency_input.setValue(machine[5])
        layout.addRow("Maintenance Frequency (days):", self.maintenance_frequency_input)
        
        self.status_input = QComboBox()
        self.status_input.addItems(["Healthy", "Warning", "Critical"])
        self.status_input.setCurrentText(machine[7])
        layout.addRow("Status:", self.status_input)
        
        submit_button = QPushButton("Update Machine")
        submit_button.clicked.connect(self.update_machine)
        layout.addRow(submit_button)

    def update_machine(self):
        name = self.name_input.text()
        machine_type = self.type_input.currentText()
        location = self.location_input.text()
        installation_date = self.installation_date_input.date().toString("yyyy-MM-dd")
        maintenance_frequency = self.maintenance_frequency_input.value()
        status = self.status_input.currentText()
        
        if not all([name, machine_type, location, installation_date, maintenance_frequency]):
            self.main_window.show_error("Invalid Input", "All fields are required.")
            return
        
        self.main_window.db.cursor.execute('''
        UPDATE machines 
        SET name = ?, type = ?, location = ?, installation_date = ?, maintenance_frequency = ?, status = ?
        WHERE id = ?
        ''', (name, machine_type, location, installation_date, maintenance_frequency, status, self.machine[0]))
        self.main_window.db.conn.commit()
        self.accept()

class LogMaintenanceForm(QDialog):
    def __init__(self, main_window, machine):
        super().__init__()
        self.main_window = main_window
        self.machine = machine
        self.setWindowTitle("Log Maintenance")
        self.setGeometry(200, 200, 400, 200)
        
        layout = QFormLayout(self)
        
        self.description_input = QLineEdit()
        layout.addRow("Description:", self.description_input)
        
        submit_button = QPushButton("Log Maintenance")
        submit_button.clicked.connect(self.log_maintenance)
        layout.addRow(submit_button)

    def log_maintenance(self):
        description = self.description_input.text()
        
        if not description:
            self.main_window.show_error("Invalid Input", "Description is required.")
            return
        
        self.main_window.db.add_maintenance(self.machine[0], description)
        self.accept()