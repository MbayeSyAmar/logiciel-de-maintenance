from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QDialog, QFormLayout, QLineEdit, QSpinBox

class InventoryPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout(self)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Item Name", "Quantity", "Unit", "Reorder Level", "Actions"])

        add_item_button = QPushButton("Add Inventory Item")
        add_item_button.clicked.connect(self.show_add_item_dialog)

        layout.addWidget(self.table)
        layout.addWidget(add_item_button)

        self.update_table()

    def update_table(self):
        self.table.setRowCount(0)
        inventory_items = self.main_window.db.get_inventory()
        for item in inventory_items:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            
            self.table.setItem(row_position, 0, QTableWidgetItem(item[1]))
            self.table.setItem(row_position, 1, QTableWidgetItem(str(item[2])))
            self.table.setItem(row_position, 2, QTableWidgetItem(item[3]))
            self.table.setItem(row_position, 3, QTableWidgetItem(str(item[4])))

            edit_button = QPushButton("Edit")
            edit_button.clicked.connect(lambda _, i=item: self.edit_item(i))
            self.table.setCellWidget(row_position, 4, edit_button)

    def show_add_item_dialog(self):
        dialog = AddInventoryItemDialog(self.main_window)
        if dialog.exec_() == QDialog.Accepted:
            self.update_table()

    def edit_item(self, item):
        dialog = EditInventoryItemDialog(self.main_window, item)
        if dialog.exec_() == QDialog.Accepted:
            self.update_table()

class AddInventoryItemDialog(QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Add Inventory Item")
        layout = QFormLayout(self)

        self.name_input = QLineEdit()
        self.quantity_input = QSpinBox()
        self.quantity_input.setRange(0, 1000000)
        self.unit_input = QLineEdit()
        self.reorder_level_input = QSpinBox()
        self.reorder_level_input.setRange(0, 1000000)

        submit_button = QPushButton("Add Item")
        submit_button.clicked.connect(self.add_item)

        layout.addRow("Item Name:", self.name_input)
        layout.addRow("Quantity:", self.quantity_input)
        layout.addRow("Unit:", self.unit_input)
        layout.addRow("Reorder Level:", self.reorder_level_input)
        layout.addRow(submit_button)

    def add_item(self):
        name = self.name_input.text()
        quantity = self.quantity_input.value()
        unit = self.unit_input.text()
        reorder_level = self.reorder_level_input.value()

        self.main_window.db.add_inventory_item(name, quantity, unit, reorder_level)
        self.accept()

class EditInventoryItemDialog(QDialog):
    def __init__(self, main_window, item):
        super().__init__()
        self.main_window = main_window
        self.item = item
        self.setWindowTitle("Edit Inventory Item")
        layout = QFormLayout(self)

        self.name_input = QLineEdit(item[1])
        self.quantity_input = QSpinBox()
        self.quantity_input.setRange(0, 1000000)
        self.quantity_input.setValue(item[2])
        self.unit_input = QLineEdit(item[3])
        self.reorder_level_input = QSpinBox()
        self.reorder_level_input.setRange(0, 1000000)
        self.reorder_level_input.setValue(item[4])

        submit_button = QPushButton("Update Item")
        submit_button.clicked.connect(self.update_item)

        layout.addRow("Item Name:", self.name_input)
        layout.addRow("Quantity:", self.quantity_input)
        layout.addRow("Unit:", self.unit_input)
        layout.addRow("Reorder Level:", self.reorder_level_input)
        layout.addRow(submit_button)

    def update_item(self):
        name = self.name_input.text()
        quantity = self.quantity_input.value()
        unit = self.unit_input.text()
        reorder_level = self.reorder_level_input.value()

        self.main_window.db.cursor.execute('''
        UPDATE inventory 
        SET item_name = ?, quantity = ?, unit = ?, reorder_level = ?
        WHERE id = ?
        ''', (name, quantity, unit, reorder_level, self.item[0]))
        self.main_window.db.conn.commit()
        self.accept()