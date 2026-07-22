from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QListWidget,
    QStackedWidget,
    QLabel,
    QStatusBar
)

from ui.tracking import TrackingPage
from ui.schedules import SchedulePage
from ui.dashboard import DashboardPage


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Freight Automation Suite v0.1")
        self.resize(1400,800)

        root = QWidget()

        layout = QHBoxLayout(root)

        self.menu = QListWidget()

        self.menu.addItem("🏠 Dashboard")
        self.menu.addItem("📦 Container Tracking")
        self.menu.addItem("🚢 Vessel Schedules")

        self.stack = QStackedWidget()

        self.stack.addWidget(DashboardPage())
        self.stack.addWidget(TrackingPage())
        self.stack.addWidget(SchedulePage())

        self.menu.currentRowChanged.connect(self.stack.setCurrentIndex)

        self.menu.setFixedWidth(220)

        layout.addWidget(self.menu)
        layout.addWidget(self.stack)

        self.setCentralWidget(root)

        self.setStatusBar(QStatusBar())

        self.statusBar().showMessage("Ready")

        self.menu.setCurrentRow(0)