from PySide2 import QtCore


class Thread(QtCore.QThread):
    def __init__(self):
        super(Thread, self).__init__()
