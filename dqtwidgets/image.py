# Copyright 2022 Dmitry Kouznetsov <dmitry.kouznetsov@protonmail.com>
#
# This program is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program. If not, see http://www.gnu.org/licenses/.
#
from PySide2.QtCore import Qt, QPoint
from PySide2.QtWidgets import QLabel, QSizePolicy
from PySide2.QtGui import QPixmap, QPainter


class ScalableImage(QLabel):
    def __init__(self, path, max_height=200):
        super().__init__()
        self.pixmap = QPixmap(path)
        self.setPixmap(self.pixmap)
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.setMaximumHeight(max_height)

    def paintEvent(self, event):
        size = self.size()
        painter = QPainter(self)
        point = QPoint(0, 0)
        scaled_pixmap = self.pixmap.scaled(size, Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
        point.setX((size.width() - scaled_pixmap.width())/2)
        point.setY((size.height() - scaled_pixmap.height())/2)
        painter.drawPixmap(point, scaled_pixmap)


if __name__ == "__main__":
    from PySide2.QtWidgets import QApplication
    import sys
    app = QApplication([])

    widget = ScalableImage("images/placeholder-image.png")
    widget.show()

    sys.exit(app.exec_())
