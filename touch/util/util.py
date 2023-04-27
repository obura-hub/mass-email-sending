import touch
from PySide2 import QtCore


def log_current_thread(name: str):
    touch.util.log.debug("{} => thread name - {}".format(name, QtCore.QThread.currentThread().objectName()))


def name_current_thread(name: str):
    QtCore.QThread.currentThread().setObjectName(name)
