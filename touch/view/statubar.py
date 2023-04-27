from PySide2 import QtWidgets, QtCore


class StatusBar(QtWidgets.QStatusBar):

    def __init__(self):
        super(StatusBar, self).__init__()
        self.queue = QtWidgets.QLabel("0")
        self.queue.setObjectName('status_queue_field')
        queue_label = QtWidgets.QLabel("Queue : ")
        self.addPermanentWidget(queue_label)
        self.addPermanentWidget(self.queue)
        self.sent = QtWidgets.QLabel("0")
        self.sent.setObjectName('status_sent_field')
        sent_label = QtWidgets.QLabel("Sent : ")
        self.addPermanentWidget(sent_label)
        self.addPermanentWidget(self.sent)
        status_label = QtWidgets.QLabel("Status :")
        self.status = QtWidgets.QLabel("Ready")
        self.addWidget(status_label)
        self.addWidget(self.status)

    @QtCore.Slot(int)
    def update_queue_slot(self, queue):
        self.queue.setText("{}".format(queue))

    @QtCore.Slot(str)
    def status_slot(self, text):
        self.status.setText(text)

    @QtCore.Slot(int)
    def update_sent_slot(self, sent):
        self.sent.setText("{}".format(sent))
