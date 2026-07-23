from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
)


class MSCSchedulePage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        title = QLabel("🚢 MSC Schedule Search")
        title.setStyleSheet("""
            font-size:22px;
            font-weight:bold;
            color:#1565C0;
        """)

        layout.addWidget(title)

        # POL
        pol_layout = QHBoxLayout()

        pol_layout.addWidget(QLabel("Port of Loading"))

        self.pol = QComboBox()

        self.pol.addItems([
            "Karachi",
            "Port Qasim"
        ])

        pol_layout.addWidget(self.pol)

        layout.addLayout(pol_layout)

        # POD
        pod_layout = QHBoxLayout()

        pod_layout.addWidget(QLabel("Port of Discharge"))

        self.pod = QComboBox()

        self.pod.addItems([
            "Jebel Ali",
            "Singapore",
            "Hamburg",
            "Rotterdam"
        ])

        pod_layout.addWidget(self.pod)

        layout.addLayout(pod_layout)

        # Search Button

        self.search = QPushButton("SEARCH")

        layout.addWidget(self.search)

        # Results Table

        self.table = QTableWidget()

        self.table.setColumnCount(4)

        self.table.setHorizontalHeaderLabels([
            "Vessel",
            "Voyage",
            "ETD",
            "ETA"
        ])

        layout.addWidget(self.table)

        self.setLayout(layout)