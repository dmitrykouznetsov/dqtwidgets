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
from PySide2.QtWidgets import QWidget
from PySide2.QtCore import QSize
from PySide2.QtGui import QPainter, QPalette
from dataclasses import dataclass


@dataclass
class Coordinate:
    x: float = 0
    y: float = 0
    z: float = 0

    def __add__(self, other):
        return Coordinate(self.x + other.x, self.y + other.y, self.z + other.z)

    def __mul__(self, number):
        return Coordinate(self.x * number, self.y * number, self.z * number)

    def __lt__(self, other):
        return {
            SYMBOLS.left: self.x < other.x,
            SYMBOLS.forward: self.y < other.y,
            SYMBOLS.down: self.z < other.z
        }

    def __gt__(self, other):
        return {
            SYMBOLS.right: self.x > other.x,
            SYMBOLS.back: self.y > other.y,
            SYMBOLS.up: self.z > other.z,
        }


@dataclass
class Bounds:
    """ Rectangle defined by two coordinates.

    The idea is to check whether a Coordinate is within the bounds of the rectangle.

    """
    bottom_left: Coordinate
    top_right: Coordinate

    def __gt__(self, coordinate):
        """ Check if a point is within bounds.

        This checks whether the point is beyond any coordinate of the left
        bottom coordinate of the bounds or right top coorinate of the bounds.
        Then the function returns a dict with all compares along with their
        respective booleans.

        >>> b = Bounds(Coordinate(0, 0, 0), Coordinate(10, 10, 0))
        >>> b > Coordinate(-1, 1, 0)
        >>> {"◀": True, "▶": False, "▲": False, "▼": False}

        """
        oob_left = coordinate < self.bottom_left
        oob_right = coordinate > self.top_right
        return {**oob_left, **oob_right}


class CrossHair(QWidget):
    def __init__(self, coordinate, bounds, width, height):
        super().__init__()
        self._width = width
        self._height = height
        self._bounds = bounds
        self._coordinate = coordinate
        self._center = Coordinate(self._width // 2 - 1, self._height // 2 - 1, 0)

        self.setFixedSize(QSize(self._width, self._height))
        offset = 10

        self._scale = dict(x=(self._width // 2 - offset) / self._bounds.top_right.x,
                          y=(self._height // 2 - offset) / self._bounds.top_right.y)

    def paintEvent(self, event):
        painter = QPainter(self)
        scaled_coord = Coordinate(self._coordinate.x * self._scale["x"],
                                  self._coordinate.y * self._scale["y"], 0)
        pos = self._center + scaled_coord

        # Two perpendicular lines for the cross-hair
        painter.drawLine(0, pos.y, self.width() - 1, pos.y)
        painter.drawLine(pos.x, 0, pos.x, self.height() - 1)

        # Surrounding rectangle
        painter.drawRect(0, 0, self.width() - 1, self.height() - 1)

    def setCoordinate(self, new_coordinate):
        self.coordinate = new_coordinate
        self.update()


if __name__ == "__main__":
    from PySide2.QtWidgets import QApplication
    import sys
    app = QApplication([])

    widget = CrossHair(coordinate=Coordinate(2.5, 2.5),
                       bounds=Bounds(Coordinate(-5, -5), Coordinate(5, 5)),
                       width=180, height=100)
    widget.show()

    sys.exit(app.exec_())
