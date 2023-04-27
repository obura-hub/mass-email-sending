import touch
from PySide2 import QtCore

from . import core
from . import  mail
import asyncio
import os


class Net(QtCore.QObject):
    net_started_sig = QtCore.Signal()
    quit_net_sig = QtCore.Signal()
    close_net_sig = QtCore.Signal(int)
    update_status_sig = QtCore.Signal(str)
    update_progress_sig = QtCore.Signal(int)
    update_queue_sig = QtCore.Signal(int)
    update_sent_sig = QtCore.Signal(int)
    send_done_sig = QtCore.Signal()
    mail: mail.Mail

    def __init__(self):
        super(Net, self).__init__()
        self.mail = mail.Mail()

    @QtCore.Slot()
    def started(self):
        touch.util.log_current_thread("net")
        self.net_started_sig.emit()

    @QtCore.Slot()
    def send_mails(self):
        if not core.Core.sending:
            core.Core.sending = True
            self.update_status_sig.emit("Setting up mail")
            self.update_progress_sig.emit(1)
            self.mail.setup()
            errors = False
            if self.mail.configure():
                value = 0
                queue_length = len(core.Core.queue_files)
                sent = 1
                while len(core.Core.queue_files) > 0:
                    mail_data = core.Core.queue_files.pop()
                    self.update_status_sig.emit("Sending {} of {}".format(sent, queue_length))
                    self.mail.send_report(mail_data[0], mail_data[1])
                    if True:
                        self.update_progress_sig.emit(10 + ((sent / queue_length) * 90))
                        self.update_queue_sig.emit(core.Core.get_queue_length())
                        self.update_sent_sig.emit(sent)
                        sent += 1
                        #os.unlink(mail_data[2])
                        #os.unlink(mail_data[1])
                    else:
                        core.Core.queue_files.append(mail_data)
                        errors = True
                        touch.util.log.error('Error sending file')
                        break
            else:
                touch.util.log.error('Mail errorrrr')
            core.Core.sending = False
            if errors:
                self.update_status_sig.emit("Sending failed")
            else:
                self.update_status_sig.emit("Send success")
        self.send_done_sig.emit()
    
    @QtCore.Slot()
    def shutdown(self):
        self.quit_net_sig.emit()
