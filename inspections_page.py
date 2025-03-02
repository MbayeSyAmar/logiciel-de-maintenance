from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QDialog, QFormLayout, QLineEdit, QDateEdit, QTextEdit, QComboBox

class InspectionsPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout(self)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Machine", "Date", "Inspector", "Result", "Notes", "Actions"])

        add_inspection_button = QPushButton("Add Inspection")
        add_inspection_button.clicked.connect(self.show_add_inspection_dialog)

        layout.addWidget(self.table)
        layout.addWidget(add_inspection_button)

        self.update_table()

    def update_table(self):
        self.table.setRowCount(0)
        inspections = self.main_window.db.get_inspections()
        for inspection in inspections:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            
            machine = self.main_window.db.get_machines(inspection[1])[0]
            self.table.setItem(row_position, 0, QTableWidgetItem(machine[1]))
            self.table.setItem(row_position, 1, QTableWidgetItem(inspection[2]))
            self.table.setItem(row_position, 2, QTableWidgetItem(inspection[3]))
            self.table.setItem(row_position, 3, QTableWidgetItem(inspection[4]))
            self.table.setItem(row_position, 4, QTableWidgetItem(inspection[5]))

            view_button = QPushButton("View")
            view_button.clicked.connect(lambda _, i=inspection: self.view_inspection(i))
            self.table.setCellWidget(row_position, 5, view_button)

    def show_add_inspection_dialog(self):
        dialog = AddInspectionDialog(self.main_window)
        if dialog.exec_() == QDialog.Accepted:
            self.update_table()

    def view_inspection(self, inspection):
        dialog = ViewInspectionDialog(self.main_window, inspection)
        dialog.exec_()

class AddInspectionDialog(QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Add Inspection")
        layout = QFormLayout(self)

        self.machine_input = QComboBox()
        machines = self.main_window.db.get_machines()
        for machine in machines:
            self.machine_input.addItem(machine[1], machine[0])

        self.date_input = QDateEdit()
        self.inspector_input = QLineEdit()
        self.result_input = QComboBox()
        self.result_input.addItems(["Pass", "Fail", "Needs Attention"])
        self.notes_input = QTextEdit()

        submit_button = QPushButton("Add Inspection")
        submit_button.clicked.connect(self.add_inspection)

        layout.addRow("Machine:", self.machine_input)
        layout.addRow("Date:", self.date_input)
        layout.addRow("Inspector:", self.inspector_input)
        layout.addRow("Result:", self.result_input)
        layout.addRow("Notes:", self.notes_input)
        layout.addRow(submit_button)

    def add_inspection(self):
        machine_id = self.machine_input.currentData()
        date = self.date_input.date().toString("yyyy-MM-dd")
        inspector = self.inspector_input.text()
        result = self.result_input.currentText()
        notes = self.notes_input.toPlainText()

        self.main_window.db.add_inspection(machine_id, date, inspector, result, notes)
        self.accept()

class ViewInspectionDialog(QDialog):
    def __init__(self, main_window, inspection):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("View Inspection")
        layout = QFormLayout(self)

        machine = self.main_window.db.get_machines(inspection[1])[0]
        layout.addRow("Machine:", QLineEdit(machine[1]))
        layout.addRow("Date:", QLineEdit(inspection[2]))
        layout.addRow("Inspector:", QLineEdit(inspection[3]))
        layout.addRow("Result:", QLineEdit(inspection[4]))
        layout.addRow("Notes:", QTextEdit(inspection[5]))

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addRow(close_button)