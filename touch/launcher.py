import touch
from PySide2 import QtCore


class Launcher(QtCore.QObject):
    start_scan_sig = QtCore.Signal()

    def __init__(self):
        super(Launcher, self).__init__()
        self.view = touch.view.View()
        self.app = touch.app.App()
        self.ctl = touch.ctl.Ctl()
        self.ctl.set_app(self.app)
        self.ctl.set_view(self.view)
        self.ctl.started_default()
        self.app_thread = touch.app.Thread()
        self.app_thread.setObjectName("app thread")
        self.app_thread.started.connect(self.app.started)
        self.app.quit_app_sig.connect(self.app_thread.quit)
        self.app.moveToThread(self.app_thread)
        self.app_thread.start()
        self.app_thread.finished.connect(self.ctl.app_closed)
        self.app.started_sig.connect(self.ctl.started_app)
        touch.util.log_current_thread("launcher")
