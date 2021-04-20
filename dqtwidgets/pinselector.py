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
from PySide2.QtWidgets import QTableWidget, QTableWidgetItem, QSizePolicy


class PinSelector(QTableWidget):
    def __init__(self, columns, total, cell_size=30):
        super().__init__()
        rows = total // columns
        self.setColumnCount(columns)
        self.setRowCount(rows)

        for col in range(columns):
            self.setColumnWidth(col, cell_size)

        for row in range(rows):
            self.setRowHeight(row, cell_size)

        # Get rid of remaining white space in the table
        horizontalHeader = self.horizontalHeader()
        verticalHeader = self.verticalHeader()
        self.setMaximumWidth(horizontalHeader.length())
        # self.setMaximumHeight(verticalHeader.length())
        self.setMinimumWidth(horizontalHeader.length())
        self.setMinimumHeight(verticalHeader.length())
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # We don't need to display header information since the pin numbers can
        # be easily navigated from the table entries
        self.horizontalHeader().hide()
        self.verticalHeader().hide()

        # Populate table
        for row in range(rows):
            self.setRowHeight(row, cell_size)

            for col in range(columns):

                # The number in the cell depends on the number of rows/columns
                item = QTableWidgetItem(str(col + columns * row + 1))
                item.setTextAlignment(Qt.AlignCenter)

                # Pins cannot be renamed
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)

                # Finally place the item in the correct position
                self.setItem(row, col, item)


if __name__ == "__main__":
    from PySide2.QtWidgets import QApplication
    import sys
    app = QApplication([])

    widget = PinSelector(2, 25)
    widget.show()

    sys.exit(app.exec_())
