from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel

class DashboardPage(QWidget):

    def __init__(self):

        super().__init__()

        layout=QVBoxLayout()

        title=QLabel("Freight Automation Suite")

        title.setStyleSheet("""
        font-size:28px;
        font-weight:bold;
        """)

        layout.addWidget(title)

        layout.addWidget(QLabel("Welcome."))

        self.setLayout(layout)  