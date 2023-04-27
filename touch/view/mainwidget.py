import touch
from PySide2 import QtWidgets, QtCore, QtGui


class TopFrame(QtWidgets.QFrame):
    refresh_sig = QtCore.Signal()
    upload_sig = QtCore.Signal()
    status_signal = QtCore.Signal(str)

    def __init__(self):
        super(TopFrame, self).__init__()
        self.last_timestamp = "Never"
        self.upload_enabled = False
        self.setMinimumHeight(100)
        self.setMaximumHeight(100)
        self.setObjectName("top_frame")
        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)
        self.button_layout = QtWidgets.QHBoxLayout()
        self.refresh_button = QtWidgets.QPushButton("Scan")
        self.refresh_button.clicked.connect(self.trigger_refresh)
        self.refresh_button.setObjectName("refresh_button")
        self.upload_button = QtWidgets.QPushButton("Start")
        self.upload_button.setObjectName("upload_button")
        self.upload_button.clicked.connect(self.trigger_upload)
        self.upload_button.setEnabled(self.upload_enabled)
        self.main_layout.addLayout(self.button_layout)
        label = QtWidgets.QLabel("Email : ")
        self.sender_email = QtWidgets.QLineEdit()
        self.sender_email.setReadOnly(True)
        self.sender_email.setAlignment(QtCore.Qt.AlignCenter)
        self.sender_email.setObjectName("sender_email")
        self.sender_email.setText(touch.util.Settings.get_setting("email"))
        self.button_layout.addStretch(1)
        self.button_layout.addWidget(label)
        self.button_layout.addWidget(self.sender_email)
        self.button_layout.addStretch(2)
        self.button_layout.addWidget(self.refresh_button)
        self.button_layout.addSpacing(10)
        self.button_layout.addWidget(self.upload_button)
        self.button_layout.addStretch(1)
        self.progress_layout = QtWidgets.QHBoxLayout()
        self.status = QtWidgets.QLabel("Waiting")
        self.status.setObjectName("status")
        self.progress = QtWidgets.QProgressBar()
        self.progress.setObjectName("progres_bar")
        self.progress.setValue(0)
        label = QtWidgets.QLabel("Status : ")
        last_scan_label = QtWidgets.QLabel("Last scan : ")
        self.last_scan = QtWidgets.QLineEdit()
        self.last_scan.setReadOnly(True)
        self.last_scan.setAlignment(QtCore.Qt.AlignCenter)
        self.last_scan.setObjectName("last_scan")
        self.last_scan.setText(self.last_timestamp)
        self.progress_layout.addWidget(last_scan_label)
        self.progress_layout.addWidget(self.last_scan)
        self.progress_layout.addStretch(1)
        self.progress_layout.addWidget(self.progress)
        self.progress_layout.addStretch(1)
        self.progress_layout.addWidget(label)
        self.progress_layout.addWidget(self.status)
        self.main_layout.addLayout(self.progress_layout)

    def scan_active_slot(self, state: bool):
        if state:
            self.refresh_button.setEnabled(False)
            self.upload_button.setEnabled(False)
        else:
            self.refresh_button.setEnabled(True)
            self.upload_button.setEnabled(self.upload_enabled)

    @QtCore.Slot(int)
    def update_queue_slot(self, queue):
        if queue > 0:
            self.upload_enabled = True
        else:
            self.upload_enabled = False
        self.upload_button.setEnabled(self.upload_enabled)

    @QtCore.Slot(str)
    def update_last_scan_slot(self, timestamp: str):
        self.last_scan.setText(timestamp)

    @QtCore.Slot()
    def update_status_slot(self, text: str):
        self.status.setText(text)

    @QtCore.Slot()
    def update_progress_slot(self, value: int):
        self.progress.setValue(value)

    @QtCore.Slot()
    def trigger_refresh(self):
        self.refresh_button.setEnabled(False)
        self.upload_button.setEnabled(False)
        self.refresh_sig.emit()

    @QtCore.Slot()
    def trigger_upload(self):
        self.refresh_button.setEnabled(False)
        self.upload_button.setEnabled(False)
        self.upload_sig.emit()


class ContainerFrame(QtWidgets.QFrame):
    def __init__(self):
        super(ContainerFrame, self).__init__()
        self.setObjectName("container_frame")
        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)
        self.log_file = QtWidgets.QTextEdit()
        self.log_file.moveCursor(QtGui.QTextCursor.End)
        self.log_file.setReadOnly(True)
        self.main_layout.addWidget(self.log_file)

    @QtCore.Slot(str)
    def update_log_slot(self, text: str):
        self.log_file.append(text + "\n")


class MainWidget(QtWidgets.QFrame):
    def __init__(self):
        super(MainWidget, self).__init__()
        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)
