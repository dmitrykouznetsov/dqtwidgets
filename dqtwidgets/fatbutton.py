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
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QPushButton


class FatButton(QPushButton):
    def __init__(self, msg, width=100, height=100, checkable=True):
        super().__init__(msg)

        if checkable:
            self.setCheckable(True)

        self.setFixedSize(width, height)


if __name__ == "__main__":
    from PySide2.QtWidgets import QApplication
    import sys
    app = QApplication([])

    widget = FatButton("Press me!")
    widget.show()

    sys.exit(app.exec_())
