from PySide6.QtWidgets import QWidget,QVBoxLayout,QLabel

class SchedulePage(QWidget):

    def __init__(self):

        super().__init__()

        layout=QVBoxLayout()

        layout.addWidget(QLabel("MSC Schedule Search"))

        self.setLayout(layout)