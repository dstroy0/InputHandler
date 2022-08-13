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

import json

from PySide6.QtCore import QRegularExpression, Qt
from PySide6.QtWidgets import QComboBox, QHeaderView, QTreeWidgetItem
from res.modules.data_models import dataModels

from res.modules.logging_setup import Logger


# settings_tree methods
class SettingsTreeMethods(object):
    def __init__(self):
        super(SettingsTreeMethods, self).__init__()
        SettingsTreeMethods.logger = Logger.get_child_logger(self.logger, __name__)

    def update_settings_tree_type_field_text(self, item):
        object_string = str(item.data(4, 0))
        object_list = object_string.strip("\n").split(",")
        sub_dict = self.cliOpt["config"]["tree"]["items"][object_list[0]][
            int(object_list[1])
        ]["fields"]
        number_field = int(sub_dict[3])
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

    def settings_tree_combo_box_index_changed(self, index):
        self.prompt_to_save = True
        object_string = self.sender().objectName()
        object_list = object_string.strip("\n").split(",")
        object_list[1] = int(object_list[1])
        if object_list[0] == "builtin methods":
            if index == 1:
                self.cliOpt[object_list[0]]["var"][object_list[2]] = True
                SettingsTreeMethods.logger.info(
                    object_list[0] + " " + object_list[2] + " enabled"
                )
            else:
                self.cliOpt[object_list[0]]["var"][object_list[2]] = False
                SettingsTreeMethods.logger.info(
                    object_list[0] + " " + object_list[2] + " disabled"
                )

            self.update_code("setup.h", object_list[2], True)
            if object_list[2] == "outputToStream":
                self.update_code("setup.cpp", object_list[2], True)

            if (
                object_list[2] == "defaultFunction"
                or object_list[2] == "listCommands"
                or object_list[2] == "listSettings"
            ):
                self.update_code("functions.h", object_list[2], True)
                self.update_code("functions.cpp", object_list[2], True)
                self.update_code("parameters.h", object_list[2], True)
                if object_list[2] == "listCommands" or object_list[2] == "listSettings":
                    combobox = self.cliOpt["builtin methods"]["tree"]["items"][
                        object_list[2]
                    ]["QComboBox"][object_list[1]]
                    if (
                        combobox.currentText() == "Enabled"
                        and object_list[2] == "listCommands"
                    ):
                        self.cliOpt["commands"]["parameters"].update(
                            dataModels.listCommands
                        )
                        self.add_qtreewidgetitem(self.ui.command_tree, "listCommands")
                    elif (
                        combobox.currentText() == "Disabled"
                        and object_list[2] == "listCommands"
                    ):
                        if "listCommands" in self.cliOpt["commands"]["parameters"]:
                            del self.cliOpt["commands"]["parameters"]["listCommands"]
                        self.rem_qtreewidgetitem(object_list)

                    if (
                        combobox.currentText() == "Enabled"
                        and object_list[2] == "listSettings"
                    ):
                        self.cliOpt["commands"]["parameters"].update(
                            dataModels.listSettings
                        )
                        self.add_qtreewidgetitem(self.ui.command_tree, "listSettings")
                    elif (
                        combobox.currentText() == "Disabled"
                        and object_list[2] == "listSettings"
                    ):
                        if "listSettings" in self.cliOpt["commands"]["parameters"]:
                            del self.cliOpt["commands"]["parameters"]["listSettings"]
                        self.rem_qtreewidgetitem(object_list)

        if object_list[0] != "builtin methods":
            combobox = self.cliOpt["config"]["tree"]["items"][object_list[0]][
                "QComboBox"
            ][object_list[1]]
            sub_dict = self.cliOpt["config"]["tree"]["items"][object_list[0]][
                object_list[1]
            ]["fields"]
            if combobox.currentText() == "Enabled":
                sub_dict[1] = "       "
                sub_dict[3] = True
                SettingsTreeMethods.logger.info(
                    str(sub_dict[2].strip("\n")) + " enabled"
                )
            elif (
                self.cliOpt["config"]["tree"]["items"][object_list[0]]["QComboBox"][
                    object_list[1]
                ].currentText()
                == "Disabled"
            ):
                sub_dict[1] = "    // "
                sub_dict[3] = False
                SettingsTreeMethods.logger.info(
                    str(sub_dict[2].strip("\n")) + " disabled"
                )
            SettingsTreeMethods.logger.debug(
                "self.cliOpt['config']['tree']['items']['{}'][{}]['fields']:".format(
                    object_list[0], object_list[1]
                ),
                json.dumps(
                    sub_dict, indent=2, sort_keys=False, default=lambda o: "object"
                ),
            )
            self.update_code("config.h", sub_dict[2], True)

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

    def check_if_settings_tree_col_editable(self, item, column):
        # allow the third column to be editable with mouse clicks
        if column == 3:
            self.edit_settings_tree_item(item)

    # this is called any time an item changes; any time any column edits take place on settings tree, user or otherwise
    def settings_tree_edit_complete(self, item, col):
        self.prompt_to_save = True
        if col != 3:
            return
        val = str(item.data(3, 0))
        if "'" in val:
            return  # already repr
        object_string = str(item.data(4, 0))
        object_list = object_string.strip("\n").split(",")

        # dict position is 3 items
        if len(object_list) < 2:
            return

        object_list[1] = int(str(object_list[1]))

        # process output
        if object_list[0] == "process output":
            item.setText(3, str(repr(val)))
            self.cliOpt["process output"]["var"][object_list[2]] = val
            SettingsTreeMethods.logger.info(object_list[2] + " " + str(val))
            self.update_code("setup.h", object_list[2], True)
            if object_list[2] == "outputToStream":
                self.update_code("setup.cpp", object_list[2], True)
            if object_list[2] == "defaultFunction":
                self.update_code("functions.h", object_list[2], True)
                self.update_code("functions.cpp", object_list[2], True)
            return

        # process parameters (setup.h)
        if object_list[0] == "process parameters":
            item.setText(3, "'" + str(val) + "'")
            SettingsTreeMethods.logger.info(
                "edited " + object_list[2] + ", new value " + "'" + str(val) + "'"
            )
            self.cliOpt["process parameters"]["var"][item.text(1)] = val
            self.update_code("setup.h", item.text(1), True)
            return

        # config.h
        sub_dict = self.cliOpt["config"]["tree"]["items"][object_list[0]][
            object_list[1]
        ]["fields"]
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
        if tmp == sub_dict[3]:
            return
        # update the config dict
        sub_dict[3] = tmp
        self.update_settings_tree_type_field_text(item)
        self.update_code("config.h", sub_dict[2], True)
        SettingsTreeMethods.logger.info(
            str(
                "self.cliOpt['config']['tree']['items']['{}'][{}]['fields']:".format(
                    object_list[0], object_list[1]
                )
            )
            + "\n"
            + str(
                json.dumps(
                    sub_dict, indent=2, sort_keys=False, default=lambda o: "object"
                )
            )
        )

    def edit_settings_tree_item(self, item):
        widget_present = self.ui.settings_tree.itemWidget(item, 0)
        if widget_present != None:
            self.edit_table_widget_item(widget_present)
            return
        object_string = str(item.data(4, 0))
        object_string = object_string.strip()
        object_list = object_string.split(",")
        SettingsTreeMethods.logger.info(
            "editing "
            + str(object_list[2])
            + " in "
            + str(object_list[0])
            + ", current value "
            + str(item.data(3, 0))
        )
        self.ui.settings_tree.editItem(item, 3)

    def build_lib_settings_tree(self):
        settings_tree = self.ui.settings_tree
        ## helper method to add children to container items
        def set_up_child(
            dict_key,
            tree,
            parent,
            index_of_child,
            var_name,
            var_type,
            var_tooltip,
            var_initial_val,
            combobox=False,
            combobox_item_tooltips=[],
        ):
            if tree["root"] == self.cliOpt["config"]["tree"]["root"]:
                access = dict_key
            else:
                access = var_name
            column_label_list = ["", var_name, var_type, str(repr(var_initial_val))]
            tree["items"][access]["QTreeWidgetItem"].update(
                {index_of_child: QTreeWidgetItem(parent, column_label_list)}
            )
            _twi = tree["items"][access]["QTreeWidgetItem"][index_of_child]
            dict_pos = dict_key + "," + str(index_of_child) + "," + var_name
            _twi.setData(4, 0, dict_pos)
            _twi.setFlags(_twi.flags() | Qt.ItemIsEditable)
            if var_tooltip != "" and var_tooltip != None:
                _twi.setToolTip(3, var_tooltip)
            if combobox == True:
                tree["items"][access]["QComboBox"].update({index_of_child: QComboBox()})
                _cmb = tree["items"][access]["QComboBox"][index_of_child]
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
                _cmb.setSizeAdjustPolicy(
                    QComboBox.AdjustToMinimumContentsLengthWithIcon
                )
                _cmb.currentIndexChanged.connect(
                    self.settings_tree_combo_box_index_changed
                )
                settings_tree.setItemWidget(
                    _twi,
                    3,
                    _cmb,
                )
            index_of_child += 1
            return index_of_child

        settings_tree = self.ui.settings_tree
        settings_tree.setHeaderLabels(("Section", "Macro Name", "Type", "Value"))
        settings_tree.header().setSectionResizeMode(0, QHeaderView.Interactive)
        settings_tree.header().setMinimumSectionSize(150)
        settings_tree.header().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        settings_tree.header().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        settings_tree.header().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        settings_tree.setColumnCount(5)
        # 5th column holds object location in cliOpt
        settings_tree.setColumnHidden(4, 1)

        # process output
        index_of_child = 0
        dict_key = "process output"
        tree = self.cliOpt[dict_key]["tree"]
        tree["root"] = QTreeWidgetItem(settings_tree, [dict_key, ""])
        tree["root"].setIcon(0, self.ui.commandLinkIcon)
        # process output buffer size option
        var_name = "buffer size"
        var_type = "bytes"
        var_initial_val = self.cliOpt[dict_key]["var"][var_name]
        index_of_child = set_up_child(
            dict_key,
            tree,
            tree["root"],
            index_of_child,
            "buffer size",
            "bytes",
            "Must be greater than zero for class output.",
            var_initial_val,
            False,
        )
        self.default_settings_tree_values.update({var_name: var_initial_val})

        # process output stream
        var_initial_val = self.cliOpt["process output"]["var"]["output stream"]
        index_of_child = set_up_child(
            dict_key,
            tree,
            tree["root"],
            index_of_child,
            "output stream",
            "Stream",
            "Set an output Stream that is legal for your platform.",
            var_initial_val,
            False,
        )
        self.default_settings_tree_values.update({var_name: var_initial_val})

        # process parameters
        index_of_child = 0
        dict_key = "process parameters"
        tree = self.cliOpt[dict_key]["tree"]
        tree["root"] = QTreeWidgetItem(self.ui.settings_tree, [dict_key, ""])
        tree["root"].setIcon(0, self.ui.commandLinkIcon)

        # process parameters process name option
        var_name = "process name"
        var_type = "plain text"
        var_initial_val = self.cliOpt[dict_key]["var"][var_name]
        index_of_child = set_up_child(
            dict_key,
            tree,
            tree["root"],
            index_of_child,
            var_name,
            var_type,
            "The process name prepends all terminal output.",
            var_initial_val,
            False,
        )
        self.default_settings_tree_values.update({var_name: var_initial_val})

        # process parameters end of line characters option
        var_name = "end of line characters"
        var_type = "plain text; control char"
        var_initial_val = self.cliOpt[dict_key]["var"][var_name]
        index_of_child = set_up_child(
            dict_key,
            tree,
            tree["root"],
            index_of_child,
            var_name,
            var_type,
            "Set to the eol char of your data.",
            var_initial_val,
            False,
        )
        self.default_settings_tree_values.update({var_name: var_initial_val})

        # process parameters input control char sequence option
        var_name = "input control char sequence"
        var_type = "plain text; control char"
        var_initial_val = self.cliOpt[dict_key]["var"][var_name]
        index_of_child = set_up_child(
            dict_key,
            tree,
            tree["root"],
            index_of_child,
            var_name,
            var_type,
            "Enter this sequence before an unescaped control char (r,n,e,t,b,etc.)",
            var_initial_val,
            False,
        )
        self.default_settings_tree_values.update({var_name: var_initial_val})

        # process parameters wildcard char option
        var_name = "wildcard char"
        var_type = "plain text; control char"
        var_initial_val = self.cliOpt[dict_key]["var"][var_name]
        index_of_child = set_up_child(
            dict_key,
            tree,
            tree["root"],
            index_of_child,
            var_name,
            var_type,
            "Any single char; * by default.",
            var_initial_val,
            False,
        )
        self.default_settings_tree_values.update({var_name: var_initial_val})

        # process parameters data delimiter sequences option
        columns = 1
        remove_row_button = True
        dict_key2 = "data delimiter sequences"
        add_row_function = self.add_data_delimiter_row
        self.build_tree_table_widget(
            index_of_child,
            tree,
            dict_key,
            dict_key2,
            columns,
            add_row_function,
            remove_row_button,
        )
        index_of_child += 1
        # process parameters start stop delimiter sequences option
        dict_key2 = "start stop data delimiter sequences"
        add_row_function = self.add_start_stop_data_delimiter_row
        self.build_tree_table_widget(
            index_of_child,
            tree,
            dict_key,
            dict_key2,
            columns,
            add_row_function,
            remove_row_button,
        )

        # builtin methods
        index_of_child = 0
        dict_key = "builtin methods"
        tree = self.cliOpt[dict_key]["tree"]
        tree["root"] = QTreeWidgetItem(self.ui.settings_tree, [dict_key, ""])
        tree["root"].setIcon(0, self.ui.commandLinkIcon)

        # outputToStream
        var_name = "outputToStream"
        var_type = "enable/disable"
        var_initial_val = self.cliOpt[dict_key]["var"][var_name]
        index_of_child = set_up_child(
            dict_key,
            tree,
            tree["root"],
            index_of_child,
            var_name,
            var_type,
            "",
            var_initial_val,
            True,
            [
                "",
                "This will have no effect if you have not designated an output Stream and set a buffer size in 'process output'.",
            ],
        )

        # defaultFunction
        var_name = "defaultFunction"
        var_type = "enable/disable"
        var_initial_val = self.cliOpt[dict_key]["var"][var_name]
        index_of_child = set_up_child(
            dict_key,
            tree,
            tree["root"],
            index_of_child,
            var_name,
            var_type,
            "",
            var_initial_val,
            True,
            ["No default function.", "Default function enabled."],
        )
        self.default_settings_tree_values.update({var_name: var_initial_val})

        # listCommands
        var_name = "listCommands"
        var_type = "enable/disable"
        var_initial_val = self.cliOpt[dict_key]["var"][var_name]
        index_of_child = set_up_child(
            dict_key,
            tree,
            tree["root"],
            index_of_child,
            var_name,
            var_type,
            "",
            var_initial_val,
            True,
            ["No listCommands command", "listCommands available to user."],
        )
        self.default_settings_tree_values.update({var_name: var_initial_val})

        # listSettings
        var_name = "listSettings"
        var_type = "enable/disable"
        var_initial_val = self.cliOpt[dict_key]["var"][var_name]
        index_of_child = set_up_child(
            dict_key,
            tree,
            tree["root"],
            index_of_child,
            var_name,
            var_type,
            "",
            var_initial_val,
            True,
            ["No listSettings command", "listSettings available to user."],
        )
        self.default_settings_tree_values.update({var_name: var_initial_val})

        # config.h
        tree = self.cliOpt["config"]["tree"]
        cfg_dict = self.cliOpt["config"]["tree"]["items"]
        cfg_path = self.session["opt"]["input_config_file_path"]
        tree["root"] = QTreeWidgetItem(settings_tree, ["Input config: " + cfg_path, ""])
        tree["root"].setIcon(0, self.ui.fileDialogContentsViewIcon)
        tree["root"].setToolTip(0, "Input config: " + cfg_path)

        # make these parents children of root using the keys from 'cfg_dict'
        for key in cfg_dict:
            tree["parents"][key]["QTreeWidgetItem"] = QTreeWidgetItem(
                tree["root"], [key, "", "", ""]
            )

        # TODO rework this to use set_up_child to reduce code length
        # populate `settings_tree`
        regexp = QRegularExpression("(\s*[\/][\/]\s*)")
        for key in cfg_dict:
            index_of_child = 0
            parent = tree["parents"][key]["QTreeWidgetItem"]
            for item in cfg_dict[key]:
                if "QComboBox" not in str(item) and "QTreeWidgetItem" not in str(item):
                    sub_dict = cfg_dict[key][item]["fields"]
                    match = regexp.match(sub_dict[1])
                    # sort out boolean fields
                    if match.hasMatch() and (
                        sub_dict[0] >= self.config_file_boolean_define_fields_line_start
                    ):
                        cfg_dict[key]["QComboBox"].update({item: ""})
                        index_of_child = set_up_child(
                            key,
                            tree,
                            parent,
                            index_of_child,
                            sub_dict[2],
                            "Enable/Disable",
                            "",
                            sub_dict[3],
                            True,
                        )
                        self.default_settings_tree_values.update(
                            {sub_dict[2]: sub_dict[3]}
                        )

                    elif not match.hasMatch() and (
                        sub_dict[0] >= self.config_file_boolean_define_fields_line_start
                    ):
                        cfg_dict[key]["QComboBox"].update({item: ""})
                        index_of_child = set_up_child(
                            key,
                            tree,
                            parent,
                            index_of_child,
                            sub_dict[2],
                            "Enable/Disable",
                            "",
                            sub_dict[3],
                            True,
                        )
                        self.default_settings_tree_values.update(
                            {sub_dict[2]: sub_dict[3]}
                        )

                    else:
                        number_field = int(sub_dict[3])
                        if number_field <= 255:
                            type_field = "uint8_t"
                        elif number_field > 255 and number_field <= 65535:
                            type_field = "uint16_t"
                        elif number_field > 65535:
                            type_field = "uint32_t"
                        index_of_child = set_up_child(
                            key,
                            tree,
                            parent,
                            index_of_child,
                            sub_dict[2],
                            type_field,
                            "This field's type is automatically set by the library.",
                            sub_dict[3],
                            False,
                        )
                        self.default_settings_tree_values.update(
                            {sub_dict[2]: sub_dict[3]}
                        )

        settings_tree.setEditTriggers(self.ui.settings_tree.NoEditTriggers)
        # update cliOpt with new value when editing is complete
        settings_tree.itemChanged.connect(self.settings_tree_edit_complete)
        # check if user clicked on the column we want them to edit
        settings_tree.itemDoubleClicked.connect(
            self.check_if_settings_tree_col_editable
        )
        # check if user hit enter on an item
        settings_tree.itemActivated.connect(self.settings_tree_item_activated)

    # end build_lib_settings_tree()


# end of file
