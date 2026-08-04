import os
from datetime import datetime

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

from workers.sapt_worker import SAPTWorker


class SAPTPage(QWidget):

    def __init__(self):
        super().__init__()

        self.input_file = ""
        self.output_file = ""

        self.thread = None
        self.worker = None

        # ==================================================
        # MAIN LAYOUT
        # ==================================================

        layout = QVBoxLayout()

        # ==================================================
        # TITLE
        # ==================================================

        title = QLabel("🚢 SAPT Container Tracking")

        title.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
            color:#1565C0;
        """)

        layout.addWidget(title)

        # ==================================================
        # INPUT EXCEL
        # ==================================================

        input_layout = QHBoxLayout()

        self.fileLabel = QLabel("No Excel Selected")

        browse = QPushButton("Browse Excel")
        browse.clicked.connect(self.browse)

        input_layout.addWidget(self.fileLabel)
        input_layout.addWidget(browse)

        # ==================================================
        # OUTPUT EXCEL
        # ==================================================

        output_layout = QHBoxLayout()

        self.outputLabel = QLabel(
            "Output : output\\container_status.xlsx"
        )

        browseOutput = QPushButton("Browse Output")
        browseOutput.clicked.connect(self.select_output)

        output_layout.addWidget(self.outputLabel)
        output_layout.addWidget(browseOutput)

        # ==================================================
        # FILE GROUP
        # ==================================================

        filesGroup = QGroupBox("Files")

        filesLayout = QVBoxLayout()

        filesLayout.addLayout(input_layout)
        filesLayout.addLayout(output_layout)

        filesGroup.setLayout(filesLayout)

        layout.addWidget(filesGroup)

        # ==================================================
        # PROGRESS
        # ==================================================

        self.progress = QProgressBar()

        self.progress.setMinimum(0)
        self.progress.setMaximum(100)
        self.progress.setValue(0)
        self.progress.setFormat("%p% Complete")

        layout.addWidget(self.progress)

        # ==================================================
        # STATUS
        # ==================================================

        self.statusLabel = QLabel("Status : Ready")

        self.statusLabel.setStyleSheet("""
            font-weight:bold;
            color:#1565C0;
        """)

        layout.addWidget(self.statusLabel)

        # ==================================================
        # LOG
        # ==================================================

        self.log = QTextEdit()

        self.log.setReadOnly(True)

        self.log.setPlaceholderText(
            "Container activity will appear here..."
        )

        layout.addWidget(self.log)

        # ==================================================
        # BUTTONS
        # ==================================================

        buttonLayout = QHBoxLayout()

        self.start = QPushButton("START SAPT")

        self.start.clicked.connect(
            self.start_sapt
        )

        self.stop = QPushButton("STOP")

        self.stop.clicked.connect(
            self.stop_tracking
        )

        self.stop.setEnabled(False)

        buttonLayout.addWidget(self.start)
        buttonLayout.addWidget(self.stop)

        layout.addLayout(buttonLayout)

        self.setLayout(layout)

    # ======================================================
    # BROWSE INPUT
    # ======================================================

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

            self.add_log(
                f"Input Excel selected: {file}"
            )

    # ======================================================
    # BROWSE OUTPUT
    # ======================================================

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

            self.add_log(
                f"Output Excel selected: {file}"
            )

    # ======================================================
    # START SAPT WORKER
    # ======================================================

    def start_sapt(self):

        if not self.input_file:

            QMessageBox.warning(
                self,
                "SAPT",
                "Please select an Excel file first."
            )

            return

        if not self.output_file:

            self.output_file = os.path.join(
                os.path.dirname(self.input_file),
                "container_status.xlsx"
            )

            self.outputLabel.setText(
                self.output_file
            )

        self.progress.setValue(0)

        self.log.clear()

        self.statusLabel.setText(
            "Status : Starting SAPT..."
        )

        self.add_log(
            "Starting SAPT worker..."
        )

        # --------------------------------------------------
        # THREAD
        # --------------------------------------------------

        self.thread = QThread()

        # --------------------------------------------------
        # WORKER
        # --------------------------------------------------

        self.worker = SAPTWorker(
            self.input_file,
            self.output_file
        )

        # Move worker to background thread
        self.worker.moveToThread(
            self.thread
        )

        # --------------------------------------------------
        # CONNECTIONS
        # --------------------------------------------------

        self.thread.started.connect(
            self.worker.run
        )

        self.worker.progress.connect(
            self.progress.setValue
        )

        self.worker.log.connect(
            self.add_log
        )

        self.worker.finished.connect(
            self.sapt_finished
        )

        self.worker.error.connect(
            self.sapt_error
        )

        # Worker finished/error → stop thread
        self.worker.finished.connect(
            self.thread.quit
        )

        self.worker.error.connect(
            self.thread.quit
        )

        # Cleanup
        self.thread.finished.connect(
            self.worker.deleteLater
        )

        self.thread.finished.connect(
            self.thread.deleteLater
        )

        # --------------------------------------------------
        # BUTTON STATE
        # --------------------------------------------------

        self.start.setEnabled(False)

        self.stop.setEnabled(True)

        # --------------------------------------------------
        # START
        # --------------------------------------------------

        self.thread.start()

    # ======================================================
    # LOG
    # ======================================================

    def add_log(self, text):

        current_time = datetime.now().strftime(
            "%H:%M:%S"
        )

        self.statusLabel.setText(
            f"Status : {text}"
        )

        self.log.append(
            f"[{current_time}] {text}"
        )

    # ======================================================
    # SAPT FINISHED
    # ======================================================

    def sapt_finished(self, message):

        self.progress.setValue(100)

        self.start.setEnabled(True)

        self.stop.setEnabled(False)

        self.add_log(
            message
        )

        QMessageBox.information(
            self,
            "SAPT",
            message
        )

        self.thread = None
        self.worker = None

    # ======================================================
    # SAPT ERROR
    # ======================================================

    def sapt_error(self, message):

        self.start.setEnabled(True)

        self.stop.setEnabled(False)

        self.add_log(
            message
        )

        QMessageBox.critical(
            self,
            "SAPT Error",
            message
        )

        self.thread = None
        self.worker = None

    # ======================================================
    # STOP
    # ======================================================

    def stop_tracking(self):

        if self.thread is not None:

            self.add_log(
                "Stopping SAPT worker..."
            )

            self.thread.quit()

            self.stop.setEnabled(False)

            self.start.setEnabled(True)