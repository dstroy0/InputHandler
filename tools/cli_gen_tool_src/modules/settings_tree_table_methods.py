##
# @file settings_tree_table_methods.py
# @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
# @brief MainWindow external methods
# @version 1.0
# @date 2022-07-08
# @copyright Copyright (c) 2022
# Copyright (C) 2022 Douglas Quigg (dstroy0) <dquigg123@gmail.com>
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 3 as published by the Free Software Foundation.

from __future__ import absolute_import

import copy

# pyside imports
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex

from PySide6.QtWidgets import (
    QHeaderView,
    QPushButton,
    QTreeWidgetItem,
    QAbstractItemView,
    QSizePolicy,
    QTableView,
    QAbstractScrollArea,
)


class DelimitersTableViewModel(QAbstractTableModel):
    """Display model for a delimiters table

    Args:
        QAbstractTableModel (class): This class specializes QAbstractTableModel
    """

    def __init__(self, parent, tree, cliopt, dict_pos, delimiters: dict) -> None:

        super(DelimitersTableViewModel, self).__init__()
        self._parent = parent
        self.tree = tree
        self.cliopt = cliopt
        self.dict_pos = dict_pos
        self.delimiters = delimiters
        self.keys = list(self.delimiters.keys())
        self.values = list(self.delimiters.values())
        self.row_count = int(len(self.delimiters) + 1)
        self.column_count = 2
        self.editing = False
        self.clicked_row = None

        for i in range(self.row_count - 1):
            parent.remove_row_buttons.append(QPushButton())
            parent.remove_row_buttons[i].setIcon(parent.remove_row_button_icon)

    def flags(self, index) -> Qt.ItemFlags:
        if (
            index.isValid()
            and index.column() == 0
            and index.row() < (self.rowCount() - 1)
        ):
            return (
                super().flags(index)
                | Qt.ItemIsSelectable
                | Qt.ItemIsEditable
                | Qt.ItemIsEnabled
            )
        else:
            return super().flags(index) | Qt.ItemIsSelectable | Qt.ItemIsEnabled

    def setData(self, index, value, role) -> bool:
        if role in (Qt.DisplayRole, Qt.EditRole):
            if not value:
                return False

            clean_value = value.strip("<>")
            if not clean_value:
                return False
            self.cliopt[self.dict_pos[0]]["var"][self.dict_pos[2]][
                str(index.row())
            ] = clean_value
            self.dataChanged.emit(index, index)
            table = self._parent.objectName().split(",")[2]
            self._parent.logger.info(
                f"{table} table, row {index.row()+1} data changed to <{clean_value}>"
            )
        return True

    def columnCount(self, parent: QModelIndex = None) -> int:        
        return self.column_count

    def rowCount(self, parent: QModelIndex = None) -> int:        
        return int(len(self.cliopt[self.dict_pos[0]]["var"][self.dict_pos[2]]) + 1)

    def ar(self) -> None:
        row = self.rowCount() - 1
        parent = self._parent.currentIndex()
        self.insertRow(row, parent)

    def insertRow(self, row: int, parent) -> bool:
        self.beginInsertRows(parent, row, row)
        start_len = len(self.cliopt[self.dict_pos[0]]["var"][self.dict_pos[2]])
        self.cliopt[self.dict_pos[0]]["var"][self.dict_pos[2]].update(
            {str(start_len): ""}
        )        
        self.insertRows(row, 1, parent)
        self.endInsertRows()
        self.insert_row_move_buttons(row)
        self.dataChanged.emit(parent, parent)
        self.layoutChanged.emit()
        return super().insertRow(row, parent)

    def insert_row_move_buttons(self, row: int):
        self._parent.remove_row_buttons.append(QPushButton())
        self._parent.remove_row_buttons[row].setIcon(
            self._parent.remove_row_button_icon
        )
        index = self.index(row, 0)
        self._parent.setIndexWidget(index, None)
        index = self.index(row, 1)
        self._parent.setIndexWidget(index, self._parent.remove_row_buttons[row])
        self._parent.remove_row_buttons[row].clicked.connect(self.rr)
        index = self.index(self.rowCount() - 1, 0)
        self._parent.add_row_button = QPushButton("Add Delimiter")
        self._parent.add_row_button.clicked.connect(self.ar)
        self._parent.setIndexWidget(index, self._parent.add_row_button)

    def rr(self):
        row = self._parent.currentIndex().row()
        parent = self._parent.currentIndex()
        self.removeRow(row, parent)

    def removeRow(self, row: int = None, parent=None) -> bool:
        if not parent.isValid():
            row = self._parent.currentIndex().row()
            parent = self._parent.currentIndex()
        print(f"remove row {row}")

        self.beginRemoveRows(parent, row, row)
        del self._parent.remove_row_buttons[row]
        del self.cliopt[self.dict_pos[0]]["var"][self.dict_pos[2]][str(row)]
        new_dict = copy.deepcopy(self.cliopt[self.dict_pos[0]]["var"][self.dict_pos[2]])

        self.cliopt[self.dict_pos[0]]["var"][self.dict_pos[2]] = {}

        i = 0
        for key in new_dict:
            self.cliopt[self.dict_pos[0]]["var"][self.dict_pos[2]].update(
                {str(i): new_dict[key]}
            )
            i += 1
        self.removeRows(row, row, parent)

        index = self.index(self.rowCount() - 1, 1)
        self._parent.setIndexWidget(index, None)
        index = self.index(self.rowCount() - 1, 0)
        self._parent.setIndexWidget(index, self._parent.add_row_button)
        self.endRemoveRows()
        self.dataChanged.emit(parent, parent)
        self.layoutChanged.emit()
        return super().removeRow(row, parent)

    def moveRow(
        self,
        sourceParent: QModelIndex,
        sourceRow: int,
        destinationParent: QModelIndex,
        destinationChild: int,
    ) -> bool:
        self.beginMoveRows(
            QModelIndex(), sourceRow, sourceRow, QModelIndex(), destinationChild
        )

        self.endMoveRows()
        return super().moveRow(
            sourceParent, sourceRow, destinationParent, destinationChild
        )

    def data(self, index: QModelIndex, role: int):
        """Table data positioning.

        Args:
            index (QModelIndex): The model index.
            role (Qt Role): What role is the data.

        Returns:
            str: data in the cell
        """
        if not index.isValid():
            return None
        elif (
            index.column() == 0
            and (index.row() - 1)
            < (len(self.cliopt[self.dict_pos[0]]["var"][self.dict_pos[2]]) - 1)
            and role == Qt.DisplayRole
            or role == Qt.EditRole
        ):
            return (
                "<"
                + str(
                    self.cliopt[self.dict_pos[0]]["var"][self.dict_pos[2]][
                        str(index.row())
                    ]
                )
                + ">"
            )

        # returns tooltips on a valid index if there are any for the cell
        elif role == Qt.ToolTipRole:
            if (index.row() - 1) < (len(self.cliopt[self.dict_pos[0]]["var"][self.dict_pos[2]]) - 1):
                if index.column() == 0:
                    return str(f"type: {self.dict_pos[2]}, any char except the wildcard char is valid")
                else:
                    return str(f"remove row {index.row()+1}")
            else:
                if index.column() == 0:
                    return str(f"add row to {self.dict_pos[2]} table")
                else:
                    return None
        else:
            return None

    def headerData(self, section: int, orientation: int, role: int):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal and section == 0:
            return "Delimiters"
        elif orientation == Qt.Vertical and role == Qt.DisplayRole:
            if int(section) < int(self.rowCount() - 1):
                return str(section + 1)
            else:
                return None
        else:
            return None

    def edit_table_view(self, index: QModelIndex):
        if index.isValid() and self.editing == False:
            self.editing = True
            self._parent.setCurrentIndex(index)
            self._parent.edit(index)


