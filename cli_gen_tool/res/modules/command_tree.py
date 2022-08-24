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


## specialized QAbstractTableModel for displaying InputHandler::CommandParameters elements
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
            if orientation == Qt.Vertical:
                return str(section)


## self.ui.command_tree methods
class CommandTreeMethods(object):
    ## CommandTreeMethods constructor
    def __init__(self) -> None:
        super(CommandTreeMethods, self).__init__()
        CommandTreeMethods.logger = Logger.get_child_logger(self.logger, __name__)

    ## search the db for the command and remove it if exists, decrement `num_commands` (total num unique cmd param)
    def rem_command(self, object_list):
        match = False
        for item in self.cliOpt["commands"]["parameters"]:
            for index in self.cliOpt["command parameters index"]:
                if (
                    self.cliOpt["command parameters index"][index]["parameters key"]
                    == item
                ):
                    match = True
                    break
        if match == True:
            if int(self.cliOpt["var"]["num_commands"]) > 0:
                self.cliOpt["var"]["num_commands"] -= 1
            del item
            del self.cliOpt["commands"]["parameters"][object_list[2]]
            self.rem_qtreewidgetitem(object_list)

    ## adds a single command to the tree
    def add_qtreewidgetitem(self, parent, dict_index) -> None:
        if dict_index == None:
            CommandTreeMethods.logger.info("no index, unable to add item to tree")
            return
        command_parameters = self.cliOpt["commands"]["parameters"][dict_index]
        self.cliOpt["commands"]["QTreeWidgetItem"]["container"][
            dict_index
        ] = QTreeWidgetItem(parent, [command_parameters["commandString"], ""])
        self.cliOpt["commands"]["QTreeWidgetItem"]["table"][
            dict_index
        ] = QTreeWidgetItem(
            self.cliOpt["commands"]["QTreeWidgetItem"]["container"][dict_index]
        )
        tree_item = self.cliOpt["commands"]["QTreeWidgetItem"]["container"][dict_index]
        self.build_command_parameters_table_view(
            dict_index, tree_item, command_parameters
        )

    ## takes the command out of the tree and scrub it from the data model
    # TODO remove orphaned children if a parent item is removed
    def rem_qtreewidgetitem(self, dict_pos):
        # take the table widget out of the qtreewidgetitem ("table")
        self.ui.command_tree.removeItemWidget(
            self.cliOpt["commands"]["QTreeWidgetItem"]["table"][dict_pos[2]], 0
        )
        # this is the tree "container", it displays the commandString and expands to view the command parameters table
        tree_item = self.cliOpt["commands"]["QTreeWidgetItem"]["container"][dict_pos[2]]
        # returns the int index of the top level item
        idx = self.ui.command_tree.indexOfTopLevelItem(tree_item)
        # get the qtreewidgetitem that is at the top
        item = self.ui.command_tree.takeTopLevelItem(idx)
        # delete it from the tree
        del item
        # scrub the data model
        if dict_pos[2] in self.cliOpt["commands"]["QTableView"]["models"]:
            del self.cliOpt["commands"]["QTableView"]["models"][dict_pos[2]]
        if dict_pos[2] in self.cliOpt["commands"]["QTableView"]:
            del self.cliOpt["commands"]["QTableView"][dict_pos[2]]
        if dict_pos[2] in self.cliOpt["commands"]["parameters"]:
            del self.cliOpt["commands"]["parameters"][dict_pos[2]]
        if dict_pos[2] in self.cliOpt["commands"]["QTreeWidgetItem"]["container"]:
            del self.cliOpt["commands"]["QTreeWidgetItem"]["container"][dict_pos[2]]
        if dict_pos[2] in self.cliOpt["commands"]["QTreeWidgetItem"]["table"]:
            del self.cliOpt["commands"]["QTreeWidgetItem"]["table"][dict_pos[2]]

    ## builds a table view for a command using a custom model and populates it with the command's parameters
    def build_command_parameters_table_view(
        self, dict_index, tree_item, command_parameters
    ):
        command_tree = self.ui.command_tree
        tree_item = self.cliOpt["commands"]["QTreeWidgetItem"]["table"][dict_index]
        self.cliOpt["commands"]["QTableView"]["models"][
            dict_index
        ] = CommandParametersTableViewModel(command_parameters)
        self.cliOpt["commands"]["QTableView"][dict_index] = QTableView()
        table_view = self.cliOpt["commands"]["QTableView"][dict_index]
        table_view.setModel(self.cliOpt["commands"]["QTableView"]["models"][dict_index])
        table_view.verticalHeader().setDefaultAlignment(Qt.AlignCenter)
        table_view.resizeColumnsToContents()
        command_tree.setItemWidget(tree_item, 0, table_view)

    ## adds items to self.ui.command_tree for display
    def build_command_tree(self):
        command_tree = self.ui.command_tree
        command_tree.setHeaderLabels(["Command Tree", ""])
        command_tree.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        command_tree.setColumnCount(2)
        command_tree.setColumnHidden(1, 1)  # dict positional data
        # TODO load child commands
        for item in self.cliOpt["command parameters index"]:
            if self.cliOpt["command parameters index"][item]["is root command"] == True:
                self.add_qtreewidgetitem(
                    self.ui.command_tree,
                    self.cliOpt["command parameters index"][item]["parameters key"],
                )


# end of file
