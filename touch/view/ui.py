import touch
from PySide2 import QtWidgets, QtCore


class View(QtCore.QObject):
    def __init__(self):
        super(View, self).__init__()
        self.main_window = touch.view.MainWindow()
        self.main_widget = touch.view.MainWidget()
        self.status_bar = touch.view.StatusBar()
        self.main_window.setStatusBar(self.status_bar)
        self.main_window.setCentralWidget(self.main_widget)
        self.top_frame = touch.view.TopFrame()
        self.container_frame_widget = QtWidgets.QScrollArea()
        self.container_frame = touch.view.ContainerFrame()
        self.container_frame_widget.setWidget(self.container_frame)
        self.container_frame_widget.setWidgetResizable(True)
        self.main_widget.main_layout.addWidget(self.top_frame)
        self.main_widget.main_layout.addWidget(self.container_frame_widget)

    @QtCore.Slot(bool)
    def scan_active_slot(self, state: bool):
        self.top_frame.scan_active_slot(state)

    def send_complete_slot(self):
        self.status_bar.status_slot('Send complete. Ready')
        self.top_frame.scan_active_slot(False)

    def show(self):
        self.main_window.show()
