from PySide2 import QtWidgets, QtGui, QtCore


class MainWindow(QtWidgets.QMainWindow):
    close_app_sig = QtCore.Signal()

    def __init__(self):
        super(MainWindow, self).__init__(parent=None)
        self.setFixedSize(800, 600)
        self.setWindowTitle("Touch mailer 1.1 beta")
        self._close = False
        self._closing = False

    @QtCore.Slot(int)
    def shutdown(self, exit_code: int):
        if exit_code == 0:
            self._closing = False
            self._close = True
            self.close()

    def closeEvent(self, event: QtGui.QCloseEvent):
        if self._closing:
            event.ignore()
        if self._close:
            event.accept()
        else:
            self._closing = True
            self.close_app_sig.emit()
            event.ignore()
