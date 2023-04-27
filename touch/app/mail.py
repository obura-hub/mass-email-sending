import touch
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from os.path import basename
from PySide2 import QtCore


class Mail(QtCore.QObject):
    email: str
    password: str
    smtp: SMTP
    update_status_sig = QtCore.Signal(str)
    update_progress_sig = QtCore.Signal(int)

    def __init__(self):
        super(Mail, self).__init__()
        self.authenticated = False

    def setup(self):
        self.email = touch.util.Settings.get_setting("email")
        self.password = touch.util.Settings.get_setting("password")

    def send_report(self, email: str, file_name: str) -> bool:
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = email
            msg['Subject'] = "Daily report"
            text = "Below is your report for this month. Thank you."
            msg.attach(MIMEText(text))
            with open(file_name, "rb") as fil:
                ext = file_name.split('.')[-1:]
                attached_file = MIMEApplication(fil.read(), _subtype=ext)
                attached_file.add_header(
                    'content-disposition', 'attachment', filename=basename(file_name))
            msg.attach(attached_file)
            touch.util.log.debug("Sending mail : {}".format(email))
            a = self.smtp.sendmail(self.email, email, msg.as_string())
            touch.util.log.debug("Send success : {}".format(email))
            return True
        except Exception as err:
            touch.util.log.error("send-report error : {}".format(err))
            return False

    def configure(self) -> bool:
        if self.authenticated:
            return True
        else:
            touch.util.log.info("Setting up mail server")
            try:
                self.update_status_sig.emit("Connecting")
                self.smtp = SMTP(host="smtp.gmail.com", port=587)
                self.update_progress_sig.emit(2)
                # self.smtp.set_debuglevel(True)
                self.smtp.starttls()
                self.update_progress_sig.emit(5)
                touch.util.log.info("Signing in")
                self.update_status_sig.emit("Authenticating")
                self.smtp.login(self.email, self.password)
                self.authenticated = True
                self.update_progress_sig.emit(10)
                self.update_status_sig.emit("Login success")
                touch.util.log.info("Login success: {}".format(self.email))
                return True
            except Exception as err:
                touch.util.log.error("Mail configure error : {}".format(err))
                return False
