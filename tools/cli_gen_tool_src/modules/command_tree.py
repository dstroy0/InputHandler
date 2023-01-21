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
from collections import OrderedDict
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import Qt, QByteArray
from PySide6.QtWidgets import (
    QTreeWidget,
    QTreeWidgetItem,
    QHeaderView,
    QWidget,
    QSplitter,
    QHBoxLayout,
    QSizePolicy,
    QAbstractItemView,
    QTableWidget,
    QTableWidgetItem,
    QMenu,
    QDialogButtonBox,
    QStyle,
    QDialog,
)


class CommandParametersPTableWidget(QTableWidget, object):
    def __init_subclass__(cls) -> None:

        return super(CommandParametersPTableWidget, cls).__init_subclass__()

    def build_table(cls, command_parameters):
        cls.prm = copy.deepcopy(command_parameters)
        cls.prm.pop("commandArguments")
        rows = int((len(cls.prm) * 2) / 6)
        cls.setColumnCount(6)
        cls.setRowCount(rows)
        cls.setHorizontalHeaderLabels(
            [
                "Setting",
                "Value",
                "Setting",
                "Value",
                "Setting",
                "Value",
            ]
        )
        cls.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        cls.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        r = 0
        c = 0
        for key in cls.prm:
            setting_item = QTableWidgetItem()
            setting_item.setData(0, key)
            setting_item.setToolTip(displayModels.command_table_tooltip_dict[key])
            setting_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            setting_item.setFlags(setting_item.flags() & ~Qt.ItemIsEditable)
            cls.setItem(r, c, setting_item)
            c += 1
            value_item = QTableWidgetItem()
            value_item.setData(0, cls.prm[key])
            value_item.setToolTip(displayModels.command_table_tooltip_dict[key])
            value_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            value_item.setFlags(value_item.flags() & ~Qt.ItemIsEditable)
            cls.setItem(r, c, value_item)
            c += 1
            if c > cls.columnCount():
                r += 1
                c = 0


