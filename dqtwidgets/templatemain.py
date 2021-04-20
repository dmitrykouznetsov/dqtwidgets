from PySide2.QtWidgets import QMainWindow
from PySide2.QtCore import QSettings


class MainWindowTemplate(QMainWindow):
    def __init__(self, domain, appname, centralwidget, close_event=None):
        super().__init__()
        self.close_event = close_event
        self.settings = QSettings(domain, appname)
        self.setWindowTitle(appname)
        self.setCentralWidget(centralwidget)

    def closeEvent(self, event):
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())
        if self.close_event:
            self.close_event()
        super().closeEvent(event)

    def readSettings(self):
        try:
            self.restoreGeometry(self.settings.value("geometry"))
            self.restoreState(self.settings.value("windowState"))
        except:
            print("Settings not found")

    def showEvent(self, event):
        self.readSettings()
        super().showEvent(event)
