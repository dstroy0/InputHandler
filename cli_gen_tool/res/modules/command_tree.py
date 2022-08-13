##
# @file command_tree.py
# @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
# @brief MainWindow external methods
# @version 1.0
# @date 2022-07-30
# @copyright Copyright (c) 2022
# Copyright (C) 2022 Douglas Quigg (dstroy0) <dquigg123@gmail.com>
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 3 as published by the Free Software Foundation.

from __future__ import absolute_import

from PySide6.QtWidgets import QTableView, QTreeWidgetItem, QHeaderView
from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt

from res.modules.logging_setup import Logger


class CommandParametersTableViewModel(QAbstractTableModel):
    def __init__(self, parameters=None) -> None:
        super(CommandParametersTableViewModel, self).__init__()
        self.h_labels = ["Setting", "Value"]
        self.keys = list(parameters.keys())
        self.values = list(parameters.values())
        self.gen_table()

    def gen_table(self):
        self.row_count = 12

    def columnCount(self, parent=QModelIndex()) -> int:
        return 2

    def rowCount(self, parent=QModelIndex()) -> int:
        return self.row_count

    def data(self, index, role):
        if role == Qt.DisplayRole:
            if index.column() == 0:
                return self.keys[index.row() - 1]
            if index.column() == 1:
                return self.values[index.row() - 1]

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self.h_labels[section])


# command_tree methods
class CommandTreeMethods(object):
    def __init__(self) -> None:
        super(CommandTreeMethods, self).__init__()
        CommandTreeMethods.logger = Logger.get_child_logger(self.logger, __name__)

    def add_qtreewidgetitem(self, parent, dict_index=None) -> None:
        if dict_index == None:
            dict_index = str(self.cliOpt["var"]["num_commands"])
        command_parameters = self.cliOpt["commands"]["parameters"][dict_index]
        self.cliOpt["commands"]["QTreeWidgetItem"][dict_index] = QTreeWidgetItem(
            parent, [command_parameters["commandString"], ""]
        )
        tree_item = self.cliOpt["commands"]["QTreeWidgetItem"][dict_index]
        self.build_command_parameters_table_view(
            dict_index, tree_item, command_parameters
        )

    def rem_qtreewidgetitem(self, dict_pos):
        self.ui.command_tree.removeItemWidget(
            self.cliOpt["commands"]["QTreeWidgetItem"][dict_pos[2]], 0
        )
        if dict_pos[2] in self.cliOpt["commands"]["QTableView"]["models"]:
            del self.cliOpt["commands"]["QTableView"]["models"][dict_pos[2]]
        if dict_pos[2] in self.cliOpt["commands"]["QTableView"]:
            del self.cliOpt["commands"]["QTableView"][dict_pos[2]]
        if dict_pos[2] in self.cliOpt["commands"]["parameters"]:
            del self.cliOpt["commands"]["parameters"][dict_pos[2]]
        if dict_pos[2] in self.cliOpt["commands"]["QTreeWidgetItem"]:
            del self.cliOpt["commands"]["QTreeWidgetItem"][dict_pos[2]]

    def build_command_parameters_table_view(
        self, dict_index, tree_item, command_parameters
    ):
        command_tree = self.ui.command_tree
        tree_item = self.cliOpt["commands"]["QTreeWidgetItem"][dict_index]
        self.cliOpt["commands"]["QTableView"]["models"][
            dict_index
        ] = CommandParametersTableViewModel(command_parameters)
        self.cliOpt["commands"]["QTableView"][dict_index] = QTableView()
        table_view = self.cliOpt["commands"]["QTableView"][dict_index]
        table_view.setModel(self.cliOpt["commands"]["QTableView"]["models"][dict_index])
        table_view.resizeColumnsToContents()
        command_tree.setItemWidget(tree_item, 0, table_view)

    def build_command_tree(self):
        command_tree = self.ui.command_tree
        command_tree.setHeaderLabels(["Command Tree", ""])
        command_tree.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        command_tree.setColumnCount(2)
        command_tree.setColumnHidden(1, 1)  # dict positional data


# end of file
