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
from PySide6.QtWidgets import (
    QTableView,
    QTreeWidgetItem,
    QHeaderView,
    QWidget,
    QSplitter,
    QHBoxLayout,
    QSizePolicy,
    QAbstractScrollArea,
)
from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt

from modules.display_models import displayModels
from modules.logging_setup import Logger
from modules.data_models import dataModels
from modules.display_models import displayModels


class CommandParametersArgumentsTableViewModel(QAbstractTableModel):
    def __init__(self, parameters: dict) -> None:
        super(CommandParametersArgumentsTableViewModel, self).__init__()
        self.keys = list(parameters.keys())
        self.values = list(parameters.values())
        arg_start = 0
        for i in range(len(self.keys)):
            if self.keys[i] == "commandArguments":
                arg_start = i
                break
        self.args_list = []
        for i in range(arg_start, len(self.values)):
            self.args_list.append(self.values[i])

        self.h_label = "Arguments"
        self.arguments = self.args_list
        self.column_count = 1
        self.row_count = int(-(-(len(self.arguments)) // (self.column_count)))
        self.matrix = []
        input_idx = 0
        for i in range(self.row_count):
            row_list = []
            for j in range(self.column_count):
                if input_idx >= len(self.arguments):
                    row_list.append(" ")
                else:
                    row_list.append(self.arguments[input_idx])
                    input_idx += 1
            self.matrix.append(row_list)

    def columnCount(self, parent=QModelIndex()) -> int:
        """property

        Args:
            parent (QModelIndex, optional): The model index. Defaults to QModelIndex().

        Returns:
            int: The number of columns.
        """
        return self.column_count

    def rowCount(self, parent=QModelIndex()) -> int:
        """property

        Args:
            parent (QModelIndex, optional): The model index. Defaults to QModelIndex().

        Returns:
            int: The number of rows.
        """
        return self.row_count

    def data(self, index: QModelIndex, role: int):
        """Table data positioning.

        Args:
            index (QModelIndex): The model index.
            role (Qt Role): What role is the data.

        Returns:
            str: data in the cell
        """

        if role == Qt.DisplayRole:
            return self.matrix[index.row()][index.column()]
        if role == Qt.ToolTipRole:
            return "Tooltip ph"

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
            if orientation == Qt.Horizontal:
                return self.h_label
            elif orientation == Qt.Vertical:
                return str(section + 1)


## specialized QAbstractTableModel for displaying InputHandler::CommandParameters elements
class CommandParametersTableViewModel(QAbstractTableModel):
    """Display model for the parameters table

    Args:
        QAbstractTableModel (class): This class specializes QAbstractTableModel
    """

    def __init__(self, parameters: dict = None) -> None:
        """constructor method

        Args:
            parameters (dict, optional): Set placeholder text in CommandParametersDialog input fields. Defaults to None.
        """
        super(CommandParametersTableViewModel, self).__init__()
        self.h_labels = ["Setting", "Value", "Setting", "Value", "Setting", "Value"]

        self.keys = list(parameters.keys())
        self.values = list(parameters.values())
        self.tooltip = displayModels._command_table_tooltip_list
        self.tooltip_idx = 0
        self.row_count = int(
            -(
                -(len(dataModels.command_parameters_dict_keys_list) - 1)
                // (len(self.h_labels) / 2)
            )
        )
        self.column_count = int(len(self.h_labels))
        self.input = []
        arg_start = 0
        for i in range(len(self.keys)):
            if self.keys[i] != "commandArguments":
                self.input.append(self.keys[i])
                self.input.append(self.values[i])
            else:
                arg_start = i
        self.args_list = []
        for i in range(arg_start, len(self.values)):
            self.args_list.append(self.values[i])
        self.matrix = []
        input_idx = 0
        for i in range(self.row_count):
            row_list = []
            for j in range(self.column_count):
                if input_idx > len(self.input) - 1:
                    row_list.append("")
                else:
                    row_list.append(self.input[input_idx])
                    input_idx += 1
            self.matrix.append(row_list)

    def columnCount(self, parent=QModelIndex()) -> int:
        """property

        Args:
            parent (QModelIndex, optional): The model index. Defaults to QModelIndex().

        Returns:
            int: The number of columns.
        """
        return self.column_count

    def rowCount(self, parent=QModelIndex()) -> int:
        """property

        Args:
            parent (QModelIndex, optional): The model index. Defaults to QModelIndex().

        Returns:
            int: The number of rows.
        """
        return self.row_count

    def data(self, index: QModelIndex, role: int):
        """Table data positioning.

        Args:
            index (QModelIndex): The model index.
            role (Qt Role): What role is the data.

        Returns:
            str: data in the cell
        """
        if role == Qt.DisplayRole:
            if self.matrix[index.row()][index.column()] == "":
                return ""
            return str(self.matrix[index.row()][index.column()])
        if role == Qt.ToolTipRole:
            retval = self.tooltip[self.tooltip_idx]
            if (self.tooltip_idx) >= len(self.tooltip):
                self.tooltip_idx = 0
            else:
                self.tooltip_idx += 1
            return str(retval)

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
            if orientation == Qt.Horizontal:
                return self.h_labels[section]


## self.ui.command_tree methods
class CommandTreeMethods(object):
    ## CommandTreeMethods constructor
    def __init__(self) -> None:
        super(CommandTreeMethods, self).__init__()
        CommandTreeMethods.logger = Logger.get_child_logger(self.logger, __name__)

    ## search the db for the command and remove it if exists, decrement `number of commands` (total num unique cmd param)
    # TODO remove orphaned children
    def rem_command(self, object_list):
        match = False
        for item in self.cliOpt["commands"]["parameters"]:
            for index in self.cliOpt["commands"]["index"]:
                if self.cliOpt["commands"]["index"][index]["root index key"] == item:
                    match = True
                    break
        if match == True:
            if int(self.cliOpt["var"]["number of commands"]) > 0:
                self.cliOpt["var"]["number of commands"] = str(
                    int(self.cliOpt["var"]["number of commands"]) - 1
                )
            self.rem_qtreewidgetitem(object_list)
            self.command_menu_button_toggles()

    ## adds a single command to the tree
    def add_qtreewidgetitem(self, parent, dict_index) -> QTreeWidgetItem:
        # error checking
        if dict_index == None:
            CommandTreeMethods.logger.info("no index, unable to add item to tree")
            return
        elif dict_index == "" and self.loading == True:
            CommandTreeMethods.logger.info(
                "loaded saved command"
            )
            return
        elif dict_index == "" and self.loading == False:
            CommandTreeMethods.logger.info(
                "user deleted a command from the tree"
            )
            self.update_code("functions.h", "", False)
            self.update_code("functions.cpp", "", False)
            self.update_code("parameters.h", "", False)
            return        
        elif dict_index not in self.cliOpt["commands"]["parameters"]:
            CommandTreeMethods.logger.info("dict_index not found: " + str(dict_index))
            return
        # end error checking
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
        return self.cliOpt["commands"]["QTreeWidgetItem"]["container"][dict_index]

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
        
        # TODO scrub children
        children = []
        for child in range(tree_item.childCount()):
            children.append(tree_item.child(child))
        for child in children:
            tree_item.removeChild(child)
        self.cliOpt["commands"]["QTreeWidgetItem"]["root"].removeChild(tree_item)

        # scrub the data model
        if pos in self.cliOpt["commands"]["QTableView"]["models"]["arguments"]:
            del self.cliOpt["commands"]["QTableView"]["models"]["arguments"][pos]
        if pos in self.cliOpt["commands"]["QTableView"]["models"]["parameters"]:
            del self.cliOpt["commands"]["QTableView"]["models"]["parameters"][pos]
        if pos in self.cliOpt["commands"]["QTableView"]["tables"]["parameters"]:
            del self.cliOpt["commands"]["QTableView"]["tables"]["parameters"][pos]
        if pos in self.cliOpt["commands"]["QTableView"]["tables"]["arguments"]:
            del self.cliOpt["commands"]["QTableView"]["tables"]["arguments"][pos]
        if pos in self.cliOpt["commands"]["parameters"]:
            del self.cliOpt["commands"]["parameters"][pos]
        if pos in self.cliOpt["commands"]["QTreeWidgetItem"]["container"]:
            del self.cliOpt["commands"]["QTreeWidgetItem"]["container"][pos]
        if pos in self.cliOpt["commands"]["QTreeWidgetItem"]["table"]:
            del self.cliOpt["commands"]["QTreeWidgetItem"]["table"][pos]
        for item in self.cliOpt["commands"]["index"]:
            if self.cliOpt["commands"]["index"][item]["parameters key"] == pos:
                CommandTreeMethods.logger.info(
                    str(
                        "removing command index struct "
                        + str(item)
                        + " "
                        + str(
                            json.dumps(self.cliOpt["commands"]["index"][item], indent=2)
                        )
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

        self.cliOpt["commands"]["QTableView"]["container"] = QWidget()
        self.cliOpt["commands"]["QTableView"]["layout"] = QHBoxLayout()
        self.cliOpt["commands"]["QTableView"]["splitter"] = QSplitter()

        container = self.cliOpt["commands"]["QTableView"]["container"]
        container_layout = self.cliOpt["commands"]["QTableView"]["layout"]
        container_splitter = self.cliOpt["commands"]["QTableView"]["splitter"]

        self.cliOpt["commands"]["QTableView"]["models"]["parameters"][
            dict_index
        ] = CommandParametersTableViewModel(command_parameters)

        self.cliOpt["commands"]["QTableView"]["models"]["arguments"][
            dict_index
        ] = CommandParametersArgumentsTableViewModel(command_parameters)

        self.cliOpt["commands"]["QTableView"]["tables"]["parameters"][
            dict_index
        ] = QTableView()
        self.cliOpt["commands"]["QTableView"]["tables"]["arguments"][
            dict_index
        ] = QTableView()

        table_view = self.cliOpt["commands"]["QTableView"]["tables"]["parameters"][
            dict_index
        ]
        table_view.setModel(
            self.cliOpt["commands"]["QTableView"]["models"]["parameters"][dict_index]
        )
        table_view.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        table_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table_view.verticalHeader().setDefaultAlignment(Qt.AlignCenter)
        table_view.resizeColumnsToContents()

        table_view = self.cliOpt["commands"]["QTableView"]["tables"]["arguments"][
            dict_index
        ]
        table_view.setModel(
            self.cliOpt["commands"]["QTableView"]["models"]["arguments"][dict_index]
        )
        table_view.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        table_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        table_view.horizontalHeader().setFixedWidth(150)
        table_view.verticalHeader().setDefaultAlignment(Qt.AlignCenter)
        table_view.resizeColumnsToContents()

        container_splitter.addWidget(
            self.cliOpt["commands"]["QTableView"]["tables"]["parameters"][dict_index]
        )
        container_splitter.addWidget(
            self.cliOpt["commands"]["QTableView"]["tables"]["arguments"][dict_index]
        )
        container_layout.addWidget(container_splitter)
        container.setLayout(container_layout)

        command_tree.setItemWidget(tree_item, 0, container)

    def _add_command_children(self, item):
        for index in range(
            len(self.cliOpt["commands"]["index"][item]["child index key list"])
        ):
            parent = self.cliOpt["commands"]["QTreeWidgetItem"]["container"][
            self.cliOpt["commands"]["index"][item]["parameters key"]
        ]
            child_index = self.cliOpt["commands"]["index"][item][
                "child index key list"
            ][index]
            self.add_qtreewidgetitem(
                parent,
                self.cliOpt["commands"]["index"][child_index]["parameters key"],
            )

    ## private method used by public methods rebuild_command_tree and build_command_tree
    def _build_command_tree(self):
        parent_index = self.cliOpt["commands"]["index"]
        for item in parent_index:
            if bool(self.cliOpt["commands"]["index"][item]["child index key list"]):
                children = len(
                    self.cliOpt["commands"]["index"][item]["child index key list"]
                )
            else:
                children = 0
            if children == 0:
                self.add_qtreewidgetitem(
                    self.cliOpt["commands"]["QTreeWidgetItem"]["root"],
                    self.cliOpt["commands"]["index"][item]["root index key"],
                )
            else:
                # command root
                self.add_qtreewidgetitem(
                    self.cliOpt["commands"]["QTreeWidgetItem"]["root"],
                    self.cliOpt["commands"]["index"][item]["root index key"],
                )
                self._add_command_children(item)

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
