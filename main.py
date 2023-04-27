import touch
from PySide2 import QtWidgets
import os


if __name__ == "__main__":
    touch.util.name_current_thread("main thread")
    home = os.path.dirname(os.path.abspath(__file__))
    # Configure application base directory
    touch.util.Settings.set_home(home)
    # bootstrap the settings with config dir or default settings
    touch.util.Settings.load_settings()
    app = QtWidgets.QApplication([])
    app.setStyleSheet(touch.util.style.stylesheet)
    launcher = touch.Launcher()
    launcher.view.show()
    app.exec_()
 