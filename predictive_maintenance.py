import random
from datetime import datetime, timedelta

class PredictiveMaintenance:
    @staticmethod
    def predict_next_maintenance(machine):
        # This is a simplified prediction model. In a real-world scenario,
        # you would use more sophisticated algorithms and historical data.
        last_maintenance = datetime.strptime(machine[6], '%Y-%m-%d') if machine[6] else datetime.strptime(machine[4], '%Y-%m-%d')
        days_since_last_maintenance = (datetime.now() - last_maintenance).days
        maintenance_frequency = machine[5]

        # Add some randomness to simulate wear and tear
        wear_factor = random.uniform(0.8, 1.2)
        predicted_days = int(maintenance_frequency * wear_factor)

        if days_since_last_maintenance >= predicted_days:
            return "Maintenance Required"
        elif days_since_last_maintenance >= predicted_days * 0.8:
            return "Maintenance Due Soon"
        else:
            return "OK"

    @staticmethod
    def estimate_remaining_life(machine):
        # This is a simplified estimation. In a real-world scenario,
        # you would use more sophisticated algorithms and sensor data.
        last_maintenance = datetime.strptime(machine[6], '%Y-%m-%d') if machine[6] else datetime.strptime(machine[4], '%Y-%m-%d')
        days_since_last_maintenance = (datetime.now() - last_maintenance).days
        maintenance_frequency = machine[5]

        # Estimate remaining life based on maintenance frequency and a random factor
        wear_factor = random.uniform(0.8, 1.2)
        estimated_life = int(maintenance_frequency * wear_factor)
        remaining_life = estimated_life - days_since_last_maintenance

        if remaining_life <= 0:
            return "Immediate Maintenance Required"
        elif remaining_life <= estimated_life * 0.2:
            return f"Critical: {remaining_life} days remaining"
        elif remaining_life <= estimated_life * 0.5:
            return f"Warning: {remaining_life} days remaining"
        else:
            return f"Good: {remaining_life} days remaining"

This completes the `PredictiveMaintenance` class in the `utils/predictive_maintenance.py` file. The class now includes two static methods: `predict_next_maintenance` and `estimate_remaining_life`, which provide basic predictive maintenance functionality for the machines in the system.

To integrate these predictive maintenance features into the main application, you would typically call these methods from the `MachinesPage` or a dedicated predictive maintenance page. For example, you could add a "Predict Maintenance" button to each machine in the machines table, which would call these methods and display the results to the user.

Here's an example of how you might modify the `MachinesPage` to include predictive maintenance information:

```python project="Advanced Dashboard" file="ui/machines_page.py" type="code"
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout
from utils.predictive_maintenance import PredictiveMaintenance

class MachinesPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout(self)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["Name", "Type", "Status", "Next Maintenance", "Location", "Predicted Status", "Actions"])

        add_machine_button = QPushButton("Add Machine")
        add_machine_button.clicked.connect(self.show_add_machine_dialog)

        layout.addWidget(self.table)
        layout.addWidget(add_machine_button)

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

            predicted_status = PredictiveMaintenance.predict_next_maintenance(machine)
            self.table.setItem(row_position, 5, QTableWidgetItem(predicted_status))
            
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            edit_button = QPushButton("Edit")
            edit_button.clicked.connect(lambda _, m=machine: self.edit_machine(m))
            actions_layout.addWidget(edit_button)
            predict_button = QPushButton("Predict Life")
            predict_button.clicked.connect(lambda _, m=machine: self.predict_machine_life(m))
            actions_layout.addWidget(predict_button)
            self.table.setCellWidget(row_position, 6, actions_widget)

    def predict_machine_life(self, machine):
        remaining_life = PredictiveMaintenance.estimate_remaining_life(machine)
        self.main_window.notification_system.show_notification(
            self, 
            "Machine Life Prediction", 
            f"Machine: {machine[1]}\nPredicted Remaining Life: {remaining_life}"
        )

    # ... (rest of the MachinesPage class remains the same)