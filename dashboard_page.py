from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QFrame, QScrollArea, QPushButton, QGraphicsDropShadowEffect)
from PyQt5.QtGui import QFont, QIcon, QColor
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QPieSeries, QBarSeries, QBarSet, QValueAxis, QBarCategoryAxis
import random
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter


class DashboardPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()
        
        # Timer for updating dashboard data
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_dashboard)
        self.update_timer.start(5000)  # Update every 5 seconds

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Header
        header = QLabel("Dashboard")
        header.setObjectName("dashboard-header")
        header.setFont(QFont("Segoe UI", 32, QFont.Bold))
        layout.addWidget(header)
        
        # Scroll area for dashboard content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setObjectName("dashboard-scroll-area")
        layout.addWidget(scroll_area)
        
        # Container for dashboard content
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(20)
        scroll_area.setWidget(container)
        
        # Quick stats
        stats_layout = QHBoxLayout()
        self.total_machines = self.create_stat_widget("Total Machines", "0")
        self.healthy_machines = self.create_stat_widget("Healthy Machines", "0")
        self.machines_in_alert = self.create_stat_widget("Machines in Alert", "0")
        stats_layout.addWidget(self.total_machines)
        stats_layout.addWidget(self.healthy_machines)
        stats_layout.addWidget(self.machines_in_alert)
        container_layout.addLayout(stats_layout)
        
        # Charts
        charts_layout = QHBoxLayout()
        self.machine_status_chart = self.create_pie_chart("Machine Status Distribution")
        self.performance_chart = self.create_line_chart("Machine Performance Over Time")
        charts_layout.addWidget(self.machine_status_chart)
        charts_layout.addWidget(self.performance_chart)
        container_layout.addLayout(charts_layout)
        
        # Recent activities and Maintenance schedule
        bottom_layout = QHBoxLayout()
        self.activities_widget = self.create_activities_widget()
        self.maintenance_widget = self.create_maintenance_widget()
        bottom_layout.addWidget(self.activities_widget)
        bottom_layout.addWidget(self.maintenance_widget)
        container_layout.addLayout(bottom_layout)

    def create_stat_widget(self, label, value):
        widget = QFrame()
        widget.setObjectName("stat-widget")
        layout = QVBoxLayout(widget)
        
        value_label = QLabel(value)
        value_label.setObjectName("stat-value")
        value_label.setAlignment(Qt.AlignCenter)
        
        description = QLabel(label)
        description.setObjectName("stat-description")
        description.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(value_label)
        layout.addWidget(description)
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(0, 0)
        widget.setGraphicsEffect(shadow)
        
        return widget

    def create_pie_chart(self, title):
        series = QPieSeries()
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle(title)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
        
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        chart_view.setMinimumSize(400, 300)
        
        return chart_view

    def create_line_chart(self, title):
        series = QLineSeries()
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle(title)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        
        axis_x = QValueAxis()
        axis_y = QValueAxis()
        chart.addAxis(axis_x, Qt.AlignBottom)
        chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_x)
        series.attachAxis(axis_y)
        
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        chart_view.setMinimumSize(400, 300)
        
        return chart_view

    def create_activities_widget(self):
        widget = QFrame()
        widget.setObjectName("activities-widget")
        layout = QVBoxLayout(widget)
        
        header = QLabel("Recent Activities")
        header.setObjectName("widget-header")
        layout.addWidget(header)
        
        self.activities_list = QVBoxLayout()
        layout.addLayout(self.activities_list)
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(0, 0)
        widget.setGraphicsEffect(shadow)
        
        return widget

    def create_maintenance_widget(self):
        widget = QFrame()
        widget.setObjectName("maintenance-widget")
        layout = QVBoxLayout(widget)
        
        header = QLabel("Upcoming Maintenance")
        header.setObjectName("widget-header")
        layout.addWidget(header)
        
        self.maintenance_list = QVBoxLayout()
        layout.addLayout(self.maintenance_list)
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(0, 0)
        widget.setGraphicsEffect(shadow)
        
        return widget

    def update_dashboard(self):
        # Update quick stats
        machines = self.main_window.db.get_machines()
        total_machines = len(machines)
        healthy_machines = sum(1 for machine in machines if machine[7] == 'Healthy')
        machines_in_alert = total_machines - healthy_machines
        
        self.animate_stat_change(self.total_machines.findChild(QLabel, "stat-value"), total_machines)
        self.animate_stat_change(self.healthy_machines.findChild(QLabel, "stat-value"), healthy_machines)
        self.animate_stat_change(self.machines_in_alert.findChild(QLabel, "stat-value"), machines_in_alert)
        
        # Update pie chart
        pie_series = self.machine_status_chart.chart().series()[0]
        pie_series.clear()
        status_count = {'Healthy': healthy_machines, 'Warning': 0, 'Critical': 0}
        for machine in machines:
            if machine[7] != 'Healthy':
                status_count[machine[7]] += 1
        for status, count in status_count.items():
            slice = pie_series.append(status, count)
            if status == 'Healthy':
                slice.setBrush(QColor("#4CAF50"))
            elif status == 'Warning':
                slice.setBrush(QColor("#FFC107"))
            else:
                slice.setBrush(QColor("#F44336"))
        
        # Update line chart
        line_series = self.performance_chart.chart().series()[0]
        line_series.clear()
        for i in range(10):
            line_series.append(i, random.randint(50, 100))
        
        # Update recent activities
        self.update_activities()
        
        # Update maintenance schedule
        self.update_maintenance_schedule()

    def animate_stat_change(self, label, new_value):
        try:
            old_value = int(label.text())  # Ensure old_value is an integer
        except ValueError:
            old_value = 0  # Fallback to 0 if the label's text is not a valid integer
        
        # Create an animation for the 'text' property
        animation = QPropertyAnimation(label, b"text")
        animation.setDuration(1000)
        animation.setStartValue(str(old_value))  # Start as a string
        animation.setEndValue(str(new_value))   # End as a string
        animation.setEasingCurve(QEasingCurve.OutCubic)

        # Connect the valueChanged signal to update the label text
        animation.valueChanged.connect(lambda value: label.setText(str(int(value))))

        animation.start()
        

    def update_activities(self):
        # Clear existing activities
        for i in reversed(range(self.activities_list.count())): 
            self.activities_list.itemAt(i).widget().setParent(None)
        
        # Add new activities (this is a placeholder, replace with actual data)
        activities = [
            "Machine A001 status changed to Warning",
            "Maintenance performed on Machine B002",
            "New user 'John Doe' added to the system",
            "Inventory low alert for Item X",
            "Work order #123 completed"
        ]
        for activity in activities:
            label = QLabel(activity)
            label.setObjectName("activity-item")
            self.activities_list.addWidget(label)

    def update_maintenance_schedule(self):
        # Clear existing schedule items
        for i in reversed(range(self.maintenance_list.count())): 
            self.maintenance_list.itemAt(i).widget().setParent(None)
        
        # Add new schedule items (this is a placeholder, replace with actual data)
        schedule = [
            ("Machine A001", "2023-06-15"),
            ("Machine B002", "2023-06-18"),
            ("Machine C003", "2023-06-20"),
            ("Machine D004", "2023-06-22"),
            ("Machine E005", "2023-06-25")
        ]
        for machine, date in schedule:
            label = QLabel(f"{machine} - {date}")
            label.setObjectName("maintenance-item")
            self.maintenance_list.addWidget(label)

