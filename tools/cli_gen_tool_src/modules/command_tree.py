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

# absolute imports
from __future__ import absolute_import
from modules.display_models import displayModels
from modules.data_models import dataModels

# imports
import copy
import json
from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PySide6.QtWidgets import (
    QTableView,
    QTreeWidget,
    QTreeWidgetItem,
    QHeaderView,
    QWidget,
    QSplitter,
    QHBoxLayout,
    QSizePolicy,
    QAbstractItemView,
)

# TODO
class CommandParametersArgumentsTableViewModel(QAbstractTableModel):
    def __init__(self, parent, parameters: dict) -> None:
        super(CommandParametersArgumentsTableViewModel, self).__init__()
        self._parent = parent
        self.editing = False
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

    def flags(self, index) -> Qt.ItemFlags:
        if index.isValid() and self.h_label[index.column()] == "Arguments":
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

            # clean_value = value.strip("<>")
            # if not clean_value:
            #     return False
            # self.cliopt[self.dict_pos[0]]["var"][self.dict_pos[2]][
            #     str(index.row())
            # ] = clean_value
            # self.dataChanged.emit(index, index)
            # table = self._parent.objectName().split(",")[2]
            # self._parent.logger.info(
            #     f"{table} table, row {index.row()+1} data changed to <{clean_value}>"
            # )
        return True

    def columnCount(self, parent=QModelIndex()) -> int:
        return self.column_count

    def rowCount(self, parent=QModelIndex()) -> int:
        return self.row_count

    def data(self, index: QModelIndex, role: int):
        if role == Qt.DisplayRole:
            return self.matrix[index.row()][index.column()]
        if role == Qt.ToolTipRole:
            return "Tooltip ph"

    def headerData(self, section: int, orientation: int, role: int):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.h_label
            elif orientation == Qt.Vertical:
                return str(section + 1)

    def edit_table_view(self, index: QModelIndex):
        if index.isValid() and self.editing == False:
            self.editing = True
            self._parent.setCurrentIndex(index)
            self._parent.edit(index)


# TODO
class CommandParametersTableViewModel(QAbstractTableModel):
    def __init__(self, parent, parameters: dict = None) -> None:
        super(CommandParametersTableViewModel, self).__init__()
        self.parameters = parameters
        self._parent = parent
        self.h_labels = ["Setting", "Value", "Setting", "Value", "Setting", "Value"]
        self.editing = False
        self.keys = list(parameters.keys())
        self.values = list(parameters.values())
        self.tooltip_dict = displayModels.command_table_tooltip_dict
        self.tt_keys = list(self.tooltip_dict.keys())
        self.tt_values = list(self.tooltip_dict.values())
        self.tt_input = []
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
            self.tt_input.append(self.tt_keys[i])
            self.tt_input.append(self.tt_values[i])
            if self.keys[i] != "commandArguments":
                self.input.append(self.keys[i])
                self.input.append(self.values[i])
            else:
                arg_start = i
        self.args_list = []
        for i in range(arg_start, len(self.values)):
            self.args_list.append(self.values[i])

        # make display matrices
        self.tt_matrix = []
        self.matrix = []
        input_idx = 0
        for i in range(self.row_count):
            row_list = []
            tt_row_list = []
            for j in range(self.column_count):
                if input_idx > len(self.input) - 1:
                    tt_row_list.append("")
                    row_list.append("")
                else:
                    tt_row_list.append(self.tt_input[input_idx])
                    row_list.append(self.input[input_idx])
                    input_idx += 1
            self.matrix.append(row_list)
            self.tt_matrix.append(tt_row_list)

    def flags(self, index) -> Qt.ItemFlags:
        if index.isValid() and self.h_labels[index.column()] == "Value":
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

            if not index.isValid():
                return False

            type_index = self.index(index.row(), index.column() - 1)
            parameter_type = self.data(type_index, Qt.DisplayRole)

            # data model
            self.parameters[parameter_type] = value
            # internal table model
            self.matrix[index.row()][index.column()] = value
            # emit this signal to update the display
            self.dataChanged.emit(index, index)

            command = self.parameters["commandString"]
            self._parent.logger.info(
                f"User edited command <{command}>; <{parameter_type}> changed to <{value}>"
            )
        return True

    def columnCount(self, parent=QModelIndex()) -> int:
        return self.column_count

    def rowCount(self, parent=QModelIndex()) -> int:
        return self.row_count

    def data(self, index: QModelIndex, role: int):
        if not index.isValid():
            return None
        if role == Qt.DisplayRole or role == Qt.EditRole:
            return str(self.matrix[index.row()][index.column()])
        if role == Qt.ToolTipRole:
            return str(self.tt_matrix[index.row()][index.column()])

    def headerData(self, section: int, orientation: int, role: int):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.h_labels[section]

    def edit_table_view(self, index: QModelIndex):
        if index.isValid() and self.editing == False:
            self.editing = True
            self._parent.setCurrentIndex(index)
            self._parent.edit(index)


