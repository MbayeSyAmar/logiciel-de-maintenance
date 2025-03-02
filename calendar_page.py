from PyQt5.QtWidgets import QWidget, QVBoxLayout, QCalendarWidget, QListWidget, QPushButton, QDialog, QFormLayout, QLineEdit, QDateTimeEdit, QTextEdit
from PyQt5.QtCore import QDate, QDateTime

class CalendarPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout(self)

        self.calendar = QCalendarWidget()
        self.calendar.selectionChanged.connect(self.update_events)

        self.event_list = QListWidget()

        add_event_button = QPushButton("Add Event")
        add_event_button.clicked.connect(self.show_add_event_dialog)

        layout.addWidget(self.calendar)
        layout.addWidget(self.event_list)
        layout.addWidget(add_event_button)

        self.update_events()

    def update_events(self):
        selected_date = self.calendar.selectedDate().toString("yyyy-MM-dd")
        events = self.main_window.db.get_calendar_events(selected_date, selected_date)
        self.event_list.clear()
        for event in events:
            self.event_list.addItem(f"{event[1]} - {event[2]} to {event[3]}")

    def show_add_event_dialog(self):
        dialog = AddEventDialog(self.main_window)
        if dialog.exec_() == QDialog.Accepted:
            self.update_events()

class AddEventDialog(QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Add Event")
        layout = QFormLayout(self)

        self.title_input = QLineEdit()
        self.start_date_input = QDateTimeEdit(QDateTime.currentDateTime())
        self.end_date_input = QDateTimeEdit(QDateTime.currentDateTime())
        self.description_input = QTextEdit()
        self.event_type_input = QLineEdit()

        submit_button = QPushButton("Add Event")
        submit_button.clicked.connect(self.add_event)

        layout.addRow("Title:", self.title_input)
        layout.addRow("Start Date:", self.start_date_input)
        layout.addRow("End Date:", self.end_date_input)
        layout.addRow("Description:", self.description_input)
        layout.addRow("Event Type:", self.event_type_input)
        layout.addRow(submit_button)

    def add_event(self):
        title = self.title_input.text()
        start_date = self.start_date_input.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        end_date = self.end_date_input.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        description = self.description_input.toPlainText()
        event_type = self.event_type_input.text()

        self.main_window.db.add_calendar_event(title, start_date, end_date, description, event_type)
        self.accept()