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
from PySide2.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout


def add_widgets(layout, widgets, alignment):
    if not widgets: return layout
    layout.addWidget(widgets[0])
    if alignment: layout.setAlignment(widgets[0], alignment)
    return add_widgets(layout, widgets[1:], alignment)


def _layout(layout, widgets, margin, alignment):
    parent = QWidget()
    layout.setContentsMargins(margin, margin, margin, margin)
    parent.setLayout(add_widgets(layout, widgets, alignment))
    return parent


def h_layout(widgets, spacing=0, margin=5, alignment=None):
    return _layout(QHBoxLayout(spacing=spacing), widgets, margin, alignment)


def v_layout(widgets, spacing=0, margin=5, alignment=None):
    return _layout(QVBoxLayout(spacing=spacing), widgets, margin, alignment)


if __name__ == "__main__":
    from PySide2.QtWidgets import QApplication, QLabel, QWidget
    import sys
    app = QApplication([])

    widget = h_layout([QLabel(str(i)) for i in range(5)])
    widget.show()

    sys.exit(app.exec_())
