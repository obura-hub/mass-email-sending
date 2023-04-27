import touch
from PySide2 import QtCore
import os
from . import core
import PyPDF2 as pdf
from datetime import datetime


class Scanner(QtCore.QThread):
    update_progress_sig = QtCore.Signal(int)
    update_status_sig = QtCore.Signal(str)
    update_log_file = QtCore.Signal(str)
    update_queue_sig = QtCore.Signal(int)
    scan_active_sig = QtCore.Signal(bool)
    last_scan_sig = QtCore.Signal(str)

    def __init__(self):
        super(Scanner, self).__init__()

    def run(self):
        self.scan_active_sig.emit(True)
        self.update_status_sig.emit("Scanning")
        new_files = []
        new_entries = os.scandir(touch.util.Settings.upload)
        self.last_scan_sig.emit(datetime.now().strftime("%I:%M:%S %p"))
        for entry in new_entries:
            if entry.is_file():
                if Scanner.is_pdf(entry):
                    if entry.path in core.Core.files:
                        pass
                    else:
                        core.Core.files.append(entry.path)
                        new_files.append(entry)
        total = len(new_files)
        self.update_status_sig.emit("Processing")
        for _id, entry in enumerate(new_files):
            self.update_progress_sig.emit((_id / total) * 100)
            self.secure_pdf(entry)
        self.update_status_sig.emit("Ready to send")
        self.update_progress_sig.emit(100)
        self.scan_active_sig.emit(False)
        core.Core.scanning = False

    @staticmethod
    def is_pdf(file_name: os.DirEntry):
        if not file_name.name.endswith((".pdf", ".PDF")):
            return False
        try:
            a = pdf.PdfFileReader(open(file_name, "rb"))
            if a.getNumPages() < 0:
                return False
            else:
                return True
        except Exception as err:
            touch.util.log.error("is_pdf : {} filename : {}".format(err, file_name))
        return False

    def secure_pdf(self, file_name: os.DirEntry):
        user = Scanner.get_user_by_id(file_name.name)
        if user:
            self.update_log_file.emit("{}".format(file_name.name))
            try:
                input_stream = pdf.PdfFileReader(open(file_name, "rb"))
                output_file = Scanner.get_secure_output(file_name.name)
                x = open(output_file, "wb")
                output_stream = pdf.PdfFileWriter()
                output_stream.appendPagesFromReader(input_stream)
                password = user.get('password')
                if not password:
                    password = touch.util.Settings.get_setting('default_password')
                output_stream.encrypt(password)
                output_stream.write(x)
                x.close()
                core.Core.queue_files.append([user.get('email'), output_file, file_name])
                self.update_queue_sig.emit(core.Core.get_queue_length())
            except Exception as err:
                touch.util.log.error("is_pdf : {}".format(err))
            return False
        else:
            touch.util.log.info("Invalid user found : {}".format(file_name.name))

    @staticmethod
    def clean_pdf(self, path):
        try:
            os.unlink(path)
        except Exception:
            pass

    @QtCore.Slot(str)
    def changed(self, a: str):
        print(a)

    @staticmethod
    def get_secure_output(file_name) -> str:
        return touch.util.Settings.upload_secure + os.path.sep + file_name

    @staticmethod
    def get_user_by_id(file_name: str) -> dict:
        user_id = Scanner.strip_file_name(file_name)
        return touch.util.Settings.get_user(user_id)

    @staticmethod
    def strip_file_name(name: str) -> int:
        a = name.split("_")
        if len(a) < 2:
            touch.util.log.error("Error reading file name : {} : {}".format(name))
        else:
            try:
                b = a[1]
                return b
            except Exception as err:
                touch.util.log.error("Error reading file name : {} : {}".format(name, err))
        return -1
