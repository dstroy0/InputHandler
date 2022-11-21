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

from modules.display_models import displayModels
from modules.data_models import dataModels

# pyside imports
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex

from PySide6.QtWidgets import (
    QHeaderView,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTreeWidgetItem,
    QAbstractItemView,
    QSizePolicy,
    QTableView,
)


class DelimitersTableViewModel(QAbstractTableModel):
    """Display model for the parameters table

    Args:
        QAbstractTableModel (class): This class specializes QAbstractTableModel
    """

    def __init__(self, parent, tree, cliopt, dict_pos, delimiters: dict, remove_row_icon) -> None:
        """constructor method

        Args:
            parameters (dict, optional): Set placeholder text in CommandParametersDialog input fields. Defaults to None.
        """
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
        
    def flags(self, index) -> Qt.ItemFlags:
        if index.column == 0 and index.row() < self.rowCount():
            return Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled
        else:
            return Qt.ItemIsSelectable | Qt.ItemIsEnabled

    def setData(self, index, value, role) -> bool:
        if role == Qt.EditRole:
            self.cliopt[self.dict_pos[0]]["var"][self.dict_pos[2]][str(index.row())] = value
            return True
        return False

    def columnCount(self, index: QModelIndex) -> int:
        """property

        Args:
            parent (QModelIndex, optional): The model index. Defaults to QModelIndex().

        Returns:
            int: The number of columns.
        """     
        return self.column_count
       
    def rowCount(self, parent) -> int:
        """property

        Args:
            parent (QModelIndex, optional): The model index. Defaults to QModelIndex().

        Returns:
            int: The number of rows.
        """
        return self.row_count

    def insertRow(self, row: int, parent) -> bool:
        return super().insertRow(row, parent)

    def removeRow(self, row: int, parent) -> bool:
        return super().removeRow(row, parent)

    def data(self, index: QModelIndex, role: int):
        """Table data positioning.

        Args:
            index (QModelIndex): The model index.
            role (Qt Role): What role is the data.

        Returns:
            str: data in the cell
        """
        if index.column() == 0 and index.row() < self.rowCount(index) - 1 and role == Qt.DisplayRole or role == Qt.EditRole:            
            return str("'" + str(self.cliopt[self.dict_pos[0]]["var"][self.dict_pos[2]][str(index.row())]) + "'")
        if role == Qt.ToolTipRole:
            return str("tooltip ph")

    def headerData(self, section: int, orientation: int, role: int):
        """Displays header labels

        Args:
            section (int): Cell position
            orientation (int): Text orientation
            role (int): role of the data

        Returns:
            str: The section label.
        """
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal and section == 0:
                return "Delimiters"
        else:
            return None


class DelimitersTableView(QTableView):
    def __init__(
        self,
        settings_tree,
        cliopt,
        tree,
        container,
        add_row_function,
        remove_row_button,
        remove_row_button_icon,
    ) -> None:
        super(DelimitersTableView, self).__init__()
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)        
        dict_pos = container.data(4, 0).split(",")

        delimiters = cliopt[dict_pos[0]]["var"][dict_pos[2]]

        self.table_model = DelimitersTableViewModel(
            self, tree, cliopt, dict_pos, delimiters, remove_row_button_icon
        )
        self.setModel(self.table_model)
        self.clicked.connect(self.edit_table_view)
        self.pressed.connect(self.edit_table_view)

        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        settings_tree.setItemWidget(container, 0, self)
        
        self.add_row_button = QPushButton("Add Delimiter")        
        index = self.table_model.index(self.table_model.rowCount(self) - 1, 0)       
        self.setIndexWidget(index, self.add_row_button)
        self.remove_row_buttons = []
        for i in range(self.table_model.row_count - 1):
            self.remove_row_buttons.append(QPushButton())            
            self.remove_row_buttons[i].setIcon(remove_row_button_icon)
            index = self.table_model.index(i, 1)        
            self.setIndexWidget(index, self.remove_row_buttons[i])

    def dataChanged(self, topLeft, bottomRight, roles) -> None:
        print("edit complete")
        return super().dataChanged(topLeft, bottomRight, roles)

    def edit_table_view(self, index: QModelIndex):
        print("edit table")


