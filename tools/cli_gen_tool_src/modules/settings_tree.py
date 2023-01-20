##
# @file settings_tree.py
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

# imports
import copy
import json

# pyside imports
from PySide6.QtCore import Qt, QByteArray
from PySide6.QtWidgets import (
    QComboBox,
    QHeaderView,
    QAbstractItemView,
    QSizePolicy,
    QTreeWidget,
    QTreeWidgetItem,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
)
from PySide6.QtGui import QCursor

# external data models
from modules.data_models import dataModels
from modules.display_models import displayModels
from modules.mainwindow_methods import TableButtonBox

# TODO update underlying data
class DelimiterTableWidget(QTableWidget):
    def __init_subclass__(cls) -> None:
        return super(DelimiterTableWidget, cls).__init_subclass__()

    def build_table(cls, container, cliopt):
        cls.ddtt = displayModels._settings_tree_display["process parameters"][
            "data delimiter sequences"
        ]["tooltip"]
        cls.sstt = displayModels._settings_tree_display["process parameters"][
            "start stop data delimiter sequences"
        ]["tooltip"]
        cls._cursor = QCursor()
        cls.dict_pos = container.data(4, 0).split(",")
        cls.setObjectName(str(container.data(4, 0)))
        cls.cliopt = cliopt
        cls.delimiters = cls.cliopt[cls.dict_pos[0]]["var"][cls.dict_pos[2]]
        cls.tt = True
        if cls.dict_pos[2] == "start stop data delimiter sequences":
            cls.tt = False
        cls.setColumnCount(2)
        cls.setRowCount(len(cls.delimiters))
        cls.setMaximumWidth(300)
        cls.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        cls.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        cls.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        cls.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        r = 0
        for key in cls.delimiters:
            delimiter_item = QTableWidgetItem()
            delimiter_item.setData(0, cls.delimiters[key])
            if cls.tt:
                delimiter_item.setToolTip(cls.ddtt)
            else:
                delimiter_item.setToolTip(cls.sstt)
            cls.setItem(r, 0, delimiter_item)
            control_item = QTableWidgetItem()
            cls.setItem(r, 1, control_item)
            cls.setCellWidget(r, 1, TableButtonBox(cls))
            r += 1


