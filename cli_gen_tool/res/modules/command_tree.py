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

import json
from PySide6.QtWidgets import QTableView, QTreeWidgetItem, QHeaderView
from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt

from res.modules.logging_setup import Logger
from res.modules.data_models import dataModels

## specialized QAbstractTableModel for displaying InputHandler::CommandParameters elements
class CommandParametersTableViewModel(QAbstractTableModel):
    def __init__(self, parameters=None) -> None:
        super(CommandParametersTableViewModel, self).__init__()
        self.h_labels = ["Setting", "Value"]
        self.keys = list(parameters.keys())
        self.values = list(parameters.values())
        # set table length to input parameters, this will grow the table if we ever add any new configuration items
        # to the commandparameters data model
        self.row_count = len(dataModels.command_parameters_dict_keys_list)

    def columnCount(self, parent=QModelIndex()) -> int:
        return 2

    def rowCount(self, parent=QModelIndex()) -> int:
        return self.row_count

    def data(self, index, role):
        if role == Qt.DisplayRole:
            if index.column() == 0:
                return self.keys[index.row()]
            if index.column() == 1:
                return self.values[index.row()]

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self.h_labels[section])
            if orientation == Qt.Vertical:
                # label rows starting at 1
                return str(section + 1)


## self.ui.command_tree methods
class CommandTreeMethods(object):
    ## CommandTreeMethods constructor
    def __init__(self) -> None:
        super(CommandTreeMethods, self).__init__()
        CommandTreeMethods.logger = Logger.get_child_logger(self.logger, __name__)

    ## search the db for the command and remove it if exists, decrement `num_commands` (total num unique cmd param)
    # TODO remove orphaned children
    def rem_command(self, object_list):
        match = False
        for item in self.cliOpt["commands"]["parameters"]:
            for index in self.cliOpt["commands"]["index"]:
                if (
                    self.cliOpt["commands"]["index"][index][
                        "root command parameters index"
                    ]
                    == item
                ):
                    match = True
                    break
        if match == True:
            if int(self.cliOpt["var"]["num_commands"]) > 0:
                self.cliOpt["var"]["num_commands"] = str(
                    int(self.cliOpt["var"]["num_commands"]) - 1
                )                        
            self.rem_qtreewidgetitem(object_list)
            self.command_menu_button_toggles()

    ## adds a single command to the tree
    def add_qtreewidgetitem(self, parent, dict_index) -> QTreeWidgetItem:
        if dict_index == None or dict_index == "":
            if dict_index == None:
                CommandTreeMethods.logger.info("no index, unable to add item to tree")
            if dict_index == "":
                CommandTreeMethods.logger.info("user deleted a command from the tree")
                self.update_code("functions.h", "", False)
                self.update_code("functions.cpp", "", False)
                self.update_code("parameters.h", "", False)
            return        
        if dict_index not in self.cliOpt["commands"]["parameters"]:
            CommandTreeMethods.logger.info("dict_index not found")
            return
        command_parameters = self.cliOpt["commands"]["parameters"][dict_index]        
        dict_pos = (
            dict_index + "," + dict_index + "," + command_parameters["commandString"]
        )
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
        self.cliOpt["commands"]["QTreeWidgetItem"]["container"][dict_index].setData(
            1, 0, dict_pos
        )
        self.cliOpt["commands"]["QTreeWidgetItem"]["table"][dict_index].setData(
            1, 0, dict_pos
        )
        self.command_menu_button_toggles()
        # return child
        return self.cliOpt["commands"]["QTreeWidgetItem"]["table"][dict_index]

    ## takes the command out of the tree and scrub it from the data model    
    def rem_qtreewidgetitem(self, dict_pos):
        _builtin_commands = self.ih_builtins
        for (
            item
        ) in (
            _builtin_commands
        ):  # determine if the something selected is an InputHandler builtin
            if dict_pos[2] == item:
                pos = dict_pos[2]
                break
            else:
                pos = dict_pos[1]
        # take the table widget out of the qtreewidgetitem ("table")
        if pos not in self.cliOpt["commands"]["QTreeWidgetItem"]["table"]:
            CommandTreeMethods.logger.info("qtreewidgetitem not in dict")
            return
        self.ui.command_tree.removeItemWidget(
            self.cliOpt["commands"]["QTreeWidgetItem"]["table"][pos], 0
        )
        tree_item = self.cliOpt["commands"]["QTreeWidgetItem"]["container"][pos]        
        #tree_item.removeChild(self.cliOpt["commands"]["QTreeWidgetItem"]["table"][pos])
        # remove children
        # TODO scrub children from data model
        children = []
        for child in range(tree_item.childCount()):        
            children.append(tree_item.child(child))
        for child in children:
            tree_item.removeChild(child)        
        self.cliOpt["commands"]["QTreeWidgetItem"]["root"].removeChild(tree_item)
        
        # scrub the data model
        if pos in self.cliOpt["commands"]["QTableView"]["models"]:
            del self.cliOpt["commands"]["QTableView"]["models"][pos]
        if pos in self.cliOpt["commands"]["QTableView"]:
            del self.cliOpt["commands"]["QTableView"][pos]
        if pos in self.cliOpt["commands"]["parameters"]:
            del self.cliOpt["commands"]["parameters"][pos]
        if pos in self.cliOpt["commands"]["QTreeWidgetItem"]["container"]:
            del self.cliOpt["commands"]["QTreeWidgetItem"]["container"][pos]
        if pos in self.cliOpt["commands"]["QTreeWidgetItem"]["table"]:
            del self.cliOpt["commands"]["QTreeWidgetItem"]["table"][pos]
        for item in self.cliOpt["commands"]["index"]:
            if self.cliOpt["commands"]["index"][item]["index key"] == pos:
                CommandTreeMethods.logger.info(
                    str(
                        "removing command index struct "
                        + str(item)
                        + " "
                        + str(json.dumps(self.cliOpt["commands"]["index"][item], indent=2))
                    )
                )
                del self.cliOpt["commands"]["index"][item]
                break
        self.rebuild_command_tree()

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

    ## private method used by public methods rebuild_command_tree and build_command_tree
    def _build_command_tree(self):
        for item in self.cliOpt["commands"]["index"]:
            if bool(self.cliOpt["commands"]["index"][item]["indices of children"]):
                children = len(
                    self.cliOpt["commands"]["index"][item]["indices of children"]
                )
            else:
                children = 0
            if children == 0:
                self.add_qtreewidgetitem(
                    self.cliOpt["commands"]["QTreeWidgetItem"]["root"],
                    self.cliOpt["commands"]["index"][item][
                        "root command parameters index"
                    ],
                )
            else:
                # command root
                parent = self.add_qtreewidgetitem(
                    self.cliOpt["commands"]["QTreeWidgetItem"]["root"],
                    self.cliOpt["commands"]["index"][item][
                        "root command parameters index"
                    ],
                )
                # command children
                for child in item["indices of children"]:
                    self.add_qtreewidgetitem(
                        parent,
                        child,
                    )
        _root = self.cliOpt["commands"]["QTreeWidgetItem"]["root"]
        _root.setExpanded(True)

    ## rebuilds the command tree from scratch
    def rebuild_command_tree(self):
        command_tree = self.ui.command_tree
        # empty entire tree of items
        command_tree.clear()
        self.cliOpt["commands"]["QTreeWidgetItem"]["root"] = QTreeWidgetItem(
            command_tree, ["Root", ""]
        )
        self._build_command_tree()
        self.command_menu_button_toggles()

    ## adds items to self.ui.command_tree for display
    def build_command_tree(self):
        command_tree = self.ui.command_tree
        command_tree.setHeaderLabels(["Command Tree", ""])
        command_tree.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        command_tree.setColumnCount(2)
        command_tree.setColumnHidden(1, 1)  # dict positional data
        self.cliOpt["commands"]["QTreeWidgetItem"]["root"] = QTreeWidgetItem(
            self.ui.command_tree, ["Root", ""]
        )

        self._build_command_tree()
        self.command_menu_button_toggles()


# end of file
