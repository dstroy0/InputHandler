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

    def item_changed(self, item, column):
        self.active_item = item
        
    def make_command_index(self):                
        primary_id_key = self.cliopt["commands"]["primary id key"]
        self.cliopt["commands"]["index"].update(
            {
                primary_id_key: copy.deepcopy(
                    dataModels.parameters_index_struct
                )
            }
        )
        self.cliopt["commands"]["index"][primary_id_key][
            "parameters key"
        ] = str(primary_id_key)
        self.cliopt["commands"]["index"][primary_id_key][
            "root index key"
        ] = str(primary_id_key)
        self.cliopt["commands"]["index"][primary_id_key][
            "parent index key"
        ] = str(primary_id_key)

    def add_command_to_tree(self, parent_item: QTreeWidgetItem):
        self.logger.info("adding command to tree")
        
        primary_id_key = int(self.cliopt["commands"]["primary id key"])
        number_of_commands = int(self.cliopt["commands"]["number of commands"])
                
        self.make_command_index()
        if parent_item == self.invisibleRootItem():
            item = self.build_command(parent_item)
            item.setData(1,0,str(primary_id_key))            
            self.addTopLevelItem(item)
        else:
            item = self.build_command(parent_item)
            item.setData(1,0,str(primary_id_key))
            parent_item.addChild(item)
        
        self.cliopt["commands"]["primary id key"] = str(primary_id_key + 1)
        self.cliopt["commands"]["number of commands"] = str(number_of_commands + 1)
        
    def remove_command_from_tree(self, search_string=None):
        if search_string != None:
            item_list = self.findItems(search_string, Qt.MatchExactly,0)
            if bool(item_list):
                item = item_list[0]
            else:
                self.logger.info(f"couldnt find {search_string} to remove it from the tree")
                return -1
        else:
            item = self.currentItem()
        if item == self.invisibleRootItem():
            self.logger.warning(f"cannot delete self.invisibleRootItem()!")
            return -1
        self.logger.info("removing command from tree")
                
        number_of_commands = int(self.cliopt["commands"]["number of commands"])                    
        
        def remove_children(item:QTreeWidgetItem, number_of_commands):
            if item.childCount() > 0:
                child_list = []
                list_len = item.childCount()
                for i in reversed(range(list_len)):
                    child_list.append(item.child(i))                    
                for i in range(list_len):
                    number_of_commands = clean_up(child_list[i], number_of_commands)    
            return number_of_commands
        
        def clean_up(item:QTreeWidgetItem, number_of_commands):            
            command_index = self.get_command_index(item)            
            del item            
            if command_index["parameters key"] in self.cliopt["commands"]["parameters"]:
                del self.cliopt["commands"]["parameters"][command_index["parameters key"]]            
            if command_index["parameters key"] in self.cliopt["commands"]["index"]:
                del self.cliopt["commands"]["index"][command_index["parameters key"]]
            number_of_commands -= 1
            return number_of_commands
        
        if item.parent() == self.invisibleRootItem():            
            command_index = self.get_command_index(item)
            number_of_commands = remove_children(item, number_of_commands)
            index = self.indexFromItem(item)
            item = self.takeTopLevelItem(index)
            number_of_commands = clean_up(item, number_of_commands)
        else:
            command_index = self.get_command_index(item)
            number_of_commands = remove_children(item, number_of_commands)
            parent = item.parent()
            parent.removeChild(item)
            number_of_commands = clean_up(item, number_of_commands)

        self.cliopt["commands"]["number of commands"] = str(number_of_commands)

    def get_command_index(self, item):        
        item_data = str(item.data(1, 0))
        if len(item_data) < 1:
            return -1
        else:            
            return self.cliopt["commands"]["index"][item_data]

    def build_command(self, parent_item):
        primary_id_key = int(self.cliopt["commands"]["primary id key"])
        command_index = self.cliopt["commands"]["primary id key"]
        command_parameters = self.cliopt["commands"]["parameters"][
            self.command_index[command_index]["parameters key"]
        ]
        command_string = command_parameters["commandString"]
        command_label = QTreeWidgetItem(parent_item, [command_string, ""])
        command_label.setData(1,0,str(primary_id_key))     
        command_container = QTreeWidgetItem(command_label, "")
        command_container.setData(1,0,str(primary_id_key))     
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

    def build_tree(self):
        self.logger.info("Building command tree.")
        for item in self.command_index:
            command_parameters = self.cliopt["commands"]["parameters"][
                self.cliopt["commands"]["index"][item]["parameters key"]
            ]
            command_string = command_parameters["commandString"]
            command_label = QTreeWidgetItem(
                self.invisibleRootItem(), [command_string, ""]
            )
            self.addTopLevelItem(command_label)
            command_container = QTreeWidgetItem(command_label, "")
            command_label.addChild(command_container)
            command_table = CommandParametersTableWidget(
                command_parameters,
                command_container,
                self.logger,
                self._cursor,
            )
            self.setItemWidget(command_container, 0, command_table)
            self.logger.info("adding " + command_string + " to CommandTreeWidget Root")

    def which_pressed(self):
        print("click")
        self.active_item = self.itemFromIndex(self.currentIndex())

    def which_clicked(self):
        print("press")
        self.active_item = self.itemAt(self._cursor.pos())


## self.ui.command_tree methods
class CommandTreeMethods(object):
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

    def build_command_tree(self):
        container = self.ui.command_tree_container
        container.layout = QHBoxLayout(container)
        self.command_tree = CommandTreeWidget(
            self, self.cliOpt, CommandTreeMethods.logger
        )
        container.layout.addWidget(self.command_tree)
        container.setLayout(container.layout)
        return self.command_tree

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
        self.cliOpt["commands"]["QTreeWidgetItem"]["table"][dict_index].setData(
            1, 0, dict_pos
        )
        tree_item.setData(1, 0, dict_pos)

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
        self.command_tree_button_toggles()
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
        self.command_tree_button_toggles()

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
        tree_item = self.cliOpt["commands"]["QTreeWidgetItem"]["table"][dict_index]
        table = CommandParametersTableWidget(
            command_parameters, tree_item, CommandTreeMethods.logger, self.qcursor
        )
        self.ui.command_tree.setItemWidget(tree_item, 0, table)

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
        self.command_tree_button_toggles()

    ## adds items to self.ui.command_tree for display
    # def build_command_tree(self):
    # """adds items from cliOpt to self.ui.command_tree"""
    # command_tree = self.ui.command_tree
    # command_tree.setSelectionMode(QAbstractItemView.SingleSelection)
    # # command_tree.
    # command_tree.setHeaderLabels(["Command Tree", ""])
    # command_tree.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)
    # command_tree.setColumnCount(2)
    # command_tree.setColumnHidden(1, 1)  # dict positional data
    # # make root invisible
    # self.cliOpt["commands"]["QTreeWidgetItem"][
    #     "root"
    # ] = self.ui.command_tree.invisibleRootItem()

    # self._build_command_tree()
    # self.command_tree = CommandTreeWidget(self, self.cliOpt, CommandTreeMethods.logger)
    # self.command_tree_button_toggles()


# end of file
