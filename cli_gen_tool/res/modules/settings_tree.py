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
from res.modules.dev_qol_var import config_file_boolean_define_fields_line_start
from res.modules.logging_setup import Logger


# settings_tree methods
class SettingsTreeMethods(object):
    logger = ""

    def __init__(self):
        super().__init__()
        SettingsTreeMethods.logger = Logger.get_child_logger(self.logger, __name__)

    def update_settings_tree_type_field_text(self, item):
        object_string = str(item.data(4, 0))
        object_list = object_string.strip("\n").split(",")
        sub_dict = self.cliOpt["config"]["tree"]["items"][object_list[0]][
            int(object_list[1])
        ]["fields"]
        number_field = int(sub_dict[4])
        if number_field <= 255:
            type_field = "uint8_t"
            sub_dict[5].setToolTip(2, "")
        elif number_field > 255 and number_field <= 65535:
            type_field = "uint16_t*"
            sub_dict[5].setToolTip(
                2, "The compiler will warn you about this type change"
            )
        elif number_field > 65535:
            type_field = "uint32_t*"
            sub_dict[5].setToolTip(
                2, "The compiler will warn you about this type change"
            )
        sub_dict[5].setText(2, type_field)

    def settings_tree_combo_box_index_changed(self, index):
        object_string = self.sender().objectName()
        object_list = object_string.strip("\n").split(",")
        object_list[1] = int(object_list[1])
        sub_dict = self.cliOpt["config"]["tree"]["items"][object_list[0]][
            object_list[1]
        ]["fields"]
        if sub_dict[6].currentText() == "Enable":
            sub_dict[1] = "       "
            sub_dict[4] = True
            SettingsTreeMethods.logger.info(str(sub_dict[3].strip("\n")) + " enabled")
        elif sub_dict[6].currentText() == "Disable":
            sub_dict[1] = "    // "
            sub_dict[4] = False
            SettingsTreeMethods.logger.info(str(sub_dict[3].strip("\n")) + " disabled")
        SettingsTreeMethods.logger.debug(
            "self.cliOpt['config']['tree']['items']['{}'][{}]['fields']:".format(
                object_list[0], object_list[1]
            ),
            json.dumps(sub_dict, indent=2, sort_keys=False, default=lambda o: "object"),
        )
        self.update_code_preview_tree(None)

    def settings_tree_item_activated(self, item):
        SettingsTreeMethods.logger.info(str(item) + " selected")
        self.edit_settings_tree_item(item)

    def check_if_settings_tree_col_editable(self, item, column):
        # allow the third column to be editable
        if column == 3:
            self.edit_settings_tree_item(item)

    # this is called any time an item changes; any time any column edits take place on settings tree, user or otherwise
    def settings_tree_edit_complete(self, item, col):
        if col != 3:
            return
        val = str(item.data(3, 0))
        if "'" in val:
            return  # already repr
        object_string = str(item.data(4, 0))
        object_list = object_string.strip("\n").split(",")
        if len(object_list) < 2:
            return
        object_list[1] = int(str(object_list[1]))
        # process output
        if object_list[0] == "process output":
            item.setText(3, str(repr(val)))
            self.cliOpt["process output"]["var"]["buffer size"] = val
            self.update_code_preview_tree(item)
            SettingsTreeMethods.logger.info("output buffer size " + str(val) + " bytes")
            return
        if object_list[0] == "process parameters":
            SettingsTreeMethods.logger.info("edited a process parameter")
            item.setText(3, str(repr(val)))
            self.update_code_preview_tree(item)
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
                item.setText(3, str(repr(tmp)))
            else:
                tmp = int(val)
                item.setText(3, str(repr(tmp)))
        if tmp == sub_dict[4]:
            return
        # update the config dict
        sub_dict[4] = tmp
        self.update_settings_tree_type_field_text(item)
        self.update_code_preview_tree(item)
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
        def set_up_child(
            dict_key, tree, index_of_child, var_name, var_type, var_initial_val
        ):
            column_label_list = ["", var_name, var_type, str(repr(var_initial_val))]
            tree["items"].update(
                {var_name: QTreeWidgetItem(tree["root"], column_label_list)}
            )
            dict_pos = dict_key + "," + str(index_of_child) + "," + var_name
            tree["items"][var_name].setData(4, 0, dict_pos)
            tree["items"][var_name].setFlags(
                tree["items"][var_name].flags() | Qt.ItemIsEditable
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
            dict_key, tree, index_of_child, var_name, var_type, var_initial_val
        )

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
            dict_key, tree, index_of_child, var_name, var_type, var_initial_val
        )

        # process parameters end of line characters option
        var_name = "end of line characters"
        var_type = "plain text; control char"
        var_initial_val = self.cliOpt[dict_key]["var"][var_name]
        index_of_child = set_up_child(
            dict_key, tree, index_of_child, var_name, var_type, var_initial_val
        )

        # process parameters input control char sequence option
        var_name = "input control char sequence"
        var_type = "plain text; control char"
        var_initial_val = self.cliOpt[dict_key]["var"][var_name]
        index_of_child = set_up_child(
            dict_key, tree, index_of_child, var_name, var_type, var_initial_val
        )

        # process parameters wildcard char option
        var_name = "wildcard char"
        var_type = "plain text; control char"
        var_initial_val = self.cliOpt[dict_key]["var"][var_name]
        index_of_child = set_up_child(
            dict_key, tree, index_of_child, var_name, var_type, var_initial_val
        )

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

        # config.h
        tree = self.cliOpt["config"]["tree"]
        cfg_dict = self.cliOpt["config"]["tree"]["items"]
        cfg_path = self.session["opt"]["input_config_file_path"]
        tree.update(
            {"root": QTreeWidgetItem(settings_tree, ["Input config: " + cfg_path, ""])}
        )
        tree["root"].setIcon(0, self.ui.fileDialogContentsViewIcon)
        tree["root"].setToolTip(0, "Input config: " + cfg_path)

        # make these parents children of root using the keys from 'cfg_dict'
        for key in cfg_dict:
            tree["parents"].update(
                {key: QTreeWidgetItem(tree["root"], [key, "", "", ""])}
            )

        # populate `settings_tree`
        for key in cfg_dict:
            for item in cfg_dict[key]:
                regexp = QRegularExpression("(\s*[\/][\/]\s*)")
                sub_dict = cfg_dict[key][item]["fields"]
                match = regexp.match(sub_dict[1])
                # sort out boolean fields
                if match.hasMatch() and (
                    sub_dict[0] >= config_file_boolean_define_fields_line_start
                ):
                    sub_dict.update({4: False})
                    obj_name = key + "," + str(item) + "," + sub_dict[3]
                    item_list = [
                        "line : " + str(sub_dict[0]),
                        sub_dict[3],
                        "Enable/Disable",
                        "",
                    ]
                    sub_dict.update(
                        {5: QTreeWidgetItem(tree["parents"][key], item_list)}
                    )
                    sub_dict[5].setFlags(sub_dict[5].flags() | Qt.ItemIsEditable)
                    sub_dict[5].setData(4, 0, obj_name)
                    sub_dict[6] = QComboBox()
                    sub_dict[6].addItem("Disable", "False")
                    sub_dict[6].addItem("Enable", "True")
                    sub_dict[6].setObjectName(obj_name)
                    sub_dict[6].setSizeAdjustPolicy(
                        QComboBox.AdjustToMinimumContentsLengthWithIcon
                    )
                    settings_tree.setItemWidget(sub_dict[5], 3, sub_dict[6])
                    sub_dict[6].currentIndexChanged.connect(
                        self.settings_tree_combo_box_index_changed
                    )
                elif not match.hasMatch() and (
                    sub_dict[0] >= config_file_boolean_define_fields_line_start
                ):
                    sub_dict.update({4: True})
                    obj_name = key + "," + str(item) + "," + sub_dict[3]
                    item_list = [
                        "line : " + str(sub_dict[0]),
                        sub_dict[3],
                        "Enable/Disable",
                        str(sub_dict[4]),
                    ]
                    sub_dict.update(
                        {5: QTreeWidgetItem(tree["parents"][key], item_list)}
                    )
                    sub_dict[5].setFlags(sub_dict[5].flags() | Qt.ItemIsEditable)
                    sub_dict[5].setData(4, 0, obj_name)
                    sub_dict[6] = QComboBox()
                    sub_dict[6].addItem("Enable", "True")
                    sub_dict[6].addItem("Disable", "False")
                    sub_dict[6].setObjectName(obj_name)
                    sub_dict[6].setSizeAdjustPolicy(
                        QComboBox.AdjustToMinimumContentsLengthWithIcon
                    )
                    settings_tree.setItemWidget(sub_dict[5], 3, sub_dict[6])
                    sub_dict[6].currentIndexChanged.connect(
                        self.settings_tree_combo_box_index_changed
                    )
                else:
                    number_field = 0
                    if sub_dict[4] == "":
                        number_field = 0
                    else:
                        number_field = int(sub_dict[4])
                    if number_field <= 255:
                        type_field = "uint8_t"
                    elif number_field > 255 and number_field <= 65535:
                        type_field = "uint16_t"
                    elif number_field > 65535:
                        type_field = "uint32_t"
                    obj_name = key + "," + str(item) + "," + sub_dict[3]
                    item_list = [
                        "line : " + str(sub_dict[0]),
                        sub_dict[3],
                        type_field,
                        str(number_field),
                    ]
                    sub_dict.update(
                        {5: QTreeWidgetItem(tree["parents"][key], item_list)}
                    )
                    sub_dict[5].setFlags(sub_dict[5].flags() | Qt.ItemIsEditable)
                    sub_dict[5].setData(4, 0, obj_name)

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
