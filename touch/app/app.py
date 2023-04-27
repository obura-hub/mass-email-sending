import touch
from PySide2 import QtCore
from . import core
from . import mail
from . import net
from . import scanner



class App(QtCore.QObject):
    quit_app_sig = QtCore.Signal()
    close_app_sig = QtCore.Signal(int)
    close_net_sig = QtCore.Signal()
    started_sig = QtCore.Signal()
    core: core.Core
    net_thread: QtCore.QThread
    net: net.Net
    scanner: scanner.Scanner

    def __init__(self):
        super(App, self).__init__()

    @QtCore.Slot()
    def started(self):
        touch.util.log_current_thread("app")
        self.core = core.Core()
        self.net = net.Net()
        self.net_thread = QtCore.QThread()
        self.net_thread.setObjectName("net thread")
        self.net_thread.started.connect(self.net.started)
        self.net_thread.finished.connect(self.net_finished)
        self.net_thread.finished.connect(self.net.deleteLater)
        self.net.quit_net_sig.connect(self.net_thread.quit)
        self.close_net_sig.connect(self.net.shutdown)
        self.net.moveToThread(self.net_thread)
        self.started_sig.emit()

    @QtCore.Slot()
    def start_scan(self):
        touch.util.log.info('app start scan')
        self.core.start_scanner()

    @QtCore.Slot()
    def shutdown(self):
        touch.util.log.debug("net shutdown")
        self.close_net_sig.emit()

    @QtCore.Slot()
    def net_finished(self):
        touch.util.log.debug("net finished")
        self.close_app_sig.emit(0)
