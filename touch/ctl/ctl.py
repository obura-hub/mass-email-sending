import touch
from PySide2 import QtCore


class Ctl(QtCore.QObject):
    view: touch.view.View
    app: touch.app.App
    app_startup_signal = QtCore.Signal()
    close_code: int

    def __init__(self):
        super(Ctl, self).__init__()

    def set_view(self, view):
        self.view = view

    def set_app(self, app):
        self.app = app

    def started_default(self):
        self.view.main_window.close_app_sig.connect(self.app.shutdown)
        self.app.close_app_sig.connect(self.app_shutdown)

    @QtCore.Slot()
    def started_app(self):
        self.app.core.scanner.update_progress_sig.connect(self.view.top_frame.update_progress_slot)
        self.app.core.scanner.update_status_sig.connect(self.view.top_frame.update_status_slot)
        self.app.core.scanner.update_log_file.connect(self.view.container_frame.update_log_slot)
        self.app.core.scanner.update_queue_sig.connect(self.view.status_bar.update_queue_slot)
        self.app.core.scanner.update_queue_sig.connect(self.view.top_frame.update_queue_slot)
        self.app.core.scanner.scan_active_sig.connect(self.view.scan_active_slot)
        self.view.top_frame.refresh_sig.connect(self.app.start_scan)
        self.view.top_frame.upload_sig.connect(self.app.net.send_mails)
        self.app.core.scanner.last_scan_sig.connect(self.view.top_frame.update_last_scan_slot)
        self.app.net.net_started_sig.connect(self.started_net)
        self.app.net_thread.start()

    @QtCore.Slot()
    def started_net(self):
        # Progress bar
        self.app.net.mail.update_progress_sig.connect(self.view.top_frame.update_progress_slot)
        # Top frame status
        self.app.net.mail.update_status_sig.connect(self.view.top_frame.update_status_slot)
        # Queue updater status bar
        self.app.net.update_queue_sig.connect(self.view.status_bar.update_queue_slot)
        # Queue updater top frame
        self.app.net.update_queue_sig.connect(self.view.top_frame.update_queue_slot)
        # a
        self.app.net.update_sent_sig.connect(self.view.status_bar.update_sent_slot)
        # Sending complete
        self.app.net.send_done_sig.connect(self.view.send_complete_slot)
        self.app.net.update_status_sig.connect(self.view.top_frame.update_status_slot)
        self.app.net.update_progress_sig.connect(self.view.top_frame.update_progress_slot)

    @QtCore.Slot()
    def app_shutdown(self, code: int):
        self.close_code = code
        touch.util.log.debug("app shutdown")
        self.app.quit_app_sig.emit()

    @QtCore.Slot()
    def app_closed(self):
        touch.util.log.debug("app closed")
        self.view.main_window.shutdown(self.close_code)
