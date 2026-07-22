from datetime import datetime
from email.mime import text
import os

from PySide6.QtCore import QThread
from PySide6.QtWidgets import (
    QGroupBox,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog,
    QProgressBar,
    QTextEdit,
    QMessageBox,
)

from workers.qict_worker import QICTWorker

class TrackingPage(QWidget):

    def __init__(self):
        super().__init__()

        self.input_file = ""
        self.output_file = ""

        layout = QVBoxLayout()
        title = QLabel("QICT Container Tracking")
        title.setStyleSheet("""
        font-size:24px;
        font-weight:bold;
        color:#1565C0;
        """)

        layout.addWidget(title)

        # ---------- INPUT ----------
        input_layout = QHBoxLayout()

        self.fileLabel = QLabel("No Excel Selected")

        browse = QPushButton("Browse Excel")
        browse.clicked.connect(self.browse)

        input_layout.addWidget(self.fileLabel)
        input_layout.addWidget(browse)

        # ---------- OUTPUT ----------
        output_layout = QHBoxLayout()

        self.outputLabel = QLabel("Output : output\\container_status.xlsx")

        browseOutput = QPushButton("Browse Output")
        browseOutput.clicked.connect(self.select_output)

        output_layout.addWidget(self.outputLabel)
        output_layout.addWidget(browseOutput)

        # ---------- FILES GROUP ----------
        filesGroup = QGroupBox("Files")
        filesLayout = QVBoxLayout()
        filesLayout.addLayout(input_layout)
        filesLayout.addLayout(output_layout)
        filesGroup.setLayout(filesLayout)

        # ---------- PROGRESS ----------
        self.progress = QProgressBar()
        
        # ---------- STATUS ----------
        self.statusLabel = QLabel("Ready")

        # # ---------- LOG ----------
        self.log = QTextEdit()
        self.log.setReadOnly(True)

        # ---------- BUTTON ----------
        self.start = QPushButton("START")
        self.start.clicked.connect(self.start_tracking)

        layout.addWidget(filesGroup)
        layout.addWidget(self.progress)
        layout.addWidget(self.statusLabel)
        layout.addWidget(self.log)
        layout.addWidget(self.start)

        self.setLayout(layout)
       
    def browse(self):

        file, _ = QFileDialog.getOpenFileName(
            self,
            "Select Excel",
            "",
            "Excel Files (*.xlsx)"
        )

        if file:
            self.input_file = file
            self.fileLabel.setText(file)

    def select_output(self):

        file, _ = QFileDialog.getSaveFileName(
            self,
            "Save Result",
            "container_status.xlsx",
            "Excel Files (*.xlsx)"
        )

        if file:
            self.output_file = file
            self.outputLabel.setText(file)

    def start_tracking(self):
        self.start.setEnabled(False)

        if not self.input_file:

            QMessageBox.warning(
                self,
                "Error",
                "Please select an Excel file."
            )
            return

        if not self.output_file:

            self.output_file = os.path.join(
                os.path.dirname(self.input_file),
                "container_status.xlsx"
            )

        self.thread = QThread()

        self.worker = QICTWorker(
            self.input_file,
            self.output_file
        )

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)

        self.worker.progress.connect(self.progress.setValue)

        self.worker.log.connect(self.add_log)

        self.worker.finished.connect(self.finished)

        self.worker.finished.connect(self.thread.quit)

        self.thread.start()

    def add_log(self, text):
        self.statusLabel.setText(text)
        time = datetime.now().strftime("%H:%M:%S")
        self.log.append(f"[{time}] {text}")

    def finished(self):
        self.start.setEnabled(True)

        self.log.append("Finished Successfully")

        QMessageBox.information(
            self,
            "Completed",
            "Container Status Saved Successfully!"
        )