from PySide6.QtCore import QObject, Signal

from carriers.msc import MSCSchedule


class MSCWorker(QObject):

    finished = Signal(list)
    error = Signal(str)

    def __init__(self, pol, pod, container="40HC"):
        super().__init__()

        self.pol = pol
        self.pod = pod
        self.container = container

    def run(self):
        try:
            engine = MSCSchedule()

            results = engine.search_schedule(
                self.pol,
                self.pod,
                self.container
        )

            print(results)          # <-- temporary

            self.finished.emit(results)

        except Exception as e:
            import traceback
            traceback.print_exc()
            print("MSC ERROR:", e)

            self.finished.emit(results)

        except Exception as e:
            self.error.emit(str(e))