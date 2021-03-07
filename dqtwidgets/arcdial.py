# Copyright 2021 Dmitry Kouznetsov <dmitry.kouznetsov@protonmail.com>
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
from PySide2.QtWidgets import QDial
from PySide2.QtCore import Qt, Signal, Slot, QPointF, QRectF, QTimer
from PySide2.QtGui import QColor, QFont, QFontMetrics, QPainter, QPen, QPainterPath, QCursor
from math import floor
from types import SimpleNamespace as box


class ArcDial(QDial):

    fvalueChanged = Signal(float)
    dragStateChanged = Signal(bool)

    def __init__(self, label="", start=0, stop=10, initial=0, color=QColor(0x3E, 0xB8, 0xBE)):
        super().__init__()
        self.setRange(start, stop)
        self.setCursor(QCursor(Qt.SizeHorCursor))

        self.fmin = start
        self.fmax = stop
        self.fprecision = 1000
        self._fvalue = initial if initial > start else start

        self._isPressed = False
        self._isHovered = False
        self._lastDragPos = None
        self._lastDragValue = 0

        self._color = color
        self._size = box(height=64, width=64, spacer=5)
        self._hover = box(active=False, min=0, max=9, step=0)
        self._label = box(text=label, width=0, height=0, position=QPointF(0, 0), font=QFont(self.font()))
        self._label.font.setPixelSize(10)

        self.updateSizes()

        QDial.setMinimum(self, 0)
        QDial.setMaximum(self, self.fprecision)
        QDial.setValue(self, 0)

        self.valueChanged.connect(self.fValueChanged)

    @Slot()
    def fValueChanged(self, value):
        self._fvalue = value / self.fprecision * (self.fmax - self.fmin) + self.fmin
        self.fvalueChanged.emit(self._fvalue)

    def setValue(self, value, emitSignal=False):
        if self._fvalue == value:
            return

        if value <= self.fmin:
            qval = 0
            self._fvalue = self.fmin
        elif value >= self.fmax:
            qval = self.fprecision
            self._fvalue = self.fmax
        else:
            qval = round((value - self.fmin) / (self.fmax - self.fmin) * self.fprecision)
            self._fvalue = value

        self.blockSignals(True)
        QDial.setValue(self, qval)
        self.blockSignals(False)

        if emitSignal:
            self.fvalueChanged.emit(self._fvalue)

    def setLabel(self, label):
        if self._label.text == label:
            return

        self._label.text = label
        self.updateSizes()
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._isPressed = True
            self._lastDragPos = event.pos()
            self._lastDragValue = self._fvalue
            self.dragStateChanged.emit(True)

    def mouseMoveEvent(self, event):
        if not self._isPressed:
            return

        r = (self.fmax - self.fmin) / 4
        pos = event.pos()
        dx = r * (pos.x() - self._lastDragPos.x()) / self.width()
        dy = r * (pos.y() - self._lastDragPos.y()) / self.height()
        value = self._lastDragValue + dx - dy

        if value < self.fmin:
            value = self.fmin
        elif value > self.fmax:
            value = self.fmax

        self.setValue(value, True)

    def mouseReleaseEvent(self, _):
        if self._isPressed:
            self._isPressed = False
            self.dragStateChanged.emit(False)

    def paintEvent(self, event):
        painter = QPainter(self)
        event.accept()

        painter.save()
        painter.setRenderHint(QPainter.Antialiasing, True)

        if self._label.text:
            painter.setFont(self._label.font)
            painter.drawText(self._label.position, self._label.text)

        h = self._size.height
        norm = (self._fvalue - self.fmin) / (self.fmax - self.fmin)
        target = QRectF(0, 0, h, h)
        source = QRectF(h, 0, h, h)

        color = self._color.lighter(100 + self._hover.step * 3)

        # Background
        painter.setBrush(Qt.lightGray)
        painter.setPen(QPen(Qt.lightGray, 4))
        painter.drawArc(8.0, 8.0, 50.0, 50.0, 216*16, -252*16)

        # draw small circle
        ballRect = QRectF(14.5, 15.0, 32.0, 32.0)
        ballPath = QPainterPath()
        ballPath.addEllipse(ballRect)
        tmp = (0.375 + 0.75 * norm)
        ballValue = tmp - floor(tmp)
        ballPoint = ballPath.pointAtPercent(ballValue)

        # draw arc
        startAngle = 216 * 16
        spanAngle = -252 * 16 * norm

        painter.setBrush(color)
        painter.setPen(QPen(color, 0))
        painter.drawEllipse(QRectF(ballPoint.x(), ballPoint.y(), 5.2, 5.2))

        painter.setBrush(color)
        painter.setPen(QPen(color, 3))

        painter.drawArc(8.0, 8.0, 50.0, 50.0, startAngle, spanAngle)

        if self._hover.min < self._hover.step < self._hover.max:
            self._hover.step += 1 if self._hover.active else -1
            QTimer.singleShot(20, self.update)

        painter.restore()

    def resizeEvent(self, event):
        QDial.resizeEvent(self, event)
        self.updateSizes()

    def updateSizes(self):
        s = (self._size.height, self._size.height + self._label.height + self._size.spacer)
        self.setMinimumSize(*s)
        self.setMaximumSize(*s)

        if not self._label:
            self._label.height = 0
            self._label.width = 0
            return

        self._label.width = QFontMetrics(self._label.font).horizontalAdvance(self._label.text)
        self._label.height = QFontMetrics(self._label.font).height()

        self._label.position.setX(self._size.height / 2 - self._label.width / 2)
        self._label.position.setY(self._size.height + self._label.height / 2)

    def enterEvent(self, event):
        self._hover.active = True
        if self._hover.step == self._hover.min:
            self._hover.step = self._hover.min + 1
        QDial.enterEvent(self, event)

    def leaveEvent(self, event):
        self._hover.active = False
        if self._hover.step == self._hover.max:
            self._hover.step = self._hover.max - 1
        QDial.leaveEvent(self, event)


if __name__ == "__main__":
    from PySide2.QtWidgets import QApplication
    import sys
    app = QApplication([])

    widget = ArcDial(label="Label", start=100, stop=200)
    # widget.fvalueChanged.connect(lambda x: print(x))
    widget.resize(100, 100)
    widget.show()

    sys.exit(app.exec_())