# TODO
class CommandParametersTableView(QTableView):
    def __init__(self, logger, cursor, command_parameters, tree_item) -> None:
        super(CommandParametersTableView, self).__init__()
        self.logger = logger
        self.cursor_ = cursor
        self.tree_item = tree_item
        # dict_pos = self.tree_item.data(1, 0).split(",")
        # self.setObjectName(str(self.tree_item.data(1, 0)))

        self.parameters = command_parameters
        self.table_model = CommandParametersTableViewModel(self, self.parameters)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setModel(self.table_model)

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


class CommandParametersArgumentsTableView(QTableView):
    def __init__(self, logger, cursor, command_parameters, tree_item) -> None:
        super(CommandParametersArgumentsTableView, self).__init__()
        self.tree_item = tree_item
        self.logger = logger
        self.cursor_ = cursor

        # dict_pos = self.tree_item.data(1, 0).split(",")
        # self.setObjectName(str(self.tree_item.data(1, 0)))

        self.parameters = command_parameters
        self.table_model = CommandParametersArgumentsTableViewModel(
            self, self.parameters
        )
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.setMaximumSize(150, 16777215)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setModel(self.table_model)

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


class CommandParametersTableWidget(QWidget):
    """Command parameters table container

    Args:
        QWidget (object): Base class that is specialized
    """

    def __init__(self, command_parameters, tree_item, logger, cursor) -> None:
        """constructor method

        Args:
            command_parameters (dict): command parameters dictionary
            tree_item (QTreeWidgetItem): parent container
            logger (logger): method logger
            cursor (QCursor): mouse cursor
        """
        super(CommandParametersTableWidget, self).__init__()
        self.parameters = command_parameters
        self.tree_item = tree_item
        self.widget_layout = QHBoxLayout(self)
        self.splitter = QSplitter(self)

        self.parameters_view = CommandParametersTableView(
            logger, cursor, self.parameters, self.tree_item
        )
        self.arguments_view = CommandParametersArgumentsTableView(
            logger, cursor, self.parameters, self.tree_item
        )

        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        self.splitter.addWidget(self.parameters_view)
        self.splitter.addWidget(self.arguments_view)
        self.widget_layout.addWidget(self.splitter)
        self.splitter.setSizes(
            [
                self.parameters_view.sizeHint().width(),
                self.arguments_view.sizeHint().width(),
            ]
        )
        self.setLayout(self.widget_layout)


