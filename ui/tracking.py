from datetime import datetime
import os

from PySide6.QtCore import QThread
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog,
    QProgressBar,
    QTextEdit,
    QMessageBox,
    QGroupBox,
)

from workers.qict_worker import QICTWorker


class TrackingPage(QWidget):

    def __init__(self):
        super().__init__()

        self.input_file = ""
        self.output_file = ""

        self.thread = None
        self.worker = None

        # ---------------- Main Layout ----------------
        layout = QVBoxLayout()

        title = QLabel("🚢 QICT Container Tracking")

        title.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
            color:#1565C0;
        """)

        layout.addWidget(title)

        # ---------------- Input ----------------

        input_layout = QHBoxLayout()

        self.fileLabel = QLabel("No Excel Selected")

        browse = QPushButton("Browse Excel")
        browse.clicked.connect(self.browse)

        input_layout.addWidget(self.fileLabel)
        input_layout.addWidget(browse)

        # ---------------- Output ----------------

        output_layout = QHBoxLayout()

        self.outputLabel = QLabel(
            "Output : output\\container_status.xlsx"
        )

        browseOutput = QPushButton("Browse Output")
        browseOutput.clicked.connect(self.select_output)

        output_layout.addWidget(self.outputLabel)
        output_layout.addWidget(browseOutput)

        # ---------------- Files Group ----------------

        filesGroup = QGroupBox("Files")

        filesLayout = QVBoxLayout()

        filesLayout.addLayout(input_layout)
        filesLayout.addLayout(output_layout)

        filesGroup.setLayout(filesLayout)

        layout.addWidget(filesGroup)

        # ---------------- Progress ----------------

        self.progress = QProgressBar()
        self.progress.setMinimum(0)
        self.progress.setMaximum(100)
        self.progress.setValue(0)
        self.progress.setFormat("%p% Complete")
        self.progress.setValue(0)

        layout.addWidget(self.progress)

        # ---------------- Status ----------------

        self.statusLabel = QLabel("Status : Ready")

        self.statusLabel.setStyleSheet("""
        font-weight:bold;
        color:#1565C0;
        """)

        layout.addWidget(self.statusLabel)

        # ---------------- Log ----------------

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setPlaceholderText(
        "Container activity will appear here..."
)

        self.log.setReadOnly(True)

        layout.addWidget(self.log)

        # ---------------- Buttons ----------------

        buttonLayout = QHBoxLayout()

        self.start = QPushButton("START")
        self.start.clicked.connect(self.start_tracking)

        self.stop = QPushButton("STOP")
        self.stop.clicked.connect(self.stop_tracking)
        self.stop.setEnabled(False)

        buttonLayout.addWidget(self.start)
        buttonLayout.addWidget(self.stop)

        layout.addLayout(buttonLayout)

        self.setLayout(layout)
       
        # --------------------------------------------------
    # Browse Input Excel
    # --------------------------------------------------

    def browse(self):

        file, _ = QFileDialog.getOpenFileName(
            self,
            "Select Excel File",
            "",
            "Excel Files (*.xlsx)"
        )

        if file:
            self.input_file = file
            self.fileLabel.setText(file)

    # --------------------------------------------------
    # Browse Output Excel
    # --------------------------------------------------

    def select_output(self):

        file, _ = QFileDialog.getSaveFileName(
            self,
            "Save Output File",
            "container_status.xlsx",
            "Excel Files (*.xlsx)"
        )

        if file:
            self.output_file = file
            self.outputLabel.setText(file)

    # --------------------------------------------------
    # START
    # --------------------------------------------------

    def start_tracking(self):

        if not self.input_file:

            QMessageBox.warning(
                self,
                "Error",
                "Please select an Excel file first."
            )
            return

        if not self.output_file:

            self.output_file = os.path.join(
                os.path.dirname(self.input_file),
                "container_status.xlsx"
            )

            self.outputLabel.setText(self.output_file)

        self.progress.setValue(0)

        self.log.clear()

        self.statusLabel.setText("Starting...")

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

        self.thread.finished.connect(self.thread.deleteLater)

        self.start.setEnabled(False)
        self.stop.setEnabled(True)

        self.thread.start()

    def add_log(self, text):
        self.statusLabel.setText(text)
        time = datetime.now().strftime("%H:%M:%S")
        self.log.append(f"[{time}] {text}")

    # --------------------------------------------------
    # STOP
    # --------------------------------------------------

    def stop_tracking(self):

        if self.worker is not None:
            self.worker.stop()

        self.stop.setEnabled(False)

        self.add_log("Stopping...")

    # --------------------------------------------------
    # LOG
    # --------------------------------------------------

    def add_log(self, text):

        self.statusLabel.setText(text)

        current_time = datetime.now().strftime("%H:%M:%S")

        self.log.append(f"[{current_time}] {text}")

    # --------------------------------------------------
    # FINISHED
    # --------------------------------------------------

    def finished(self):

        self.progress.setValue(100)

        self.start.setEnabled(True)
        self.stop.setEnabled(False)

        self.statusLabel.setText("Ready")

        self.add_log("Completed Successfully.")

        QMessageBox.information(
            self,
            "Completed",
            "Container Status Saved Successfully!"
        )

        if self.thread is not None:
            self.thread.quit()
            self.thread.wait()

            self.thread = None

        self.worker = None


    # --------------------------------------------------
    # FINISHED
    # --------------------------------------------------

    def finished(self):

        self.start.setEnabled(True)
        self.stop.setEnabled(False)

        self.statusLabel.setText("Ready")

        self.add_log("Completed Successfully.")

        self.progress.setValue(100)

        if self.thread is not None:

            self.thread.quit()
            self.thread.wait()

            self.thread.deleteLater()

            self.thread = None

        self.worker = None

        QMessageBox.information(
            self,
            "Completed",
            f"Container Status Saved Successfully!\n\n{self.output_file}"
        )