from PySide2.QtGui import QPalette, QColor
from PySide2.QtCore import Qt

def dark():
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.black)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    return palette


THEME = {"dark": dark()}


if __name__ == "__main__":
    from PySide2.QtWidgets import QApplication, QLabel
    import sys
    app = QApplication([])

    app.setStyle("Fusion")
    app.setPalette(THEME["dark"])
    widget = QLabel("Hello")
    widget.resize(100, 100)
    widget.show()

    sys.exit(app.exec_())