# this is a helper class
class SettingsTreeTableMethods(object):
    ## the constructor
    def __init__(self):
        super(SettingsTreeTableMethods, self).__init__()
        SettingsTreeTableMethods.logger = self.get_child_logger(__name__)

    ## self.ui.settings_tree table functions
    def set_table_vertical_labels(self, tree, section, rows):
        vertical_label_list = []
        for i in range(1, rows + 1):
            vertical_label_list.append(str(i))
        vertical_label_list.append("")
        tree["items"][section]["QTableWidget"].setVerticalHeaderLabels(
            vertical_label_list
        )

    ## adds a row to the current table, moves the add row button down one row
    def add_settings_tree_table_row(
        self, dict_key, dict_key2, add_row_function, remove_row_button=False
    ):
        tree = self.cliOpt[dict_key]["tree"]
        table_widget = tree["items"][dict_key2]["QTableWidget"]
        add_row_button = tree["items"][dict_key2]["QTableWidgetItems"]["add row"][
            "button"
        ]
        add_row_button_item = tree["items"][dict_key2]["QTableWidgetItems"]["add row"][
            "item"
        ]
        input_cells = tree["items"]["data delimiter sequences"]["QTableWidgetItems"][
            "input cells"
        ]
        remove_row_buttons = tree["items"][dict_key2]["QTableWidgetItems"][
            "remove row buttons"
        ]
        add_row_button = QPushButton("add delimiter sequence")
        add_row_button.clicked.connect(add_row_function)
        # get current row count
        new_row = table_widget.rowCount()
        last_row = new_row - 1
        # remove add row button from last row
        table_widget.removeCellWidget(last_row, 0)
        # take the table widget item that held the add row button out of the table but dont delete it
        table_widget.takeItem(last_row, 0)
        input_cells.update({last_row: ""})
        input_cells[last_row] = QTableWidgetItem()

        table_widget.insertRow(new_row)
        input_cells[last_row].setText("")
        table_widget.setItem(last_row, 0, input_cells[last_row])
        SettingsTreeTableMethods.logger.debug(str(add_row_button_item))
        table_widget.setItem(new_row, 0, add_row_button_item)
        table_widget.setCellWidget(new_row, 0, add_row_button)
        self.set_table_vertical_labels(tree, dict_key2, new_row)

        if remove_row_button == True:
            remove_row_buttons["items"].update({last_row: ""})
            remove_row_buttons["items"][last_row] = QTableWidgetItem()
            remove_row_buttons["items"][last_row].setFlags(
                remove_row_buttons["items"][last_row].flags() | Qt.NoItemFlags
            )
            remove_row_buttons["buttons"].update({last_row: ""})
            remove_row_buttons["buttons"][last_row] = QPushButton()
            remove_row_buttons["items"][last_row].setText("")
            remove_row_buttons["buttons"][last_row].setIcon(self.ui.trashIcon)
            obj_name = (
                "remove row button,"
                + str(dict_key)
                + ","
                + str(dict_key2)
                + ","
                + str(last_row)
            )
            remove_row_buttons["buttons"][last_row].setObjectName(obj_name)
            remove_row_buttons["buttons"][last_row].clicked.connect(
                self.rem_settings_tree_table_row
            )
            tree["items"][dict_key2]["QTableWidget"].setItem(
                last_row, 1, remove_row_buttons["items"][last_row]
            )
            tree["items"][dict_key2]["QTableWidget"].setCellWidget(
                last_row, 1, remove_row_buttons["buttons"][last_row]
            )

    ## remove a row from the currently selected table in self.ui.settings_tree
    def rem_settings_tree_table_row(self):
        object_list = self.sender().objectName().split(",")
        SettingsTreeTableMethods.logger.info(str(object_list))
        tree = self.cliOpt[object_list[1]]["tree"]
        table_widget = tree["items"][object_list[2]]["QTableWidget"]
        table_widget.removeRow(int(object_list[3]))

    ## adds a row to "data delimiters"
    def add_data_delimiter_row(self):
        SettingsTreeTableMethods.logger.info("add data delimiter row")
        dict_key = "process parameters"
        dict_key2 = "data delimiter sequences"
        add_row_function = self.add_data_delimiter_row
        remove_row_button = True
        self.add_settings_tree_table_row(
            dict_key, dict_key2, add_row_function, remove_row_button
        )

    ## adds a row to "start stop data delimiters"
    def add_start_stop_data_delimiter_row(self):
        SettingsTreeTableMethods.logger.info("add start stop data delimiter row")
        dict_key = "process parameters"
        dict_key2 = "start stop data delimiter sequences"
        add_row_function = self.add_start_stop_data_delimiter_row
        remove_row_button = True
        self.add_settings_tree_table_row(
            dict_key, dict_key2, add_row_function, remove_row_button
        )

    ## edit currently selected table item
    def edit_table_widget_item(self, item):
        # this can get triggered from the QTreeWidget, or a QTreeWidgetItem and we need to know what it is
        if str(item).find("QTableWidgetItem") != -1:
            current_item = item
            item = item.tableWidget()
        else:
            current_item = item.currentItem()
        object_list = str(item.objectName()).split(",")
        SettingsTreeTableMethods.logger.info("edit item in " + object_list[2])
        self.settings_tree_button_toggles()
        item.editItem(current_item)

    ## called on field changes
    def table_widget_item_changed(self, item):
        self.settings_tree_button_toggles()
        table_widget = item.tableWidget()
        row = table_widget.row(item)
        if row == table_widget.rowCount() - 1:
            # the user added a row to the table
            return
        data = str(repr(item.data(0))).strip("'").replace("\\\\", "\\")
        object_list = table_widget.objectName().split(",")
        if data != "" and data != None:
            delim_dict = self.cliOpt[object_list[0]]["var"][object_list[2]]
            delim_dict.update({row: data})
            table_widget.blockSignals(True)
            item.setText("'" + data + "'")
            table_widget.blockSignals(False)
            self.update_code("setup.h", object_list[2], True)

    ## builds a table onto a tree widget item
    def build_tree_table_widget(
        self,
        index,
        tree,
        dict_key,
        dict_key2,
        columns,
        add_row_function,
        remove_row_button=False,
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

        table = DelimitersTableView(
            self.ui.settings_tree,
            self.cliOpt,
            tree,
            tree_widget_item,
            add_row_function,
            remove_row_button,
            self.ui.trashIcon,
        )
        # self.make_settings_tree_delimiter_table(tree, tree_widget_item, add_row_function, remove_row_button)

        # # make a table widget
        # tree["items"][dict_key2]["QTableWidget"] = QTableWidget()
        # table_widget = tree["items"][dict_key2]["QTableWidget"]
        # table_widget.setSizePolicy(
        #     QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding
        # )
        # table_widget.setSelectionMode(QAbstractItemView.SingleSelection)
        # table_header = table_widget.horizontalHeader()
        # table_widget.setObjectName(dict_pos)
        # table_widget_items = tree["items"][dict_key2]["QTableWidgetItems"]

        # if remove_row_button == True:
        #     columns += 1
        # table_widget.setColumnCount(columns)
        # table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # for i in range(0, table_widget.columnCount() - 1):
        #     table_header.setSectionResizeMode(i, QHeaderView.Stretch)
        # if remove_row_button == True:
        #     table_header.setSectionResizeMode(columns - 1, QHeaderView.ResizeToContents)
        # else:
        #     table_header.setSectionResizeMode(columns - 1, QHeaderView.Stretch)

        # delimiter_dict = self.cliOpt[dict_key]["var"][dict_key2]
        # for key in delimiter_dict:
        #     row = table_widget.rowCount()
        #     table_widget.insertRow(row)

        #     table_widget_items["input cells"].update({row: ""})
        #     table_widget_items["input cells"][row] = QTableWidgetItem()

        #     table_widget_items["input cells"][row].setText(
        #         str(repr(self.cliOpt[dict_key]["var"][dict_key2][key])).replace(
        #             "\\\\", "\\"
        #         )
        #     )
        #     table_widget.setItem(row, 0, table_widget_items["input cells"][row])

        #     if remove_row_button == True:
        #         remove_row_buttons = tree["items"][dict_key2]["QTableWidgetItems"][
        #             "remove row buttons"
        #         ]
        #         remove_row_buttons["items"].update({row: ""})
        #         remove_row_buttons["items"][row] = QTableWidgetItem()
        #         remove_row_buttons["items"][row].setFlags(
        #             remove_row_buttons["items"][row].flags() | Qt.NoItemFlags
        #         )
        #         remove_row_buttons["buttons"].update({row: ""})
        #         remove_row_buttons["buttons"][row] = QPushButton()
        #         remove_row_buttons["buttons"][row].setIcon(self.ui.trashIcon)
        #         obj_name = (
        #             "remove row button,"
        #             + str(dict_key)
        #             + ","
        #             + str(dict_key2)
        #             + ","
        #             + str(row)
        #         )
        #         remove_row_buttons["buttons"][row].setObjectName(obj_name)
        #         remove_row_buttons["buttons"][row].clicked.connect(
        #             self.rem_settings_tree_table_row
        #         )
        #         table_widget.setItem(row, 1, remove_row_buttons["items"][row])
        #         table_widget.setCellWidget(row, 1, remove_row_buttons["buttons"][row])

        # row = table_widget.rowCount()
        # table_widget.insertRow(row)

        # table_widget_items["add row"]["item"] = QTableWidgetItem()
        # table_widget_items["add row"]["button"] = QPushButton("add delimiter sequence")

        # table_widget.setItem(row, 0, table_widget_items["add row"]["item"])
        # table_widget.setCellWidget(row, 0, table_widget_items["add row"]["button"])

        # table_widget.setHorizontalHeaderLabels([dict_key2, ""])
        # vertical_label_list = []
        # for i in range(1, row + 1):
        #     vertical_label_list.append(str(i))
        # vertical_label_list.append("")
        # table_widget.setVerticalHeaderLabels(vertical_label_list)

        # table_widget_items["add row"]["button"].clicked.connect(add_row_function)
        # table_widget.itemClicked.connect(self.edit_table_widget_item)
        # table_widget.itemPressed.connect(self.edit_table_widget_item)
        # table_widget.itemChanged.connect(self.table_widget_item_changed)
        # self.ui.settings_tree.setItemWidget(tree_widget_item, 0, table_widget)

    # end settings_tree table functions


# end of file
