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


def add_context_menu(widget):
    widget.on_context_menu = lambda p: widget.popMenu.exec_(widget.mapToGlobal(p))
    # set button context menu policy
    widget.setContextMenuPolicy(Qt.CustomContextMenu)
    widget.customContextMenuRequested.connect(widget.on_context_menu)
    widget.popMenu = QMenu(widget)


def add_action(widget, entry, action):
    widget.popMenu.addAction(entry, lambda: action(widget))


def enable_bidirectional_drag(widget):
    widget.setDragDropMode(widget.DragDrop)
    widget.setSelectionMode(widget.ExtendedSelection)
    widget.setAcceptDrops(True)
    widget.setDefaultDropAction(Qt.MoveAction)
    widget.setDropIndicatorShown(True)


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
    def __init__(self, nodes={}, actions={}):
        # TODO: fix resize bug for windows
        super().__init__()
        add_context_menu(self)

        # Don't like the headerbar
        self.setHeaderHidden(True)

        # TODO: draw lines to make divisions more clear
        self.setAlternatingRowColors(True)

        # Drag'n'drop between e.g. list and tree
        enable_bidirectional_drag(self)

        #TODO: add unpacking logic
        self.nodes = nodes
        self.itemDoubleClicked.connect(self.edit_item)

    def add_entry(self):
        i = QTreeWidgetItem()
        i.setText(0, "NEW ENTRY")
        self.insertTopLevelItem(0, i)

    @property
    def items(self):
        return model_to_dict(self.model())

    def edit_item(self, item, col):
        if not (item.flags() & Qt.ItemIsEditable):
            item.setFlags(item.flags() | Qt.ItemIsEditable)
        self.editItem(item, col)


class EditableList(QListWidget):
    def __init__(self, items=[]):
        super().__init__()
        add_context_menu(self)
        self.itemDoubleClicked.connect(self.edit_item)

        # Drag'n'drop between e.g. list and tree
        enable_bidirectional_drag(self)

        self.populate(items)

    def populate(self, items):
        for item in items:
            i = QListWidgetItem(item)
            i.setFlags(i.flags() | Qt.ItemIsEditable)
            self.addItem(i)

    def edit_item(self, item):
        if not (item.flags() & Qt.ItemIsEditable):
            item.setFlags(item.flags() | Qt.ItemIsEditable)
        self.editItem(item)

    @property
    def items(self):
        return [self.item(i).text() for i in range(self.count())]



if __name__ == "__main__":
    from PySide2.QtWidgets import QApplication, QHBoxLayout, QWidget
    import sys
    app = QApplication([])

    list_widget = EditableList(items=["item 1", "item 2", "item 3"])
    add_action(list_widget, "print list", lambda l: print(l.items))
    add_action(list_widget, "clear list", lambda l: l.clear())

    tree_widget = EditableTree()
    add_action(tree_widget, "print items dict", lambda tree: print(tree.items))
    add_action(tree_widget, "add entry", lambda tree: tree.add_entry())

    container = QWidget()
    layout = QHBoxLayout()
    layout.addWidget(list_widget)
    layout.addWidget(tree_widget)
    container.setLayout(layout)
    container.show()

    sys.exit(app.exec_())
