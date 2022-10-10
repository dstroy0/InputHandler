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
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QComboBox, QHeaderView, QTreeWidgetItem

# external data models
from res.modules.data_models import dataModels
from res.modules.display_models import displayModels

# logging api
from res.modules.logging_setup import Logger


# settings_tree methods
class SettingsTreeMethods(object):
    ## the constructor
    def __init__(self):
        super(SettingsTreeMethods, self).__init__()
        SettingsTreeMethods.logger = Logger.get_child_logger(self.logger, __name__)
        SettingsTreeMethods._tree = displayModels._settings_tree_display

    ## updates the type field to reflect the value
    def update_settings_tree_type_field_text(self, item):
        object_string = str(item.data(4, 0))
        object_list = object_string.strip("\n").split(",")
        sub_dict = self.cliOpt["config"]["tree"]["items"][object_list[0]][
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
    def settings_tree_combo_box_index_changed(self, index):
        self.prompt_to_save = True
        self.windowtitle_set = False
        object_string = self.sender().objectName()
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
            _twi = self.cliOpt["builtin methods"]["tree"]["items"][object_list[2]][
                "QTreeWidgetItem"
            ][object_list[1]]
            if index == 1:
                self.cliOpt[object_list[0]]["var"][object_list[2]] = True
                SettingsTreeMethods.logger.info(
                    object_list[0] + " " + object_list[2] + " enabled"
                )
                for col in range(self.ui.settings_tree.columnCount()):
                    _twi.setToolTip(col, _tt[1])
            else:
                self.cliOpt[object_list[0]]["var"][object_list[2]] = False
                SettingsTreeMethods.logger.info(
                    object_list[0] + " " + object_list[2] + " disabled"
                )
                for col in range(self.ui.settings_tree.columnCount()):
                    _twi.setToolTip(col, _tt[0])

            self.update_code("setup.h", object_list[2], True)
            if object_list[2] == "outputToStream":
                self.update_code("setup.cpp", object_list[2], True)

            if (
                object_list[2] == "defaultFunction"
                or object_list[2] == "listCommands"
                or object_list[2] == "listSettings"
            ):
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
                        self.cliOpt["commands"]["index"].update(
                            {
                                self.cliOpt["var"]["primary id key"]: copy.deepcopy(
                                    dataModels.parameters_index_struct
                                )
                            }
                        )
                        self.cliOpt["commands"]["index"][
                            self.cliOpt["var"]["primary id key"]
                        ]["parameters key"] = object_list[2]
                        self.cliOpt["commands"]["index"][
                            self.cliOpt["var"]["primary id key"]
                        ]["root index key"] = "listCommands"
                        self.add_qtreewidgetitem(
                            self.cliOpt["commands"]["QTreeWidgetItem"]["root"],
                            "listCommands",
                        )
                        self.cliOpt["var"]["primary id key"] = str(
                            int(self.cliOpt["var"]["primary id key"]) + 1
                        )
                        self.cliOpt["var"]["number of commands"] = str(
                            int(self.cliOpt["var"]["number of commands"]) + 1
                        )
                    elif (
                        combobox.currentText() == "Disabled"
                        and object_list[2] == "listCommands"
                    ):
                        self.rem_command(object_list)

                    if (
                        combobox.currentText() == "Enabled"
                        and object_list[2] == "listSettings"
                    ):
                        self.cliOpt["commands"]["parameters"].update(
                            dataModels.listSettings
                        )
                        self.cliOpt["commands"]["index"].update(
                            {
                                self.cliOpt["var"]["primary id key"]: copy.deepcopy(
                                    dataModels.parameters_index_struct
                                )
                            }
                        )

                        self.cliOpt["commands"]["index"][
                            self.cliOpt["var"]["primary id key"]
                        ]["parameters key"] = object_list[2]
                        self.cliOpt["commands"]["index"][
                            self.cliOpt["var"]["primary id key"]
                        ]["root index key"] = "listSettings"
                        self.add_qtreewidgetitem(
                            self.cliOpt["commands"]["QTreeWidgetItem"]["root"],
                            "listSettings",
                        )
                        self.cliOpt["var"]["primary id key"] = str(
                            int(self.cliOpt["var"]["primary id key"]) + 1
                        )
                        self.cliOpt["var"]["number of commands"] = str(
                            int(self.cliOpt["var"]["number of commands"]) + 1
                        )
                    elif (
                        combobox.currentText() == "Disabled"
                        and object_list[2] == "listSettings"
                    ):
                        self.rem_command(object_list)
            self.update_code("functions.h", object_list[2], True)
            self.update_code("functions.cpp", object_list[2], True)
            self.update_code("parameters.h", object_list[2], True)

        if object_list[0] != "builtin methods":
            _twi = self.cliOpt["config"]["tree"]["items"][object_list[0]][
                "QTreeWidgetItem"
            ][object_list[1]]
            combobox = self.cliOpt["config"]["tree"]["items"][object_list[0]][
                "QComboBox"
            ][object_list[1]]
            sub_dict = self.cliOpt["config"]["tree"]["items"][object_list[0]][
                object_list[1]
            ]["fields"]
            if combobox.currentText() == "Enabled":
                sub_dict["1"] = "       "
                sub_dict["3"] = True
                SettingsTreeMethods.logger.info(
                    str(sub_dict["2"].strip("\n")) + " enabled"
                )
                for col in range(self.ui.settings_tree.columnCount()):
                    _twi.setToolTip(col, _tt[1])
            elif (
                self.cliOpt["config"]["tree"]["items"][object_list[0]]["QComboBox"][
                    object_list[1]
                ].currentText()
                == "Disabled"
            ):
                sub_dict["1"] = "    // "
                sub_dict["3"] = False
                SettingsTreeMethods.logger.info(
                    str(sub_dict["2"].strip("\n")) + " disabled"
                )
                for col in range(self.ui.settings_tree.columnCount()):
                    _twi.setToolTip(col, _tt[0])
            SettingsTreeMethods.logger.debug(
                "self.cliOpt['config']['tree']['items']['{}'][{}]['fields']:".format(
                    object_list[0], object_list[1]
                ),
                json.dumps(
                    sub_dict, indent=2, sort_keys=False, default=lambda o: "object"
                ),
            )
            self.update_code("config.h", sub_dict["2"], True)

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

    ## this is called any time an item changes; any time any column edits take place on settings tree, user or otherwise
    def settings_tree_edit_complete(self, item, col):
        self.prompt_to_save = True
        self.windowtitle_set = False
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
        if object_list[0] == "builtin methods":
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
        if tmp == sub_dict["3"]:
            return
        # update the config dict
        sub_dict["3"] = tmp
        self.update_settings_tree_type_field_text(item)
        self.update_code("config.h", sub_dict["2"], True)
        SettingsTreeMethods.logger.debug(
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

    ## this is called after determining if an item is editable
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

    ## helper method to add children to container items
    def set_up_child(
        self,
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
            for col in range(self.ui.settings_tree.columnCount()):
                _twi.setToolTip(col, var_tooltip)
        if combobox == True:
            for col in range(self.ui.settings_tree.columnCount()):
                _twi.setToolTip(col, combobox_item_tooltips[0])
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
            _cmb.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLengthWithIcon)
            _cmb.currentIndexChanged.connect(self.settings_tree_combo_box_index_changed)
            self.ui.settings_tree.setItemWidget(
                _twi,
                3,
                _cmb,
            )
        index_of_child += 1
        return index_of_child

    ## this builds the entire MainWindow.ui.settings_tree
    def build_lib_settings_tree(self):
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

        # use the text in _tree for self.ui.settings_tree field labels, build the tree
        for parent in SettingsTreeMethods._tree:
            index_of_child = 0
            dict_key = parent

            tree = self.cliOpt[dict_key]["tree"]
            is_config = True if dict_key == "config" else False
            # add parents to self.ui.settings_tree
            if not is_config:
                tree["root"] = QTreeWidgetItem(settings_tree, [dict_key, ""])
                tree["root"].setIcon(0, self.ui.commandLinkIcon)
            elif is_config:
                cfg_dict = self.cliOpt["config"]["tree"]["items"]
                cfg_path = self.session["opt"]["input_config_file_path"]
                tree["root"] = QTreeWidgetItem(
                    settings_tree, ["Input config: " + cfg_path, ""]
                )
                tree["root"].setIcon(0, self.ui.fileDialogContentsViewIcon)
                tree["root"].setToolTip(0, "Input config: " + cfg_path)
                # make these parents children of root using the keys from 'cfg_dict'

            if is_config:
                for subsection in SettingsTreeMethods._tree["config"]:
                    index_of_child = 0
                    tree["parents"][subsection]["QTreeWidgetItem"] = QTreeWidgetItem(
                        tree["root"], [subsection, "", "", ""]
                    )
                    for item in SettingsTreeMethods._tree["config"][subsection]:
                        var_initial_val = self.cliOpt["config"]["var"][subsection][item]
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
                            tree,
                            tree["parents"][subsection]["QTreeWidgetItem"],
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
                for child in SettingsTreeMethods._tree[parent]:
                    var_initial_val = self.cliOpt[dict_key]["var"][child]
                    if (
                        child == "data delimiter sequences"
                        or child == "start stop data delimiter sequences"
                    ):
                        columns = 1
                        remove_row_button = True
                        if child == "data delimiter sequences":
                            add_row_function = self.add_data_delimiter_row
                        if child == "start stop data delimiter sequences":
                            add_row_function = self.add_start_stop_data_delimiter_row
                        self.build_tree_table_widget(
                            index_of_child,
                            tree,
                            dict_key,
                            child,
                            columns,
                            add_row_function,
                            remove_row_button,
                        )
                        index_of_child += 1
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
                            tree,
                            tree["root"],
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

        settings_tree.setEditTriggers(self.ui.settings_tree.NoEditTriggers)
        # update cliOpt with new value when editing is complete
        settings_tree.itemChanged.connect(self.settings_tree_edit_complete)
        # check if user clicked on the column we want them to edit
        settings_tree.itemDoubleClicked.connect(
            self.check_if_settings_tree_col_editable
        )
        # check if user hit enter on an item
        settings_tree.itemActivated.connect(self.settings_tree_item_activated)
        self.settings_tree_button_toggles()

    # end build_lib_settings_tree()


# end of file