class CommandParametersArgumentsTableWidget(QTableWidget, object):
    def __init_subclass__(cls) -> None:
        return super(CommandParametersArgumentsTableWidget, cls).__init_subclass__()

    def build_table(cls, command_parameters):
        cls.args_list = cls.parse_commandarguments_string(
            command_parameters["commandArguments"]
        )
        table = cls
        table.clear()
        table.setColumnCount(1)
        table.setHorizontalHeaderLabels(["type"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setRowCount(len(cls.args_list))
        table.setMinimumWidth(150)
        table.setMaximumWidth(175)
        for r in range(len(cls.args_list)):
            type_item = QTableWidgetItem()
            type_item.setData(0, cls.args_list[r])
            type_item.setToolTip(
                displayModels.argument_table_tooltip_dict[cls.args_list[r]]
            )
            type_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            table.setItem(r, 0, type_item)

    def parse_commandarguments_string(self, args: str) -> list:
        args_list = copy.deepcopy(args)
        args_list = args_list.replace("UITYPE::", "")
        args_list = args_list.replace("{", "")
        args_list = args_list.replace("}", "")
        args_list = args_list.replace(" ", "")
        args_list = args_list.replace("\n", "")
        args_list = args_list.split(",")
        return args_list


class CommandParametersTableWidget(QWidget):
    """Command parameters table container

    Args:
        QWidget (object): Base class that is specialized
    """

    def __init__(self, command_parameters, tree_item, logger, cursor, builtins) -> None:
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

        self.parameters_view = CommandParametersPTableWidget()
        self.parameters_view.build_table(self.parameters)

        self.arguments_view = CommandParametersArgumentsTableWidget()
        self.arguments_view.build_table(self.parameters)

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
        self.active_builtins = []
        self._settings_tree = None
        self._parent = parent
        self.ih_builtins = self._parent.ih_builtins
        self.cliopt = cliopt
        self.active_item = self.invisibleRootItem()
        self._cursor = self._parent.qcursor
        self.create_qdialog = self._parent.create_qdialog
        self.logger = logger
        self.command_index = cliopt["commands"]["index"]
        self.loading_index = 0
        self.setColumnCount(2)
        self.setColumnHidden(1, 1)
        self.setHeaderLabel("Command Tree")
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_customContextMenuRequested)
        self.build_tree()
        self.clicked.connect(self.which_clicked)
        self.pressed.connect(self.which_pressed)
        self.itemChanged.connect(self.item_changed)
        self.currentItemChanged.connect(self.item_changed)
        self.itemSelectionChanged.connect(self._parent.command_tree_button_toggles)
        self.itemClicked.connect(self._parent.command_tree_button_toggles)
        self.itemCollapsed.connect(self._parent.command_tree_button_toggles)
        self.itemExpanded.connect(self._parent.command_tree_button_toggles)

    def on_customContextMenuRequested(self, pos):
        self._pos = pos
        menu = QMenu(self)
        item_title = self.get_parent_item(self.itemAt(pos)).data(0, 0)
        collapseAction = QAction(f"collapse {item_title}", self)
        collapseAction.triggered.connect(self.collapseAt)
        deleteAction = QAction(f"delete {item_title}")
        deleteAction.triggered.connect(self.deleteAt)
        editAction = QAction(f"edit {item_title}")
        editAction.triggered.connect(self.editAt)
        menu.addAction(collapseAction)
        menu.addAction(editAction)
        menu.addAction(deleteAction)
        menu.exec(self.mapToGlobal(pos))
        return super().customContextMenuRequested

    def collapseAt(self):
        index = self.indexFromItem(self.get_parent_item(self.itemAt(self._pos)))
        self.collapse(index)

    def deleteAt(self):
        item = self.itemAt(self._pos)
        item_title = self.get_parent_item(item).data(0, 0)
        self.active_item = item
        b = QDialogButtonBox.StandardButton
        buttons = [b.Ok, b.Close]
        button_text = ["Yes", "No"]
        result = self.create_qdialog(
            f"remove {item_title} from tree?",
            Qt.AlignCenter,
            Qt.NoTextInteraction,
            "Deleting command",
            buttons,
            button_text,
            QStyle.StandardPixmap.SP_MessageBoxCritical,
            self._parent.qscreen,
        )
        if result == QDialog.Accepted:
            self.remove_command_from_tree()

    def editAt(self):
        item = self.itemAt(self._pos)
        item_title = self.get_parent_item(item).data(0, 0)
        self.active_item = item
        self._parent.clicked_edit_tab_two()

    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key_Escape:
            self.selectionModel().clearSelection()
        if event.key() == Qt.Key_Delete:
            if self.active_item:
                item_title = self.get_parent_item(self.active_item).data(0, 0)
                b = QDialogButtonBox.StandardButton
                buttons = [b.Ok, b.Close]
                button_text = ["Yes", "No"]
                result = self.create_qdialog(
                    f"remove {item_title} from tree?",
                    Qt.AlignCenter,
                    Qt.NoTextInteraction,
                    "Deleting command",
                    buttons,
                    button_text,
                    QStyle.StandardPixmap.SP_MessageBoxCritical,
                    self._parent.qscreen,
                )
                if result == QDialog.Accepted:
                    self.remove_command_from_tree()
        if event.key() in (Qt.Key_Enter, Qt.Key_Return):
            if self.active_item:
                self._parent.clicked_edit_tab_two()
        return super().keyPressEvent(event)

    def mouseDoubleClickEvent(self, event) -> None:
        if self.active_item:
            self._parent.clicked_edit_tab_two()
        return super().mouseDoubleClickEvent(event)

    def make_builtin_parameters(self, builtin: str = None) -> dict:
        if builtin == "listCommands":
            list_commands = OrderedDict()
            list_commands = dict(
                zip(
                    dataModels.command_parameters_dict_keys_list,
                    dataModels.LCcmdParam,
                )
            )
            return list_commands
        if builtin == "listSettings":
            list_settings = OrderedDict()
            list_settings = dict(
                zip(
                    dataModels.command_parameters_dict_keys_list,
                    dataModels.LScmdParam,
                )
            )
            return list_settings
        return {}

    def saveState(self):
        items = self.findItems("*", Qt.MatchWrap | Qt.MatchWildcard | Qt.MatchRecursive)
        current_selected = ""
        expanded_state = []
        state = {"selected item": current_selected, "expanded": expanded_state}
        state_index = 0
        for item in items:
            if item.isSelected():
                state["selected item"] = state_index
            if item.isExpanded():
                state["expanded"].append(True)
            else:
                state["expanded"].append(False)
            state_index += 1
        b = json.dumps(state, indent=2).encode("utf-8")
        return QByteArray(b)

    def restoreState(self, b: QByteArray):
        items = self.findItems("*", Qt.MatchWrap | Qt.MatchWildcard | Qt.MatchRecursive)
        state = json.loads(b.data())
        state_index = 0
        for item in items:
            if state_index == state["selected item"]:
                self.setCurrentItem(item)
                self.active_item = item
            if state_index < len(state["expanded"]):
                if state["expanded"][state_index] == True:
                    item.setExpanded(True)
                else:
                    item.setExpanded(False)
            else:
                break
            state_index += 1

    def get_settings_tree(self):
        self._settings_tree = self._parent.settings_tree

    def build_tree(self):
        self.logger.info("Building command tree.")

        def populate_children(parent, index):
            if bool(self.command_index[index]["child index key list"]):
                for child_index in self.command_index[index]["child index key list"]:
                    child_command = self.add_command_to_tree(parent)
                    if bool(self.command_index[child_index]["child index key list"]):
                        populate_children(child_command, child_index)

        for root_command_index in self.command_index:
            # only populates root commands with their children, because
            # self.command_index is flat, not a matrix
            if int(self.command_index[root_command_index]["root index key"]) == int(
                self.command_index[root_command_index]["parameters key"]
            ):
                root_command = self.add_command_to_tree(self.invisibleRootItem())
                populate_children(root_command, root_command_index)

    def add_command_to_tree(
        self, parent_item: QTreeWidgetItem, builtin: str = None
    ) -> QTreeWidgetItem:

        item = self.build_command(parent_item, builtin)
        self.active_item = item

        if self._parent.loading == False and self._parent.prompt_to_save == False:
            item.setExpanded(True)
            self.setCurrentItem(item)
            self._parent.prompt_to_save = True
            self._parent.windowtitle_set = False
        return item

    def build_command(self, parent_item, builtin: str = None):
        if builtin != None:
            if builtin in self.active_builtins:
                return None

        if self._parent.loading:
            if len(self.command_index) - 1 >= int(self.loading_index):
                command_index = str(
                    list(self.command_index.keys())[int(self.loading_index)]
                )
            else:
                self.make_command_index(parent_item)
                command_index = str(
                    list(self.command_index.keys())[int(self.loading_index)]
                )
            self.cliopt["commands"]["primary id key"] = command_index
            primary_id_key = command_index
            if int(self.loading_index) < len(list(self.command_index.keys())):
                self.loading_index = str(int(self.loading_index) + 1)
        else:
            command_index = str(self.cliopt["commands"]["primary id key"])
            primary_id_key = command_index
            if primary_id_key not in self.cliopt["commands"]["index"]:
                self.make_command_index(parent_item)

        if builtin != None:
            self.active_builtins.append(builtin)
            self.cliopt["commands"]["parameters"].update(
                {
                    self.cliopt["commands"][
                        "primary id key"
                    ]: self.make_builtin_parameters(builtin)
                }
            )

        if parent_item == None:
            parent_item = self.active_item
            if parent_item == None:
                parent_item = self.invisibleRootItem()

        command_parameters = self.cliopt["commands"]["parameters"][
            self.command_index[command_index]["parameters key"]
        ]
        command_string = command_parameters["commandString"]

        command_label = QTreeWidgetItem(parent_item, [command_string, ""])
        command_label.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        command_label.setData(1, 0, str(primary_id_key))
        command_container = QTreeWidgetItem(command_label, "")
        command_container.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        command_container.setData(1, 0, str(primary_id_key))
        command_label.addChild(command_container)

        command_table = CommandParametersTableWidget(
            command_parameters,
            command_container,
            self.logger,
            self._cursor,
            self._parent.ih_builtins,
        )

        self.setItemWidget(command_container, 0, command_table)

        if parent_item == self.invisibleRootItem():
            self.addTopLevelItem(command_label)
            command_label.setExpanded(True)
            parent_string = "Root"
        else:
            item = self.active_item
            item.addChild(command_label)
            command_label.setExpanded(True)
            parent_string = parent_item.data(0, 0)

        self.cliopt["commands"]["primary id key"] = str(int(int(primary_id_key) + 1))
        # if not self._parent.loading:
        number_of_commands = self.cliopt["commands"]["number of commands"]
        self.cliopt["commands"]["number of commands"] = str(
            int(int(number_of_commands) + 1)
        )

        self.logger.info(f"added {command_string} to CommandTreeWidget {parent_string}")

        self._parent.update_code("README.md", command_string, True)
        self._parent.update_code("CLI.h", command_string, True)
        self._parent.update_code("functions.h", command_string, True)
        self._parent.update_code("parameters.h", command_string, True)

        return command_label

    def item_changed(self, item, column):
        self.active_item = item

    def make_command_index(self, parent_item):
        primary_id_key = self.cliopt["commands"]["primary id key"]
        self.cliopt["commands"]["index"].update(
            {primary_id_key: copy.deepcopy(dataModels.parameters_index_struct)}
        )

        if parent_item == self.invisibleRootItem() or parent_item == None:
            self.cliopt["commands"]["index"][primary_id_key]["parameters key"] = str(
                primary_id_key
            )
            self.cliopt["commands"]["index"][primary_id_key]["root index key"] = str(
                primary_id_key
            )
            self.cliopt["commands"]["index"][primary_id_key]["parent index key"] = str(
                primary_id_key
            )
        else:
            parent_index = self.get_command_index(parent_item)
            self.cliopt["commands"]["index"][primary_id_key]["parameters key"] = str(
                primary_id_key
            )
            self.cliopt["commands"]["index"][primary_id_key]["root index key"] = str(
                parent_index["root index key"]
            )
            self.cliopt["commands"]["index"][primary_id_key]["parent index key"] = str(
                parent_item.data(1, 0)
            )
            parent_index["child index key list"].append(primary_id_key)

    def remove_command_from_tree(self, search_string=None):
        if (
            search_string in self.ih_builtins
            and search_string not in self.active_builtins
        ):
            self.logger.info(f"{search_string} not in command tree")
            return -1

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
            item = self.get_parent_item(self.active_item)

        number_of_commands = int(self.cliopt["commands"]["number of commands"])

        if item == self.invisibleRootItem():
            self.logger.warning(f"cannot delete self.invisibleRootItem()!")
            return -1

        def remove_children(item: QTreeWidgetItem, number_of_commands):
            if item.childCount() > 0:
                child_list = []
                list_len = item.childCount()
                for i in range(list_len):
                    child_list.append(item.child(i))
                for i in reversed(range(list_len)):
                    if item.child(i).childCount() > 0:
                        remove_children(item.child(i), number_of_commands)
                    number_of_commands = clean_up(child_list[i], number_of_commands)
            else:
                number_of_commands = clean_up(item, number_of_commands)
            return number_of_commands

        def clean_up(item: QTreeWidgetItem, number_of_commands):
            command_index = self.get_command_index(item)
            if command_index == -1:
                return number_of_commands
            if (
                command_index["parameters key"]
                in self.command_index[command_index["parent index key"]][
                    "child index key list"
                ]
            ):
                self.command_index[command_index["parent index key"]][
                    "child index key list"
                ].remove(command_index["parameters key"])
            command_string = self.cliopt["commands"]["parameters"][
                command_index["parameters key"]
            ]["commandString"]
            self.logger.info(f"removing {command_string} from command tree")
            if item != self.invisibleRootItem():
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
        if self._parent.loading == False and self._parent.prompt_to_save == False:
            self._parent.prompt_to_save = True
            self._parent.windowtitle_set = False

        # switch off builtin
        if item.data(0, 0) in self.active_builtins:
            self.active_builtins.remove(item.data(0, 0))
            item_list = self._settings_tree.findItems(
                str(item.data(0, 0)), Qt.MatchRecursive | Qt.MatchExactly, 1
            )
            cmb_item = item_list[0]
            self._settings_tree.setCurrentItem(cmb_item)
            cmb = self._settings_tree.itemWidget(cmb_item, 3)
            self._settings_tree.setCurrentItem(item)
            cmb.setCurrentIndex(cmb.findText("Disabled"))
            self.cliopt["builtin methods"]["var"][item.data(0, 0)] = False

        self._parent.update_code("README.md", item.data(0, 0), True)
        self._parent.update_code("CLI.h", item.data(0, 0), True)
        self._parent.update_code("functions.h", item.data(0, 0), True)
        self._parent.update_code("parameters.h", item.data(0, 0), True)
        self.cliopt["commands"]["number of commands"] = str(number_of_commands)

    def get_parent_item(self, item: QTreeWidgetItem):
        if item:
            if item.data(0, 0) != None and item.data(1, 0) != None:
                return item
            else:
                return item.parent()

    def get_child_item(self, item: QTreeWidgetItem):
        if item:
            if item.data(0, 0) == None and item.data(1, 0) != None:
                return item
            elif (
                item.data(1, 0) != None
                and item.data(1, 0) != None
                and item.childCount() > 0
            ):
                return item.child(0)

    def get_command_index(self, item):
        item_data = str(item.data(1, 0))
        if len(item_data) < 1:
            return -1
        elif item_data not in self.cliopt["commands"]["index"]:
            return -1
        else:
            return self.cliopt["commands"]["index"][item_data]

    def which_pressed(self):
        self.active_item = self.itemFromIndex(self.currentIndex())

    def which_clicked(self):
        self.active_item = self.itemFromIndex(self.currentIndex())


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