class DelimitersTableView(QTableView):
    def __init__(
        self,
        logger,
        cursor,
        settings_tree,
        cliopt,
        tree,
        container,
        remove_row_button_icon,
    ) -> None:
        super(DelimitersTableView, self).__init__()
        self.logger = logger
        self.cursor_ = cursor
        self.remove_row_button_icon = remove_row_button_icon
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        dict_pos = container.data(4, 0).split(",")
        self.setObjectName(str(container.data(4, 0)))

        delimiters = cliopt[dict_pos[0]]["var"][dict_pos[2]]
        self.remove_row_buttons = []
        self.table_model = DelimitersTableViewModel(
            self, tree, cliopt, dict_pos, delimiters
        )
        self.setModel(self.table_model)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        settings_tree.setItemWidget(container, 0, self)

        self.add_row_button = QPushButton("Add Delimiter")
        self.add_row_button.clicked.connect(self.table_model.ar)
        index = self.table_model.index(self.table_model.rowCount() - 1, 0)
        self.setIndexWidget(index, self.add_row_button)

        for i in range(len(self.remove_row_buttons)):
            index = self.table_model.index(i, 1)
            self.setIndexWidget(index, self.remove_row_buttons[i])
            self.remove_row_buttons[i].clicked.connect(self.table_model.rr)

        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.clicked.connect(self.table_model.edit_table_view)
        self.clicked.connect(self.update_index)
        self.pressed.connect(self.table_model.edit_table_view)

    def update_index(self):
        self.setCurrentIndex(self.indexAt(self.cursor_pos()))

    def cursor_pos(self):
        return self.cursor_.pos()

    def dataChanged(self, topLeft, bottomRight, roles) -> None:
        if self.table_model.editing == True:
            self.table_model.editing = False
            print("edit complete")
        return super().dataChanged(topLeft, bottomRight, roles)


# this is a helper class
class SettingsTreeTableMethods(object):
    ## the constructor
    def __init__(self):
        super(SettingsTreeTableMethods, self).__init__()
        SettingsTreeTableMethods.logger = self.get_child_logger(__name__)

    ## builds a table onto a tree widget item
    def build_tree_table_widget(
        self,
        index,
        tree,
        dict_key,
        dict_key2,
    ):
        dict_pos = str(dict_key) + "," + str(index) + "," + str(dict_key2)
        # add parent tree item to root
        tree["parents"][dict_key2] = QTreeWidgetItem(tree["root"], [dict_key2, ""])
        # add treewidgetitem parent tree item to contain the table
        tree["items"][dict_key2]["QTreeWidgetItem"] = QTreeWidgetItem(
            tree["parents"][dict_key2], ["", ""]
        )
        tree_widget_item = tree["items"][dict_key2]["QTreeWidgetItem"]
        # set the treewidgetitem column 4 (hidden to user) to positional data
        tree_widget_item.setData(4, 0, dict_pos)
        # make the treewidgetitem editable
        tree_widget_item.setFlags(tree_widget_item.flags() | Qt.ItemIsSelectable)
        # make the treewidgetitem span columns
        tree_widget_item.setFirstColumnSpanned(True)

        cursor = self.qcursor

        logger = SettingsTreeTableMethods.logger

        table = DelimitersTableView(
            logger,
            cursor,
            self.ui.settings_tree,
            self.cliOpt,
            tree,
            tree_widget_item,
            self.ui.trashIcon,
        )

    # end settings_tree table functions


# end of file