class SettingsTreeWidget(QTreeWidget):
    def __init__(self, parent, cliopt, session, logger) -> None:
        super(SettingsTreeWidget, self).__init__()
        self.command_tree = parent.command_tree
        self.update_code = parent.update_code
        self.loading = parent.loading
        self.setParent(parent.ui.settings_tree_container)
        self.items = []
        self.tables = []
        self.default_settings_tree_values = parent.default_settings_tree_values
        self._parent = parent
        self.cliopt = cliopt
        self.session = session
        self.item_clicked = None
        self._cursor = parent.qcursor
        self.logger = logger

        self.setHeaderLabel("Settings Tree")
        self.setColumnCount(5)
        self.setColumnHidden(4, True)
        self.setHeaderLabels(("Section", "Macro Name", "Type", "Value"))
        self.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        for i in range(self.columnCount() - 1):
            self.header().setSectionResizeMode(i, QHeaderView.ResizeToContents)
            self.header().setSectionResizeMode(i, QHeaderView.Stretch)
        self.setMinimumWidth(400)
        # self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setSelectionMode(QAbstractItemView.NoSelection)
        self.setFocusPolicy(Qt.NoFocus)
        # use the text in _tree for self.ui.settings_tree field labels, build the tree
        for parent in SettingsTreeMethods._tree:
            index_of_child = 0
            dict_key = parent

            is_config = True if dict_key == "config" else False
            # add parents to self.ui.settings_treeS

            if is_config:
                # make these parents children of root using the keys from 'cfg_dict'
                cfg_path = session["opt"]["input_config_file_path"]
                setting_container = QTreeWidgetItem(
                    self.invisibleRootItem(), [str("Input config: " + cfg_path), ""]
                )
                setting_container.setIcon(0, self._parent.ui.fileDialogContentsViewIcon)
                setting_container.setToolTip(0, "Input config: " + cfg_path)
                setting_label.setFlags(setting_label.flags() | Qt.ItemIsSelectable)

                for subsection in SettingsTreeMethods._tree["config"]:
                    # index_of_child = 0
                    setting_label = QTreeWidgetItem(
                        setting_container, [subsection, "", "", ""]
                    )
                    # make the treewidgetitem editable
                    setting_label.setFlags(setting_label.flags() | Qt.ItemIsSelectable)
                    # make the treewidgetitem span columns

                    for item in SettingsTreeMethods._tree["config"][subsection]:
                        # dict_pos = subsection + "," + str(index_of_child) + "," + item
                        var_initial_val = self.cliopt["config"]["var"][subsection][
                            item
                        ]["value"]
                        has_combobox = False
                        tooltip = SettingsTreeMethods._tree[dict_key][subsection][item][
                            "tooltip"
                        ]
                        combobox_tooltip = SettingsTreeMethods._tree[dict_key][
                            subsection
                        ][item]["tooltip"]
                        if (
                            SettingsTreeMethods._tree[dict_key][subsection][item][
                                "type"
                            ]
                            == "Enable/Disable"
                        ):
                            has_combobox = True
                            tooltip = ""
                        index_of_child = self.set_up_child(
                            subsection,
                            setting_label,
                            index_of_child,
                            item,
                            SettingsTreeMethods._tree[dict_key][subsection][item][
                                "type"
                            ],
                            tooltip,
                            var_initial_val,
                            has_combobox,
                            combobox_tooltip,
                        )
            elif not is_config:
                setting_container = QTreeWidgetItem(
                    self.invisibleRootItem(), [dict_key, ""]
                )
                setting_container.setIcon(0, self._parent.ui.commandLinkIcon)

                for child in SettingsTreeMethods._tree[parent]:

                    dict_pos = dict_key + "," + str(index_of_child) + "," + child

                    var_initial_val = self.cliopt[dict_key]["var"][child]
                    if (
                        child == "data delimiter sequences"
                        or child == "start stop data delimiter sequences"
                    ):
                        setting_label = QTreeWidgetItem(
                            setting_container, [child, "", "", ""]
                        )
                        setting_label.setData(4, 0, dict_pos)
                        setting_label.setFlags(
                            setting_label.flags() | Qt.ItemIsSelectable
                        )
                        index_of_child = self.build_tree_table_widget(
                            setting_label, index_of_child, dict_pos
                        )
                    else:
                        has_combobox = False
                        tooltip = SettingsTreeMethods._tree[dict_key][child]["tooltip"]
                        combobox_tooltip = SettingsTreeMethods._tree[dict_key][child][
                            "tooltip"
                        ]
                        if (
                            SettingsTreeMethods._tree[dict_key][child]["type"]
                            == "Enable/Disable"
                        ):
                            has_combobox = True
                            tooltip = ""
                        index_of_child = self.set_up_child(
                            dict_key,
                            setting_container,
                            index_of_child,
                            child,
                            SettingsTreeMethods._tree[dict_key][child]["type"],
                            tooltip,
                            var_initial_val,
                            has_combobox,
                            combobox_tooltip,
                        )

                    self.default_settings_tree_values.update(
                        {str(child).strip(): var_initial_val}
                    )

        self.setEditTriggers(self.NoEditTriggers)
        # update cliopt with new value when editing is complete
        self.itemChanged.connect(self.settings_tree_edit_complete)
        # check if user clicked on the column we want them to edit
        self.itemDoubleClicked.connect(self.check_if_settings_tree_col_editable)
        # check if user hit enter on an item
        self.itemActivated.connect(self.settings_tree_item_activated)
        # self._parent.settings_tree_button_toggles()
        # self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.itemSelectionChanged.connect(self._parent.settings_tree_button_toggles)
        self.itemClicked.connect(self._parent.settings_tree_button_toggles)
        self.itemCollapsed.connect(self._parent.settings_tree_button_toggles)
        self.itemExpanded.connect(self._parent.settings_tree_button_toggles)
        self.itemExpanded.connect(self.item_expanded)

    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key_Escape:
            self.selectionModel().clearSelection()
        return super().keyPressEvent(event)

    def item_expanded(self, item: QTreeWidgetItem):
        self.active_item = item

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

            if state["expanded"][state_index] == True:
                item.setExpanded(True)
            else:
                item.setExpanded(False)
            state_index += 1

    ## builds a table onto a tree widget item
    def build_tree_table_widget(self, label: QTreeWidgetItem, index_of_child, dict_pos):
        container = QTreeWidgetItem(label)
        container.setFirstColumnSpanned(True)
        container.setData(4, 0, dict_pos)
        # add parent tree item to root
        cursor = self._cursor
        logger = self.logger
        # table = DelimitersTableView(self, logger, cursor, container, self.cliopt)
        table = DelimiterTableWidget(self)
        table.build_table(container, self.cliopt)
        self.setItemWidget(container, 0, table)
        self.tables.append(table)
        index_of_child += 1
        return index_of_child

    ## helper method to add children to container items
    def set_up_child(
        self,
        dict_key,
        parent,
        index_of_child,
        var_name,
        var_type,
        var_tooltip,
        var_initial_val,
        combobox=False,
        combobox_item_tooltips=[],
    ):
        column_label_list = ["", var_name, var_type, str(repr(var_initial_val))]
        child_container = QTreeWidgetItem(parent, column_label_list)
        _twi = child_container
        dict_pos = dict_key + "," + str(index_of_child) + "," + var_name
        _twi.setData(4, 0, dict_pos)
        _twi.setFlags(_twi.flags() | Qt.ItemIsEditable)
        if var_tooltip != "" and var_tooltip != None:
            for col in range(self.columnCount()):
                _twi.setToolTip(col, var_tooltip)
        if combobox == True:
            for col in range(self.columnCount()):
                _twi.setToolTip(col, combobox_item_tooltips[0])
            _cmb = QComboBox()
            _cmb.addItem("Disabled", False)
            _cmb.addItem("Enabled", True)

            if (
                combobox_item_tooltips
                and combobox_item_tooltips[0] != None
                and combobox_item_tooltips[0] != ""
            ):
                _cmb.setItemData(0, combobox_item_tooltips[0], Qt.ToolTipRole)
            if (
                combobox_item_tooltips
                and combobox_item_tooltips[1] != None
                and combobox_item_tooltips[1] != ""
            ):
                _cmb.setItemData(1, combobox_item_tooltips[1], Qt.ToolTipRole)
            _cmb.setObjectName(dict_pos)
            if var_initial_val == False:
                _cmb.setCurrentIndex(_cmb.findText("Disabled"))
            elif var_initial_val == True:
                _cmb.setCurrentIndex(_cmb.findText("Enabled"))
            _cmb.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLengthWithIcon)
            # either or, dont trigger twice
            # _cmb.currentIndexChanged.connect(self.settings_tree_combo_box_index_changed)
            _cmb.currentTextChanged.connect(
                lambda text, combobox=_cmb, item=_twi: self.settings_tree_combo_box_index_changed(
                    text, combobox, item
                )
            )
            self.setItemWidget(
                _twi,
                3,
                _cmb,
            )
        index_of_child += 1
        return index_of_child

    ## updates the type field to reflect the value
    def update_settings_tree_type_field_text(self, item):
        object_string = str(item.data(4, 0))
        object_list = object_string.strip("\n").split(",")
        sub_dict = self.cliopt["config"]["tree"]["items"][object_list[0]][
            int(object_list[1])
        ]["fields"]
        number_field = int(sub_dict["3"])
        if number_field <= 255:
            type_field = "uint8_t"
            item.setToolTip(2, "")
        elif number_field > 255 and number_field <= 65535:
            type_field = "uint16_t*"
            item.setToolTip(2, "The compiler will warn you about this type change")
        elif number_field > 65535:
            type_field = "uint32_t*"
            item.setToolTip(2, "The compiler will warn you about this type change")
        item.setText(2, type_field)

    ## called on combobox change
    def settings_tree_combo_box_index_changed(self, text, combobox, item):
        self.prompt_to_save = True
        self.windowtitle_set = False
        _twi = item
        self.setCurrentItem(_twi)
        object_string = str(_twi.data(4, 0))
        object_list = object_string.strip("\n").split(",")
        object_list[1] = int(object_list[1])

        if object_list[0] in displayModels._settings_tree_display["config"]:
            _tt = displayModels._settings_tree_display["config"][object_list[0]][
                object_list[2]
            ]["tooltip"]
        else:
            _tt = displayModels._settings_tree_display[object_list[0]][object_list[2]][
                "tooltip"
            ]
        if object_list[0] == "builtin methods":

            if combobox.currentText() == "Enabled":
                self.cliopt[object_list[0]]["var"][object_list[2]] = True
                SettingsTreeMethods.logger.info(
                    object_list[0] + " " + object_list[2] + " enabled"
                )
                for col in range(self.columnCount()):
                    _twi.setToolTip(col, _tt[1])
            else:
                self.cliopt[object_list[0]]["var"][object_list[2]] = False
                SettingsTreeMethods.logger.info(
                    object_list[0] + " " + object_list[2] + " disabled"
                )
                for col in range(self.columnCount()):
                    _twi.setToolTip(col, _tt[0])

            self.update_code("CLI.h", object_list[2], True)

            if object_list[2] == "outputToStream":
                self.update_code("CLI.h", object_list[2], True)

            elif object_list[2] == "defaultFunction":
                if combobox.currentText() == "Enabled":
                    self.cliopt["builtin methods"]["var"]["defaultFunction"] = True
                else:
                    self.cliopt["builtin methods"]["var"]["defaultFunction"] = False

            elif object_list[2] == "listCommands":
                if combobox.currentText() == "Enabled":
                    self.command_tree.add_command_to_tree(
                        self.command_tree.invisibleRootItem(), "listCommands"
                    )
                else:
                    if self.cliopt["builtin methods"]["var"]["listCommands"] == True:
                        self.command_tree.remove_command_from_tree("listCommands")

            elif object_list[2] == "listSettings":
                if combobox.currentText() == "Enabled":
                    self.command_tree.add_command_to_tree(
                        self.command_tree.invisibleRootItem(), "listSettings"
                    )
                else:
                    if self.cliopt["builtin methods"]["var"]["listSettings"] == True:
                        self.command_tree.remove_command_from_tree("listSettings")

            self.update_code("functions.h", object_list[2], True)
            self.update_code("parameters.h", object_list[2], True)
            self.update_code("CLI.h", object_list[2], True)

        if object_list[0] != "builtin methods":
            # _twi = self.currentItem()

            object_data = self.get_object_data(_twi)
            info = self.cliopt["config"]["var"][object_data["pos"][2]]

            if combobox.currentText() == "Enabled":
                info["value"] = True
                self.log_settings_tree_edit(_twi)
                for col in range(self.columnCount()):
                    _twi.setToolTip(col, _tt[1])
            elif combobox.currentText() == "Disabled":
                info["value"] = False
                self.log_settings_tree_edit(_twi)
                for col in range(self.columnCount()):
                    _twi.setToolTip(col, _tt[0])
            self.update_code("config.h", object_data["pos"]["2"], True)

    ## this is called after determining if an item is editable
    def edit_settings_tree_item(self, item):
        widget_present = self.itemWidget(item, 0)
        if widget_present != None:
            # self.edit_table_widget_item(widget_present)
            widget_present.edit(widget_present.currentIndex())
            return
        self.log_settings_tree_edit(item)
        self.editItem(item, 3)

    ## called when a user "activates" a tree item (by pressing enter)
    def settings_tree_item_activated(self, item):
        # expand/collapse QTreeWidgetItem that has children, if it has them
        if item.childCount() > 0:
            if item.isExpanded():
                item.setExpanded(False)
            else:
                item.setExpanded(True)
            return
        object_list = str(item.data(4, 0)).split(",")
        SettingsTreeMethods.logger.info(object_list[2] + " selected")
        self.edit_settings_tree_item(item)

    ## if the user double clicks on something, see if it is editable
    def check_if_settings_tree_col_editable(self, item, column):
        # allow the third column to be editable with mouse clicks
        if column == 3:
            self.edit_settings_tree_item(item)

    def log_settings_tree_edit(self, item, object_data=None):
        if object_data == None:
            object_data = self.get_object_data(item)
        info = self.cliopt[object_data["pos"][0]]["var"][object_data["pos"][2]]
        val_type = object_data["type"]
        val = object_data["value"]
        if self.loading:
            SettingsTreeMethods.logger.info(
                "set "
                + object_data["pos"][2]
                + " to "
                + "'"
                + str(val)
                + "' "
                + str(val_type)
            )
        else:
            SettingsTreeMethods.logger.info(
                "User set "
                + object_data["pos"][2]
                + " to "
                + "'"
                + str(val)
                + "' "
                + str(val_type)
            )
        SettingsTreeMethods.logger.debug(
            str("self.cliOpt['config']['var']['{}']:".format(object_data["pos"][2]))
            + "\n"
            + str(
                json.dumps(info, indent=2, sort_keys=False, default=lambda o: "object")
            )
        )

    def get_object_data(self, item):
        retval = {"type": "", "value": "", "pos": []}
        object_data_pos_string = str(item.data(4, 0))
        object_data_pos_list = object_data_pos_string.strip("\n").split(",")
        if len(object_data_pos_list) < 2:
            return -1
        else:
            retval["type"] = str(item.data(2, 0))
            retval["value"] = str(item.data(3, 0))
            retval["pos"] = object_data_pos_list
            return retval

    ## this is called any time an item changes; any time any column edits take place on settings tree, user or otherwise
    def settings_tree_edit_complete(self, item, col):
        self.prompt_to_save = True
        self.windowtitle_set = False
        if col != 3:
            return
        object_data = self.get_object_data(item)

        val = object_data["value"]
        if "'" in val:
            return  # already repr

        if object_data["pos"][0] == "builtin methods":
            return
        object_data["pos"][1] = int(str(object_data["pos"][1]))

        # process output
        if object_data["pos"][0] == "process output":
            item.setText(3, str(repr(val)))
            self.cliopt["process output"]["var"][object_data["pos"][2]] = val
            self.log_settings_tree_edit(item, object_data)
            self.update_code("CLI.h", object_data["pos"][2], True)
            if object_data["pos"][2] == "defaultFunction":
                self.update_code("functions.h", object_data["pos"][2], True)
            return

        # process parameters (CLI.h)
        if object_data["pos"][0] == "process parameters":
            item.setText(3, "'" + str(val) + "'")
            self.log_settings_tree_edit(item, object_data)
            self.cliopt["process parameters"]["var"][item.text(1)] = val
            self.update_code("CLI.h", val, True)
            return

        # config.h
        info = self.cliopt["config"]["var"][object_data["pos"][2]]
        tmp = ""
        if val == "enabled":
            tmp = True
        elif val == "disabled":
            tmp = False
        else:
            if val == "":
                tmp = 0
                item.setText(3, "'" + str(repr(tmp)) + "'")
            else:
                tmp = int(val)
                item.setText(3, "'" + str(repr(tmp)) + "'")
        if tmp == info["value"]:
            return
        # update the config dict
        info["value"] = tmp
        self.update_settings_tree_type_field_text(item)
        self.update_code("config.h", object_data["pos"][2], True)
        self.log_settings_tree_edit(item, object_data)

    ## this is called after determining if an item is editable
    def edit_item(self, item):
        widget_present = self.itemWidget(item, 0)
        if widget_present != None:
            # self.edit_table_widget_item(widget_present)
            widget_present.edit(widget_present.currentIndex())
            return
        self.log_settings_tree_edit(item)
        self.editItem(item, 3)


