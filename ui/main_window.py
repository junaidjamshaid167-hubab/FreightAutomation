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
from ui.dashboard import DashboardPage
from ui.msc_schedule import MSCSchedulePage


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Freight Automation Suite v0.1")
        self.resize(1400,800)

        root = QWidget()

        layout = QHBoxLayout(root)

        self.menu = QListWidget()

        self.menu.addItem("🏠 Dashboard")
        self.menu.addItem("📦 QICT Container Tracking")
        self.menu.addItem("🚢 MSC Schedule Search")

        self.stack = QStackedWidget()

        self.stack.addWidget(DashboardPage())      # Index 0
        self.stack.addWidget(TrackingPage())       # Index 1
        self.stack.addWidget(MSCSchedulePage())    # Index 2

        self.menu.currentRowChanged.connect(self.stack.setCurrentIndex)

        self.menu.setFixedWidth(220)

        layout.addWidget(self.menu)
        layout.addWidget(self.stack)

        self.setCentralWidget(root)

        self.setStatusBar(QStatusBar())

        self.statusBar().showMessage("Ready")

        self.menu.setCurrentRow(0)