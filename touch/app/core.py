import touch
import os
from PySide2 import QtCore
from datetime import datetime
from . import scanner


class Core(QtCore.QObject):
    queue_files = []
    files = []
    scanning = False
    sending = False

    def __init__(self):
        super(Core, self).__init__()
        self.scanner = scanner.Scanner()

    @QtCore.Slot()
    def start_scanner(self):
        if not Core.scanning:
            Core.scanning = True
            self.scanner.start()

    @staticmethod
    def get_queue_length() -> int:
        return len(Core.queue_files)
