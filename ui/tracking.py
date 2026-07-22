from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QFileDialog,
    QProgressBar,
    QTextEdit
)


class TrackingPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.fileLabel = QLabel("No Excel Selected")

        browse = QPushButton("Browse Excel")

        self.progress = QProgressBar()

        self.log = QTextEdit()

        self.log.setReadOnly(True)

        start = QPushButton("Start Tracking")

        browse.clicked.connect(self.browse)

        layout.addWidget(self.fileLabel)
        layout.addWidget(browse)
        layout.addWidget(self.progress)
        layout.addWidget(self.log)
        layout.addWidget(start)

        self.setLayout(layout)

    def browse(self):

        file,_ = QFileDialog.getOpenFileName(
            self,
            "Select Excel",
            "",
            "Excel Files (*.xlsx)"
        )

        if file:
            self.fileLabel.setText(file)