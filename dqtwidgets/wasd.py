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
from PySide2.QtWidgets import QWidget, QPushButton, QGroupBox, QGridLayout, QLabel
from PySide2.QtCore import Slot, Qt, QSize
from PySide2.QtGui import QCursor, QPixmap
from dataclasses import dataclass
import dqtwidgets.resources_rc


@dataclass
class Symbols:
    """ Store the utf8 symbols in a separate object.

    This facilitates mantaining a dictionary of symbols and is convenient
    for communication between classes. The Symbols are initialized as a
    global value

    >>> SYMBOLS = Symbols()

    Make sure not to mutate this value after creation.

    """
    left: str = "◀"
    right: str = "▶"
    forward: str = "▲"
    back: str = "▼"
    up: str = "△"
    down: str = "▽"


SYMBOLS = Symbols()


@dataclass
class KeyboardShortCuts:
    left: str
    right: str
    forward: str
    back: str
    up: str
    down: str

    def __call__(self):
        return {
            SYMBOLS.left: self.left,
            SYMBOLS.right: self.right,
            SYMBOLS.forward: self.forward,
            SYMBOLS.back: self.back,
            SYMBOLS.up: self.up,
            SYMBOLS.down: self.down
        }

    def __str__(self):
        return self.forward + self.left + self.back + self.right + self.up + self.down


def setHandCursor(widget):
    widget.setCursor(QCursor(Qt.PointingHandCursor))


def ArrowKey(label, shortcut, size=(50, 40)):
    button = QPushButton(label)
    setHandCursor(button)
    button.setFixedSize(QSize(*size))
    button.setShortcut(shortcut)
    return button


class QLED(QLabel):
    def __init__(self, parent):
        super().__init__()
        setHandCursor(self)

        self.ACTIVE = QPixmap(":images/led_green.png")
        self.DISABLED = QPixmap(":images/led_off.png")
        self.MOVING = QPixmap(":images/led_yellow.png")
        self.WARNING = QPixmap(":images/led_red.png")

        self.parent = parent
        self.setState(self.ACTIVE)
        self.setAlignment(Qt.AlignCenter)

    def moving(self):
        self.setState(self.MOVING)

    def active(self):
        self.setState(self.ACTIVE)

    def warning(self):
        self.setState(self.WARNING)

    def setState(self, state):
        self.setPixmap(state)


class ArrowKeys(QGroupBox):
    def __init__(self, label, keymap):
        super().__init__(label)
        layout = QGridLayout()
        self.keymap = keymap()

        self.buttons = {
            SYMBOLS.left: ArrowKey(SYMBOLS.left, self.keymap[SYMBOLS.left]),
            SYMBOLS.right: ArrowKey(SYMBOLS.right, self.keymap[SYMBOLS.right]),
            SYMBOLS.forward: ArrowKey(SYMBOLS.forward, self.keymap[SYMBOLS.forward]),
            SYMBOLS.back: ArrowKey(SYMBOLS.back, self.keymap[SYMBOLS.back]),
            SYMBOLS.up: ArrowKey(SYMBOLS.up, self.keymap[SYMBOLS.up]),
            SYMBOLS.down: ArrowKey(SYMBOLS.down, self.keymap[SYMBOLS.down]),
        }

        # The positions of the buttons should resemble their actual position on
        # the keyboard e.g. wasd
        layout.addWidget(self.buttons[SYMBOLS.left], 1, 0)
        layout.addWidget(self.buttons[SYMBOLS.right], 1, 2)
        layout.addWidget(self.buttons[SYMBOLS.forward], 0, 1)
        layout.addWidget(self.buttons[SYMBOLS.back], 1, 1)

        # TODO: Make optional
        # Vertical control
        layout.addWidget(self.buttons[SYMBOLS.up], 0, 3)
        layout.addWidget(self.buttons[SYMBOLS.down], 1, 3)

        # Toggle controls
        self.led = QLED(self)
        layout.addWidget(self.led, 0, 0)

        self.setLayout(layout)

    def connect(self, direction, action):
        self.buttons[direction].clicked.connect(action)

    def toggleButtons(self, disabled):
        for button in self.buttons.values():
            button.setDisabled(disabled)


if __name__ == "__main__":
    from PySide2.QtWidgets import QApplication
    import sys
    app = QApplication([])

    widget = ArrowKeys("controls",
                       KeyboardShortCuts(left="A", right="D", forward="W", back="S", up="R", down="F"))
    widget.show()

    sys.exit(app.exec_())
