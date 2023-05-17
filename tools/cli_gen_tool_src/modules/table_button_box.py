from PySide6.QtWidgets import QHBoxLayout, QStyle, QPushButton, QWidget


class TableButtonBox(QWidget):
    """up/down/remove row button widget for qtablewidget

    Args:
        QWidget (class): base class being specialized
    """

    def __init__(self, parent) -> None:
        super(TableButtonBox, self).__init__()
        self.setParent(parent)
        self.table = parent
        self.widget_layout = QHBoxLayout(parent)
        self.up_icn = self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowUp)
        self.dn_icn = self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowDown)
        self.del_row_icn = self.style().standardIcon(
            QStyle.StandardPixmap.SP_BrowserStop
        )
        self.up_btn = QPushButton()
        self.up_btn.setFixedSize(
            self.up_icn.actualSize(self.up_icn.availableSizes()[0])
        )
        self.up_btn.setText("")
        self.up_btn.setToolTip("Move argument up")
        self.up_btn.setIcon(self.up_icn)
        self.dn_btn = QPushButton()
        self.dn_btn.setFixedSize(
            self.dn_icn.actualSize(self.dn_icn.availableSizes()[0])
        )
        self.dn_btn.setText("")
        self.dn_btn.setToolTip("Move argument down")
        self.dn_btn.setIcon(self.dn_icn)
        self.del_row_btn = QPushButton()
        self.del_row_btn.setFixedSize(
            self.dn_icn.actualSize(self.dn_icn.availableSizes()[0])
        )
        self.del_row_btn.setText("")
        self.del_row_btn.setToolTip("Delete argument")
        self.del_row_btn.setIcon(self.del_row_icn)
        self.widget_layout.addWidget(self.up_btn)
        self.widget_layout.addWidget(self.dn_btn)
        self.widget_layout.addWidget(self.del_row_btn)
        self.setLayout(self.widget_layout)
        self.up_btn.clicked.connect(self.move_row_up)
        self.dn_btn.clicked.connect(self.move_row_down)
        self.del_row_btn.clicked.connect(self.remove_row)

    def row(self):
        return self.table.row(
            self.table.itemAt(
                self.table.viewport().mapFromGlobal(self.table._cursor.pos())
            )
        )

    def move_row_up(self):
        row = self.row()
        sourceItems = self.takeRow(row)
        destItems = self.takeRow(row - 1)
        self.setRow(row - 1, sourceItems)
        self.setRow(row, destItems)

    def move_row_down(self, row: int = None):
        row = self.row()
        sourceItems = self.takeRow(row)
        destItems = self.takeRow(row + 1)
        self.setRow(row + 1, sourceItems)
        self.setRow(row, destItems)

    def remove_row(self):
        row = self.row()
        self.table.removeRow(row)
        self.table.setCurrentCell(row - 1, 0)

    def takeRow(self, row: int) -> list:
        rowItems = []
        table = self.table
        for col in range(table.columnCount()):
            rowItems.append(table.takeItem(row, col))
        return rowItems

    def setRow(self, row: int, rowItems: list):
        table = self.table
        for col in range(table.columnCount()):
            table.setItem(row, col, rowItems[col])
