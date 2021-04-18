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
from PySide2.QtWidgets import QGroupBox, QVBoxLayout, QSizePolicy


def group_box(label, widget):
    g = QGroupBox(label)
    layout = QVBoxLayout()
    layout.setSpacing(0)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(widget)
    g.setLayout(layout)
    g.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    return g


if __name__ == "__main__":
    from PySide2.QtWidgets import QApplication, QPushButton
    import sys
    app = QApplication([])

    widget = group_box("test", QPushButton("press me!"))
    widget.show()

    sys.exit(app.exec_())
