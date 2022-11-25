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

import json, copy
from PySide6.QtWidgets import (
    QTableView,
    QTreeWidgetItem,
    QHeaderView,
    QWidget,
    QSplitter,
    QHBoxLayout,
    QSizePolicy,
    QAbstractScrollArea,
    QAbstractItemView,
)
from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt

from modules.display_models import displayModels
from modules.data_models import dataModels
from modules.display_models import displayModels


class CommandParametersArgumentsTableViewModel(QAbstractTableModel):
    """Command Tree arguments pane view model

    Args:
        QAbstractTableModel (class): This is the model used to construct the arguments QTableView
    """

    def __init__(self, parameters: dict) -> None:
        """Constructor method

        Args:
            parameters (dict): Dictionary of arguments
        """
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
    """All methods related to command tree manipulation

    Args:
        object (class): base class

    Returns:
        None: None
    """

    ## CommandTreeMethods constructor
    def __init__(self) -> None:
        """constructor method"""
        super(CommandTreeMethods, self).__init__()
        CommandTreeMethods.logger = self.get_child_logger(__name__)

        self.ui.new_cmd_button.setEnabled(False)
        # edit button
        self.ui.edit_cmd_button.setEnabled(False)
        # delete button
        self.ui.delete_cmd_button.setEnabled(False)

        tree_buttons = copy.deepcopy(dataModels.button_dict)
        tree_buttons["buttons"].update(
            {
                "new": copy.deepcopy(dataModels.button_sub_dict),
                "edit": copy.deepcopy(dataModels.button_sub_dict),
                "delete": copy.deepcopy(dataModels.button_sub_dict),
                "collapse": copy.deepcopy(dataModels.button_sub_dict),
            }
        )
        tree_buttons["buttons"]["new"]["QPushButton"] = self.ui.new_cmd_button
        tree_buttons["buttons"]["edit"]["QPushButton"] = self.ui.edit_cmd_button
        tree_buttons["buttons"]["delete"]["QPushButton"] = self.ui.delete_cmd_button
        tree_buttons["buttons"]["collapse"][
            "QPushButton"
        ] = self.ui.command_tree_collapse_button
        tree_buttons["buttons"]["collapse"]["enabled"] = True
        self.command_tree_buttons = tree_buttons        

    ## adds a single command to the tree
    def add_qtreewidgetitem(
        self, parent: QTreeWidgetItem, dict_index: str
    ) -> QTreeWidgetItem:
        """Adds QTreeWidgetItem at dict_index as a child to parent QTreeWidgetItem

        Args:
            parent (QTreeWidgetItem): The parent QTreeWidgetItem
            dict_index (str): the location of the child in the data model

        Returns:
            QTreeWidgetItem: the created QTreeWidgetItem on success, None on fail.
        """
        # error checking
        if dict_index == None:
            CommandTreeMethods.logger.info("no index, unable to add item to tree")
            return None
        elif dict_index == "" and self.loading == True:
            CommandTreeMethods.logger.info("loaded saved command ")
            return None
        elif dict_index == "" and self.loading == False:
            CommandTreeMethods.logger.info("user deleted a command from the tree")
            self.update_code("functions.h", "", False)
            self.update_code("functions.cpp", "", False)
            self.update_code("parameters.h", "", False)
            return None
        elif dict_index not in self.cliOpt["commands"]["parameters"]:
            CommandTreeMethods.logger.info("dict_index not found: " + str(dict_index))
            return None
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
        tree_item.setExpanded(True)

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
        if self.loading:
            CommandTreeMethods.logger.info(
                "added saved command `"
                + command_parameters["commandString"]
                + "` to the command tree"
            )
        else:
            CommandTreeMethods.logger.info(
                "user added command `"
                + command_parameters["commandString"]
                + "` to the command tree"
            )
        self.update_code("functions.h", command_parameters["commandString"], True)
        self.update_code("functions.cpp", command_parameters["commandString"], True)
        self.update_code("parameters.h", command_parameters["commandString"], True)
        # return child
        return self.cliOpt["commands"]["QTreeWidgetItem"]["container"][dict_index]

    ## scrubs command from data model
    def scrub_command_from_datamodel(
        self, pos: str, tree_item: QTreeWidgetItem
    ) -> None:
        """Removes everything related to the command from the display and data models

        Args:
            pos (str): position in self.cliOpt
            tree_item (QTreeWidgetItem): the tree item to be removed
        """
        # scrub the data model
        if pos in self.cliOpt["commands"]["parameters"]:
            command = self.cliOpt["commands"]["parameters"][pos]["commandString"]
            CommandTreeMethods.logger.info(
                "removing `" + command + "` from the command tree"
            )

        if tree_item != None:
            parent_treewidgetitem = self.cliOpt["commands"]["QTreeWidgetItem"]["root"]
            parent_treewidgetitem.removeChild(tree_item)

        if pos in self.cliOpt["commands"]["QTableView"]["models"]["arguments"]:
            del self.cliOpt["commands"]["QTableView"]["models"]["arguments"][pos]
        if pos in self.cliOpt["commands"]["QTableView"]["models"]["parameters"]:
            del self.cliOpt["commands"]["QTableView"]["models"]["parameters"][pos]
        if pos in self.cliOpt["commands"]["QTableView"]["tables"]["parameters"]:
            del self.cliOpt["commands"]["QTableView"]["tables"]["parameters"][pos]
        if pos in self.cliOpt["commands"]["QTableView"]["tables"]["arguments"]:
            del self.cliOpt["commands"]["QTableView"]["tables"]["arguments"][pos]
        if pos in self.cliOpt["commands"]["QTableView"]["container"]:
            del self.cliOpt["commands"]["QTableView"]["container"][pos]
        if pos in self.cliOpt["commands"]["QTableView"]["layout"]:
            del self.cliOpt["commands"]["QTableView"]["layout"][pos]
        if pos in self.cliOpt["commands"]["QTableView"]["splitter"]:
            del self.cliOpt["commands"]["QTableView"]["splitter"][pos]
        if str(pos) in self.cliOpt["commands"]["parameters"]:
            del self.cliOpt["commands"]["parameters"][str(pos)]
        if pos in self.cliOpt["commands"]["QTreeWidgetItem"]["container"]:
            del self.cliOpt["commands"]["QTreeWidgetItem"]["container"][pos]
        if pos in self.cliOpt["commands"]["QTreeWidgetItem"]["table"]:
            del self.cliOpt["commands"]["QTreeWidgetItem"]["table"][pos]
        if (
            pos in self.cliOpt["commands"]["index"]
            and self.cliOpt["commands"]["index"][pos]["parameters key"] == pos
        ):
            CommandTreeMethods.logger.debug(
                str(
                    "removing command index struct "
                    + str(pos)
                    + " "
                    + str(json.dumps(self.cliOpt["commands"]["index"][pos], indent=2))
                )
            )
            del self.cliOpt["commands"]["index"][pos]
        self.update_code("functions.h", "", False)
        self.update_code("functions.cpp", "", False)
        self.update_code("setup.cpp", "", False)
        self.update_code("parameters.h", "", False)

    ## rem_qtreewidgetitem wrapper deprecated
    def rem_command(self, object_list: list):
        """self.rem_qtreewidgetitem wrapper; deprecated

        Args:
            object_list (list): position of command in self.cliOpt
        """
        self.rem_qtreewidgetitem(object_list)
        self.prompt_to_save = True
        self.windowtitle_set = False
        self.set_main_window_title()
        self.command_menu_button_toggles()

    # TODO fix rem_qtreewidgetitem
    ## takes the command out of the tree and scrubs it from the data model and removes its QTreeWidgetItem from self.ui.command_tree
    def rem_qtreewidgetitem(self, dict_pos: str) -> None:
        """removes QTreeWidgetItem and associated structures from cliOpt at dict_pos

        Args:
            dict_pos (str): cliOpt key
        """

        def pop_from_dict(pos, tree_item):
            match = False
            for _item in self.cliOpt["commands"]["index"]:
                if (
                    self.cliOpt["commands"]["index"][_item]["parameters key"]
                    == dict_pos[2]
                ):
                    match = True
                    break
            if match == True:
                result = self.cliOpt["commands"]["index"].pop(_item, None)
            else:
                result = self.cliOpt["commands"]["index"].pop(pos, None)
            if result != None:
                # the number of commands is equal to the len of the commands index
                self.cliOpt["var"]["number of commands"] = str(
                    len(self.cliOpt["commands"]["index"])
                )
                CommandTreeMethods.logger.info(
                    "removed key " + _item + ' from self.cliOpt["commands"]["index"]'
                )
            self.scrub_command_from_datamodel(pos, tree_item)
            # the number of commands is equal to the len of the commands index
            self.cliOpt["var"]["number of commands"] = str(
                len(self.cliOpt["commands"]["index"])
            )

        pos = dict_pos[1]
        if pos in self.cliOpt["commands"]["QTreeWidgetItem"]["container"]:
            tree_item = self.cliOpt["commands"]["QTreeWidgetItem"]["container"][pos]
        else:
            CommandTreeMethods.logger.info(
                "couldnt find QTreeWidgetItem for `" + str(pos) + "`"
            )
            tree_item = None

        # take the table widget out of the qtreewidgetitem ("table")
        if pos not in self.cliOpt["commands"]["QTreeWidgetItem"]["table"]:
            CommandTreeMethods.logger.info("qtreewidgetitem not in dict")
            return
        self.ui.command_tree.removeItemWidget(
            self.cliOpt["commands"]["QTreeWidgetItem"]["table"][pos], 0
        )

        children = []
        if pos in self.cliOpt["commands"]["index"]:
            child_list = self.cliOpt["commands"]["index"][pos]["child index key list"]
        else:
            pop_from_dict(pos, tree_item)
            return
        child_positions = [pos]
        pos_idx = 0
        prev_pos_idx = 0
        if bool(child_list):
            CommandTreeMethods.logger.info("looking for command children")
        else:
            pop_from_dict(pos, tree_item)
            return
        index_struct = self.cliOpt["commands"]["index"][pos]
        if index_struct["root index key"] == index_struct["parent index key"]:
            this_parent_index_key = self.cliOpt["commands"]["index"][pos][
                "parent index key"
            ]
            this_parent_index_struct = self.cliOpt["commands"]["index"][
                this_parent_index_key
            ]
            if pos in this_parent_index_struct["child index key list"]:
                this_parent_index_struct["child index key list"].remove(pos)
                CommandTreeMethods.logger.debug(
                    "pruning child "
                    + str(pos)
                    + " from child index key list of index "
                    + str(this_parent_index_key)
                )
        while bool(child_list):
            for item in child_list:
                if item in self.cliOpt["commands"]["QTreeWidgetItem"]["container"]:
                    child_treewidgetitem = self.cliOpt["commands"]["QTreeWidgetItem"][
                        "container"
                    ][item]
                    children.append(child_treewidgetitem)
                    child_positions.append(item)
                    pos_idx += 1
            child_list = self.cliOpt["commands"]["index"][child_positions[pos_idx]][
                "child index key list"
            ]
            if not bool(child_list):
                CommandTreeMethods.logger.info("no more command children found")
                break
            # increment sentinel breaks the loop if no more children are located and appended to [children]
            if pos_idx == prev_pos_idx:
                break
            else:
                prev_pos_idx = pos_idx

        # prune children
        for child in children:
            _object_list = child.data(1, 0).split(",")
            index = self.cliOpt["commands"]["index"]
            child_index = index[_object_list[1]]
            parent_index_key = child_index["parent index key"]
            if parent_index_key in index:
                parent_index = index[parent_index_key]
                parent_child_list = parent_index["child index key list"]
                if _object_list[1] in parent_child_list:
                    parent_child_list.remove(
                        _object_list[1]
                    )  # remove this child from the parent's list of children
            tree_item.removeChild(child)

        # remove children from cliOpt starting with the farthest leaf from Root
        for item in reversed(child_positions):
            pop_from_dict(item, tree_item)

    ## builds a table view for a command using a custom model and populates it with the command's parameters
    def build_command_parameters_table_view(
        self, dict_index: str, tree_item: QTreeWidgetItem, command_parameters: dict
    ):
        """builds a table view for the QTreeWidgetItem at dict_index using command_parameters

        Args:
            dict_index (str): location in cliOpt
            tree_item (QTreeWidgetItem): the QTreeWidgetItem
            command_parameters (dict): command parameters dict
        """
        command_tree = self.ui.command_tree
        tree_item = self.cliOpt["commands"]["QTreeWidgetItem"]["table"][dict_index]

        self.cliOpt["commands"]["QTableView"]["container"].update(
            {dict_index: QWidget()}
        )
        self.cliOpt["commands"]["QTableView"]["layout"].update(
            {dict_index: QHBoxLayout()}
        )
        self.cliOpt["commands"]["QTableView"]["splitter"].update(
            {dict_index: QSplitter()}
        )

        container = self.cliOpt["commands"]["QTableView"]["container"][dict_index]
        container_layout = self.cliOpt["commands"]["QTableView"]["layout"][dict_index]
        container_splitter = self.cliOpt["commands"]["QTableView"]["splitter"][
            dict_index
        ]

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
        table_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        table_view.verticalHeader().setDefaultAlignment(Qt.AlignCenter)
        table_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        table_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        table_view.resizeColumnsToContents()

        table_view = self.cliOpt["commands"]["QTableView"]["tables"]["arguments"][
            dict_index
        ]
        table_view.setModel(
            self.cliOpt["commands"]["QTableView"]["models"]["arguments"][dict_index]
        )
        table_view.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        table_view.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.MinimumExpanding)
        table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        table_view.verticalHeader().setDefaultAlignment(Qt.AlignCenter)
        table_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
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

    ## private method used by public methods rebuild_command_tree and build_command_tree
    def _build_command_tree(self):
        """private method called by self.build_command_tree and self.rebuild_command_tree"""
        parent_index = self.cliOpt["commands"]["index"]
        for item in parent_index:
            # command root
            if (
                self.cliOpt["commands"]["index"][item]["parameters key"]
                == self.cliOpt["commands"]["index"][item]["root index key"]
                == self.cliOpt["commands"]["index"][item]["parent index key"]
            ):
                CommandTreeMethods.logger.info(
                    "adding "
                    + self.cliOpt["commands"]["parameters"][
                        self.cliOpt["commands"]["index"][item]["parameters key"]
                    ]["commandString"]
                    + " to self.ui.command_tree Root"
                )
                self.add_qtreewidgetitem(
                    self.cliOpt["commands"]["QTreeWidgetItem"]["root"],
                    self.cliOpt["commands"]["index"][item]["root index key"],
                )
            else:  # child command
                CommandTreeMethods.logger.info(
                    "adding "
                    + self.cliOpt["commands"]["parameters"][item]["commandString"]
                    + " to self.ui.command_tree, child of: "
                    + self.cliOpt["commands"]["parameters"][
                        self.cliOpt["commands"]["index"][item]["parent index key"]
                    ]["commandString"]
                )
                self.add_qtreewidgetitem(
                    self.cliOpt["commands"]["QTreeWidgetItem"]["container"][
                        self.cliOpt["commands"]["index"][item]["parent index key"]
                    ],
                    self.cliOpt["commands"]["index"][item]["parameters key"],
                )

    ## rebuilds the command tree from scratch
    def rebuild_command_tree(self):
        """clears self.ui.command_tree and rebuilds from scratch"""
        command_tree = self.ui.command_tree
        # empty entire tree of items
        command_tree.clear()
        self.cliOpt["commands"]["QTreeWidgetItem"][
            "root"
        ] = self.ui.command_tree.invisibleRootItem()
        self._build_command_tree()
        command_tree.setExpanded(True)
        self.command_menu_button_toggles()

    ## adds items to self.ui.command_tree for display
    def build_command_tree(self):
        """adds items from cliOpt to self.ui.command_tree"""
        command_tree = self.ui.command_tree
        command_tree.setSelectionMode(QAbstractItemView.SingleSelection)
        # command_tree.
        command_tree.setHeaderLabels(["Command Tree", ""])
        command_tree.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        command_tree.setColumnCount(2)
        command_tree.setColumnHidden(1, 1)  # dict positional data
        # make root invisible
        self.cliOpt["commands"]["QTreeWidgetItem"][
            "root"
        ] = self.ui.command_tree.invisibleRootItem()

        self._build_command_tree()
        self.command_menu_button_toggles()


# end of file
