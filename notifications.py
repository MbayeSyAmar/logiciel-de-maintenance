from PyQt5.QtWidgets import QMessageBox

class NotificationSystem:
    @staticmethod
    def show_notification(parent, title, message):
        QMessageBox.information(parent, title, message)

    @staticmethod
    def show_warning(parent, title, message):
        QMessageBox.warning(parent, title, message)

    @staticmethod
    def show_error(parent, title, message):
        QMessageBox.critical(parent, title, message)

    @staticmethod
    def show_confirmation(parent, title, message):
        return QMessageBox.question(parent, title, message, 
                                    QMessageBox.Yes | QMessageBox.No, 
                                    QMessageBox.No) == QMessageBox.Yes