class CommandTreeWidget(QTreeWidget, QTreeWidgetItem):
    def __init__(self, parent, cliopt, logger) -> None:
        super(CommandTreeWidget, self).__init__()
        self.setParent(parent.ui.command_tree_container)
        self._parent = parent
        self.cliopt = cliopt
        self.active_item = None
        self._cursor = parent.qcursor
        self.logger = logger
        self.setColumnCount(2)
        self.setColumnHidden(1, 1)
        self.command_index = cliopt["commands"]["index"]
        self.setHeaderLabel("Command Tree")
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)

        self.build_tree()

        self.clicked.connect(self.which_clicked)
        self.pressed.connect(self.which_pressed)
        self.itemChanged.connect(self.item_changed)
        self.currentItemChanged.connect(self.item_changed)
        self.itemSelectionChanged.connect(self._parent.command_tree_button_toggles)
        self.itemClicked.connect(self._parent.command_tree_button_toggles)
        self.itemCollapsed.connect(self._parent.command_tree_button_toggles)
        self.itemExpanded.connect(self._parent.command_tree_button_toggles)

    def build_tree(self):
        self.logger.info("Building command tree.")

        def populate_children(parent, index):
            if bool(self.command_index[index]["child index key list"]):
                for child_index in self.command_index[index]["child index key list"]:
                    child_command = self.add_command_to_tree(parent)
                    if bool(self.command_index[child_index]["child_index_key_list"]):
                        populate_children(child_command, child_index)

        for root_command_index in self.command_index:
            root_command = self.add_command_to_tree(self.invisibleRootItem())
            populate_children(root_command, root_command_index)

    def add_command_to_tree(self, parent_item: QTreeWidgetItem):
        self.logger.info("adding command to tree")

        primary_id_key = int(self.cliopt["commands"]["primary id key"])
        number_of_commands = int(self.cliopt["commands"]["number of commands"])

        self.make_command_index()
        if parent_item == self.invisibleRootItem():
            item = self.build_command(parent_item)
            item.setData(1, 0, str(primary_id_key))
            self.addTopLevelItem(item)
        else:
            item = self.build_command(parent_item)
            item.setData(1, 0, str(primary_id_key))
            parent_item.addChild(item)

        self.cliopt["commands"]["primary id key"] = str(primary_id_key + 1)
        self.cliopt["commands"]["number of commands"] = str(number_of_commands + 1)
        return item

    def build_command(self, parent_item):
        primary_id_key = int(self.cliopt["commands"]["primary id key"])
        command_index = self.cliopt["commands"]["primary id key"]
        command_parameters = self.cliopt["commands"]["parameters"][
            self.command_index[command_index]["parameters key"]
        ]
        command_string = command_parameters["commandString"]
        command_label = QTreeWidgetItem(parent_item, [command_string, ""])
        command_label.setData(1, 0, str(primary_id_key))
        command_container = QTreeWidgetItem(command_label, "")
        command_container.setData(1, 0, str(primary_id_key))
        command_label.addChild(command_container)
        command_table = CommandParametersTableWidget(
            command_parameters,
            command_container,
            self.logger,
            self._cursor,
        )
        self.setItemWidget(command_container, 0, command_table)
        self.logger.info("adding " + command_string + " to CommandTreeWidget Root")
        return command_label

    def item_changed(self, item, column):
        self.active_item = item

    def make_command_index(self):
        primary_id_key = self.cliopt["commands"]["primary id key"]
        self.cliopt["commands"]["index"].update(
            {primary_id_key: copy.deepcopy(dataModels.parameters_index_struct)}
        )
        self.cliopt["commands"]["index"][primary_id_key]["parameters key"] = str(
            primary_id_key
        )
        self.cliopt["commands"]["index"][primary_id_key]["root index key"] = str(
            primary_id_key
        )
        self.cliopt["commands"]["index"][primary_id_key]["parent index key"] = str(
            primary_id_key
        )

    def remove_command_from_tree(self, search_string=None):
        if search_string != None:
            item_list = self.findItems(search_string, Qt.MatchExactly, 0)
            if bool(item_list):
                item = item_list[0]
            else:
                self.logger.info(
                    f"couldnt find {search_string} to remove it from the tree"
                )
                return -1
        else:
            item = self.active_item

        if item == self.invisibleRootItem():
            self.logger.warning(f"cannot delete self.invisibleRootItem()!")
            return -1
        self.logger.info("removing command from tree")

        number_of_commands = int(self.cliopt["commands"]["number of commands"])

        def remove_children(item: QTreeWidgetItem, number_of_commands):
            if item.childCount() > 0:
                child_list = []
                list_len = item.childCount()
                for i in reversed(range(list_len)):
                    child_list.append(item.child(i))
                for i in range(list_len):
                    number_of_commands = clean_up(child_list[i], number_of_commands)
            return number_of_commands

        def clean_up(item: QTreeWidgetItem, number_of_commands):
            command_index = self.get_command_index(item)
            del item
            if command_index["parameters key"] in self.cliopt["commands"]["parameters"]:
                del self.cliopt["commands"]["parameters"][
                    command_index["parameters key"]
                ]
            if command_index["parameters key"] in self.cliopt["commands"]["index"]:
                del self.cliopt["commands"]["index"][command_index["parameters key"]]
            number_of_commands -= 1
            return number_of_commands

        if item.parent() == self.invisibleRootItem():
            index = self.indexFromItem(item)
            item = self.takeTopLevelItem(index)
            number_of_commands = remove_children(item, number_of_commands)
        else:
            parent = item.parent()
            if parent == None:
                parent = self.invisibleRootItem()
            number_of_commands = remove_children(item, number_of_commands)
            parent.removeChild(item)

        self.cliopt["commands"]["number of commands"] = str(number_of_commands)

    def get_command_index(self, item):
        item_data = str(item.data(1, 0))
        print(item_data)
        if len(item_data) < 1:
            return -1
        else:
            return self.cliopt["commands"]["index"][item_data]

    def which_pressed(self):
        print("click")
        self.active_item = self.itemFromIndex(self.currentIndex())
        print(self.active_item)

    def which_clicked(self):
        print("press")
        self.active_item = self.itemFromIndex(self.currentIndex())
        print(self.active_item)


