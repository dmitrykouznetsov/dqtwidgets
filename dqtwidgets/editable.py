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
from PySide2.QtWidgets import QTreeWidget, QTreeWidgetItem, QListWidget, QListWidgetItem, QMenu, QAction
from PySide2.QtCore import Qt, QDataStream


def model_to_dict(model):
    d = dict()

    def fill(parent_index, d):
        v = {}
        for i in range(model.rowCount(parent_index)):
            ix = model.index(i, 0, parent_index)
            fill(ix, v)
        d[parent_index.data()] = v

    for i in range(model.rowCount()):
        ix = model.index(i, 0)
        fill(ix, d)
    return d


class EditableTree(QTreeWidget):
    def __init__(self, nodes={}):
        super().__init__()

        self.setHeaderHidden(True)
        self.setDragDropMode(self.DragDrop)
        self.setSelectionMode(self.ExtendedSelection)
        self.setAcceptDrops(True)
        self.setDefaultDropAction(Qt.MoveAction)
        self.setAlternatingRowColors(True)

        #TODO: add unpacking logic
        self.nodes = nodes

        # set button context menu policy
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_context_menu)

        # create context menu
        self.popMenu = QMenu(self)
        self.popMenu.addAction(QAction('print model', self, triggered=self.print_model))

    def on_context_menu(self, point):
        # show context menu
        self.popMenu.exec_(self.mapToGlobal(point))

    def print_model(self):
        print(model_to_dict(self.model()))


class EditableList(QListWidget):
    def __init__(self, *items):
        super().__init__()

        self.setDragDropMode(self.DragDrop)
        self.setSelectionMode(self.ExtendedSelection)
        self.setAcceptDrops(True)
        self.setDefaultDropAction(Qt.MoveAction)

        self.populate(*items)

    def populate(self, *items):
        for i in items:
            self.addItem(i)


if __name__ == "__main__":
    from PySide2.QtWidgets import QApplication, QHBoxLayout, QWidget
    import sys
    app = QApplication([])

    layout = QHBoxLayout()
    layout.addWidget(EditableList("item 1", "item 2", "item 3"))
    layout.addWidget(EditableTree())

    container = QWidget()
    container.setLayout(layout)
    container.show()

    sys.exit(app.exec_())
