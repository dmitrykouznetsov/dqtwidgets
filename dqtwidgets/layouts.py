from PySide2.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout


def add_widgets(layout, widgets):
    if not widgets: return layout
    layout.addWidget(widgets[0])
    return add_widgets(layout, widgets[1:])


def _layout(layout, widgets):
    parent = QWidget()
    parent.setLayout(add_widgets(layout, widgets))
    return parent

def h_layout(widgets):
    return _layout(QHBoxLayout(), widgets)


def v_layout(widgets):
    return _layout(QVBoxLayout(), widgets)


if __name__ == "__main__":
    from PySide2.QtWidgets import QApplication, QLabel, QWidget
    import sys
    app = QApplication([])

    widget = h_layout([QLabel(str(i)) for i in range(5)])
    widget.show()

    sys.exit(app.exec_())