## self.ui.command_tree methods
class CommandTreeMethods(object):
    ## CommandTreeMethods constructor
    def __init__(self) -> None:
        """constructor method"""
        super(CommandTreeMethods, self).__init__()
        CommandTreeMethods.logger = self.get_child_logger(__name__)

        # new cmd button
        self.ui.new_cmd_button.setEnabled(False)
        # edit button
        self.ui.edit_cmd_button.setEnabled(False)
        # delete button
        self.ui.delete_cmd_button.setEnabled(False)

        self.command_tree_buttons = copy.deepcopy(dataModels.button_dict)
        self.command_tree_buttons["buttons"].update(
            {
                "new": copy.deepcopy(dataModels.button_sub_dict),
                "edit": copy.deepcopy(dataModels.button_sub_dict),
                "delete": copy.deepcopy(dataModels.button_sub_dict),
                "collapse": copy.deepcopy(dataModels.button_sub_dict),
            }
        )
        self.command_tree_buttons["buttons"]["new"][
            "QPushButton"
        ] = self.ui.new_cmd_button
        self.command_tree_buttons["buttons"]["edit"][
            "QPushButton"
        ] = self.ui.edit_cmd_button
        self.command_tree_buttons["buttons"]["delete"][
            "QPushButton"
        ] = self.ui.delete_cmd_button
        self.command_tree_buttons["buttons"]["collapse"][
            "QPushButton"
        ] = self.ui.command_tree_collapse_button
        self.command_tree_buttons["buttons"]["collapse"]["enabled"] = True

    def build_command_tree(self):
        container = self.ui.command_tree_container
        container.layout = QHBoxLayout(container)
        self.command_tree = CommandTreeWidget(
            self, self.cliOpt, CommandTreeMethods.logger
        )
        container.layout.addWidget(self.command_tree)
        container.setLayout(container.layout)
        return self.command_tree


# end of file