# settings_tree methods
class SettingsTreeMethods(object):
    ## the constructor
    def __init__(self):
        super(SettingsTreeMethods, self).__init__()
        SettingsTreeMethods.logger = self.get_child_logger(__name__)
        SettingsTreeMethods._tree = displayModels._settings_tree_display
        self.settings_tree_buttons = copy.deepcopy(dataModels.button_dict)
        self.settings_tree_buttons["buttons"].update(
            {
                "edit": copy.deepcopy(dataModels.button_sub_dict),
                "clear": copy.deepcopy(dataModels.button_sub_dict),
                "default": copy.deepcopy(dataModels.button_sub_dict),
                "collapse": copy.deepcopy(dataModels.button_sub_dict),
            }
        )
        self.settings_tree_buttons["buttons"]["edit"][
            "QPushButton"
        ] = self.ui.edit_setting_button
        self.settings_tree_buttons["buttons"]["clear"][
            "QPushButton"
        ] = self.ui.clear_setting_button
        self.settings_tree_buttons["buttons"]["default"][
            "QPushButton"
        ] = self.ui.default_setting_button
        self.settings_tree_buttons["buttons"]["collapse"][
            "QPushButton"
        ] = self.ui.settings_tree_collapse_button
        self.settings_tree_buttons["buttons"]["collapse"]["enabled"] = True

    def build_settings_tree(self):
        container = self.ui.settings_tree_container
        container.layout = QHBoxLayout(container)
        self.settings_tree = SettingsTreeWidget(
            self, self.cliOpt, self.session, SettingsTreeMethods.logger
        )
        container.layout.addWidget(self.settings_tree)
        container.setLayout(container.layout)
        return self.settings_tree


# end of file
