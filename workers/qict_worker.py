from PySide6.QtCore import QObject, Signal

from terminals.qict import process_excel


class QICTWorker(QObject):

    progress = Signal(int)
    log = Signal(str)
    finished = Signal()

    def __init__(self, input_file, output_file):
        super().__init__()

        self.input_file = input_file
        self.output_file = output_file

    def run(self):

        process_excel(
            self.input_file,
            self.output_file,
            progress_callback=self.progress.emit,
            log_callback=self.log.emit
        )

        self.finished.emit()