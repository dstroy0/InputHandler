
## SettingsTreeMethods
    # ## updates the type field to reflect the value
    # def update_settings_tree_type_field_text(self, item):
    #     object_string = str(item.data(4, 0))
    #     object_list = object_string.strip("\n").split(",")
    #     sub_dict = self.cliOpt["config"]["tree"]["items"][object_list[0]][
    #         int(object_list[1])
    #     ]["fields"]
    #     number_field = int(sub_dict["3"])
    #     if number_field <= 255:
    #         type_field = "uint8_t"
    #         item.setToolTip(2, "")
    #     elif number_field > 255 and number_field <= 65535:
    #         type_field = "uint16_t*"
    #         item.setToolTip(2, "The compiler will warn you about this type change")
    #     elif number_field > 65535:
    #         type_field = "uint32_t*"
    #         item.setToolTip(2, "The compiler will warn you about this type change")
    #     item.setText(2, type_field)

    # ## called on combobox change
    # def settings_tree_combo_box_index_changed(self, index):
    #     self.prompt_to_save = True
    #     self.windowtitle_set = False
    #     object_string = self.sender().objectName()
    #     object_list = object_string.strip("\n").split(",")
    #     object_list[1] = int(object_list[1])

    #     if object_list[0] in displayModels._settings_tree_display["config"]:
    #         _tt = displayModels._settings_tree_display["config"][object_list[0]][
    #             object_list[2]
    #         ]["tooltip"]
    #     else:
    #         _tt = displayModels._settings_tree_display[object_list[0]][object_list[2]][
    #             "tooltip"
    #         ]
    #     if object_list[0] == "builtin methods":
    #         _twi = self.cliOpt["builtin methods"]["tree"]["items"][object_list[2]][
    #             "QTreeWidgetItem"
    #         ][object_list[1]]
    #         if index == 1:
    #             self.cliOpt[object_list[0]]["var"][object_list[2]] = True
    #             SettingsTreeMethods.logger.info(
    #                 object_list[0] + " " + object_list[2] + " enabled"
    #             )
    #             for col in range(self.ui.settings_tree.columnCount()):
    #                 _twi.setToolTip(col, _tt[1])
    #         else:
    #             self.cliOpt[object_list[0]]["var"][object_list[2]] = False
    #             SettingsTreeMethods.logger.info(
    #                 object_list[0] + " " + object_list[2] + " disabled"
    #             )
    #             for col in range(self.ui.settings_tree.columnCount()):
    #                 _twi.setToolTip(col, _tt[0])

    #         self.update_code("setup.h", object_list[2], True)
    #         if object_list[2] == "outputToStream":
    #             self.update_code("setup.cpp", object_list[2], True)

    #         if (
    #             object_list[2] == "defaultFunction"
    #             or object_list[2] == "listCommands"
    #             or object_list[2] == "listSettings"
    #         ):
    #             combobox = self.cliOpt["builtin methods"]["tree"]["items"][
    #                 object_list[2]
    #             ]["QComboBox"][object_list[1]]

    #             if object_list[2] == "defaultFunction":
    #                 if combobox.currentText() == "Enabled":
    #                     self.cliOpt["builtin methods"]["var"]["defaultFunction"] = True
    #                 elif combobox.currentText() == "Disabled":
    #                     self.cliOpt["builtin methods"]["var"]["defaultFunction"] = False

    #             elif (
    #                 object_list[2] == "listCommands" or object_list[2] == "listSettings"
    #             ):
    #                 if (
    #                     combobox.currentText() == "Enabled"
    #                     and object_list[2] == "listCommands"
    #                 ):
    #                     list_commands = OrderedDict()
    #                     list_commands = {
    #                         str(self.cliOpt["var"]["primary id key"]): dict(
    #                             zip(
    #                                 dataModels.command_parameters_dict_keys_list,
    #                                 dataModels.LCcmdParam,
    #                             )
    #                         )
    #                     }
    #                     self.cliOpt["commands"]["parameters"].update(list_commands)
    #                     self.cliOpt["commands"]["index"].update(
    #                         {
    #                             self.cliOpt["var"]["primary id key"]: copy.deepcopy(
    #                                 dataModels.parameters_index_struct
    #                             )
    #                         }
    #                     )
    #                     self.cliOpt["commands"]["index"][
    #                         self.cliOpt["var"]["primary id key"]
    #                     ]["parameters key"] = str(self.cliOpt["var"]["primary id key"])
    #                     self.cliOpt["commands"]["index"][
    #                         self.cliOpt["var"]["primary id key"]
    #                     ]["root index key"] = str(self.cliOpt["var"]["primary id key"])
    #                     self.cliOpt["commands"]["index"][
    #                         self.cliOpt["var"]["primary id key"]
    #                     ]["parent index key"] = str(
    #                         self.cliOpt["var"]["primary id key"]
    #                     )
    #                     self.add_qtreewidgetitem(
    #                         self.cliOpt["commands"]["QTreeWidgetItem"]["root"],
    #                         str(self.cliOpt["var"]["primary id key"]),
    #                     )
    #                     self.cliOpt["var"]["primary id key"] = str(
    #                         int(self.cliOpt["var"]["primary id key"]) + 1
    #                     )
    #                     self.cliOpt["var"]["number of commands"] = str(
    #                         int(self.cliOpt["var"]["number of commands"]) + 1
    #                     )

    #                 if (
    #                     combobox.currentText() == "Enabled"
    #                     and object_list[2] == "listSettings"
    #                 ):
    #                     list_settings = OrderedDict()
    #                     list_settings = {
    #                         str(self.cliOpt["var"]["primary id key"]): dict(
    #                             zip(
    #                                 dataModels.command_parameters_dict_keys_list,
    #                                 dataModels.LScmdParam,
    #                             )
    #                         )
    #                     }
    #                     self.cliOpt["commands"]["parameters"].update(list_settings)
    #                     self.cliOpt["commands"]["index"].update(
    #                         {
    #                             self.cliOpt["var"]["primary id key"]: copy.deepcopy(
    #                                 dataModels.parameters_index_struct
    #                             )
    #                         }
    #                     )

    #                     self.cliOpt["commands"]["index"][
    #                         self.cliOpt["var"]["primary id key"]
    #                     ]["parameters key"] = str(self.cliOpt["var"]["primary id key"])
    #                     self.cliOpt["commands"]["index"][
    #                         self.cliOpt["var"]["primary id key"]
    #                     ]["root index key"] = str(self.cliOpt["var"]["primary id key"])
    #                     self.cliOpt["commands"]["index"][
    #                         self.cliOpt["var"]["primary id key"]
    #                     ]["parent index key"] = str(
    #                         self.cliOpt["var"]["primary id key"]
    #                     )
    #                     self.add_qtreewidgetitem(
    #                         self.cliOpt["commands"]["QTreeWidgetItem"]["root"],
    #                         str(self.cliOpt["var"]["primary id key"]),
    #                     )
    #                     self.cliOpt["var"]["primary id key"] = str(
    #                         int(self.cliOpt["var"]["primary id key"]) + 1
    #                     )
    #                     self.cliOpt["var"]["number of commands"] = str(
    #                         int(self.cliOpt["var"]["number of commands"]) + 1
    #                     )

    #         self.update_code("functions.h", object_list[2], True)
    #         self.update_code("functions.cpp", object_list[2], True)
    #         self.update_code("parameters.h", object_list[2], True)
    #         self.update_code("setup.cpp", object_list[2], True)

    #     if object_list[0] != "builtin methods":
    #         _twi = self.cliOpt["config"]["tree"]["items"][object_list[0]][
    #             "QTreeWidgetItem"
    #         ][object_list[1]]
    #         combobox = self.cliOpt["config"]["tree"]["items"][object_list[0]][
    #             "QComboBox"
    #         ][object_list[1]]
    #         sub_dict = self.cliOpt["config"]["tree"]["items"][object_list[0]][
    #             object_list[1]
    #         ]["fields"]
    #         if combobox.currentText() == "Enabled":
    #             sub_dict["1"] = "       "
    #             sub_dict["3"] = True
    #             SettingsTreeMethods.logger.info(
    #                 str(sub_dict["2"].strip("\n")) + " enabled"
    #             )
    #             for col in range(self.ui.settings_tree.columnCount()):
    #                 _twi.setToolTip(col, _tt[1])
    #         elif (
    #             self.cliOpt["config"]["tree"]["items"][object_list[0]]["QComboBox"][
    #                 object_list[1]
    #             ].currentText()
    #             == "Disabled"
    #         ):
    #             sub_dict["1"] = "    // "
    #             sub_dict["3"] = False
    #             SettingsTreeMethods.logger.info(
    #                 str(sub_dict["2"].strip("\n")) + " disabled"
    #             )
    #             for col in range(self.ui.settings_tree.columnCount()):
    #                 _twi.setToolTip(col, _tt[0])
    #         SettingsTreeMethods.logger.debug(
    #             "self.cliOpt['config']['tree']['items']['{}'][{}]['fields']:".format(
    #                 object_list[0], object_list[1]
    #             ),
    #             json.dumps(
    #                 sub_dict, indent=2, sort_keys=False, default=lambda o: "object"
    #             ),
    #         )
    #         self.update_code("config.h", sub_dict["2"], True)

    # ## called when a user "activates" a tree item (by pressing enter)
    # def settings_tree_item_activated(self, item):
    #     # expand/collapse QTreeWidgetItem that has children, if it has them
    #     if item.childCount() > 0:
    #         if item.isExpanded():
    #             item.setExpanded(False)
    #         else:
    #             item.setExpanded(True)
    #         return
    #     object_list = str(item.data(4, 0)).split(",")
    #     SettingsTreeMethods.logger.info(object_list[2] + " selected")
    #     self.edit_settings_tree_item(item)

    # ## if the user double clicks on something, see if it is editable
    # def check_if_settings_tree_col_editable(self, item, column):
    #     # allow the third column to be editable with mouse clicks
    #     if column == 3:
    #         self.edit_settings_tree_item(item)

    # ## this is called any time an item changes; any time any column edits take place on settings tree, user or otherwise
    # def settings_tree_edit_complete(self, item, col):
    #     def log_edit(item, object_list, val):
    #         val_type = item.data(2, 0)
    #         if self.loading:
    #             SettingsTreeMethods.logger.info(
    #                 "set "
    #                 + object_list[2]
    #                 + " to "
    #                 + "'"
    #                 + str(val)
    #                 + "' "
    #                 + str(val_type)
    #             )
    #         else:
    #             SettingsTreeMethods.logger.info(
    #                 "User set "
    #                 + object_list[2]
    #                 + " to "
    #                 + "'"
    #                 + str(val)
    #                 + "' "
    #                 + str(val_type)
    #             )

    #     self.prompt_to_save = True
    #     self.windowtitle_set = False
    #     if col != 3:
    #         return
    #     val = str(item.data(3, 0))
    #     if "'" in val:
    #         return  # already repr
    #     object_string = str(item.data(4, 0))
    #     object_list = object_string.strip("\n").split(",")

    #     # dict position is 3 items
    #     if len(object_list) < 2:
    #         return
    #     if object_list[0] == "builtin methods":
    #         return
    #     object_list[1] = int(str(object_list[1]))

    #     # process output
    #     if object_list[0] == "process output":
    #         item.setText(3, str(repr(val)))
    #         self.cliOpt["process output"]["var"][object_list[2]] = val
    #         log_edit(item, object_list, val)
    #         self.update_code("setup.h", object_list[2], True)
    #         if object_list[2] == "outputToStream":
    #             self.update_code("setup.cpp", object_list[2], True)
    #         if object_list[2] == "defaultFunction":
    #             self.update_code("functions.h", object_list[2], True)
    #             self.update_code("functions.cpp", object_list[2], True)
    #         return

    #     # process parameters (setup.h)
    #     if object_list[0] == "process parameters":
    #         item.setText(3, "'" + str(val) + "'")
    #         log_edit(item, object_list, val)
    #         self.cliOpt["process parameters"]["var"][item.text(1)] = val
    #         self.update_code("setup.h", item.text(1), True)
    #         return

    #     # config.h
    #     sub_dict = self.cliOpt["config"]["tree"]["items"][object_list[0]][
    #         object_list[1]
    #     ]["fields"]
    #     tmp = ""
    #     if val == "enabled":
    #         tmp = True
    #     elif val == "disabled":
    #         tmp = False
    #     else:
    #         if val == "":
    #             tmp = 0
    #             item.setText(3, "'" + str(repr(tmp)) + "'")
    #         else:
    #             tmp = int(val)
    #             item.setText(3, "'" + str(repr(tmp)) + "'")
    #     if tmp == sub_dict["3"]:
    #         return
    #     # update the config dict
    #     sub_dict["3"] = tmp
    #     self.update_settings_tree_type_field_text(item)
    #     self.update_code("config.h", sub_dict["2"], True)
    #     log_edit(item, object_list, val)
    #     SettingsTreeMethods.logger.debug(
    #         str(
    #             "self.cliOpt['config']['tree']['items']['{}'][{}]['fields']:".format(
    #                 object_list[0], object_list[1]
    #             )
    #         )
    #         + "\n"
    #         + str(
    #             json.dumps(
    #                 sub_dict, indent=2, sort_keys=False, default=lambda o: "object"
    #             )
    #         )
    #     )

   

    # ## helper method to add children to container items
    # def set_up_child(
    #     self,
    #     dict_key,
    #     tree,
    #     parent,
    #     index_of_child,
    #     var_name,
    #     var_type,
    #     var_tooltip,
    #     var_initial_val,
    #     combobox=False,
    #     combobox_item_tooltips=[],
    # ):
    #     if tree["root"] == self.cliOpt["config"]["tree"]["root"]:
    #         access = dict_key
    #     else:
    #         access = var_name
    #     column_label_list = ["", var_name, var_type, str(repr(var_initial_val))]
    #     tree["items"][access]["QTreeWidgetItem"].update(
    #         {index_of_child: QTreeWidgetItem(parent, column_label_list)}
    #     )
    #     _twi = tree["items"][access]["QTreeWidgetItem"][index_of_child]
    #     dict_pos = dict_key + "," + str(index_of_child) + "," + var_name
    #     _twi.setData(4, 0, dict_pos)
    #     _twi.setFlags(_twi.flags() | Qt.ItemIsEditable)
    #     if var_tooltip != "" and var_tooltip != None:
    #         for col in range(self.ui.settings_tree.columnCount()):
    #             _twi.setToolTip(col, var_tooltip)
    #     if combobox == True:
    #         for col in range(self.ui.settings_tree.columnCount()):
    #             _twi.setToolTip(col, combobox_item_tooltips[0])
    #         tree["items"][access]["QComboBox"].update({index_of_child: QComboBox()})
    #         _cmb = tree["items"][access]["QComboBox"][index_of_child]
    #         _cmb.addItem("Disabled", False)
    #         _cmb.addItem("Enabled", True)
    #         if (
    #             combobox_item_tooltips
    #             and combobox_item_tooltips[0] != None
    #             and combobox_item_tooltips[0] != ""
    #         ):
    #             _cmb.setItemData(0, combobox_item_tooltips[0], Qt.ToolTipRole)
    #         if (
    #             combobox_item_tooltips
    #             and combobox_item_tooltips[1] != None
    #             and combobox_item_tooltips[1] != ""
    #         ):
    #             _cmb.setItemData(1, combobox_item_tooltips[1], Qt.ToolTipRole)
    #         _cmb.setObjectName(dict_pos)
    #         if var_initial_val == False:
    #             _cmb.setCurrentIndex(_cmb.findText("Disabled"))
    #         elif var_initial_val == True:
    #             _cmb.setCurrentIndex(_cmb.findText("Enabled"))
    #         _cmb.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLengthWithIcon)
    #         # _cmb.currentIndexChanged.connect(self.settings_tree_combo_box_index_changed)
    #         _cmb.currentTextChanged.connect(self.settings_tree_combo_box_index_changed)
    #         self.ui.settings_tree.setItemWidget(
    #             _twi,
    #             3,
    #             _cmb,
    #         )
    #     index_of_child += 1
    #     return index_of_child

    # ## this builds the entire MainWindow.ui.settings_tree
    # def build_lib_settings_tree(self):
    #     settings_tree = self.ui.settings_tree
    #     settings_tree.setHeaderLabels(("Section", "Macro Name", "Type", "Value"))
    #     # settings_tree.header().setSectionResizeMode(0, QHeaderView.Interactive)
    #     settings_tree.setMinimumWidth(400)
    #     settings_tree.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
    #     settings_tree.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)
    #     settings_tree.header().setSectionResizeMode(1, QHeaderView.ResizeToContents)
    #     settings_tree.header().setSectionResizeMode(2, QHeaderView.ResizeToContents)
    #     settings_tree.header().setSectionResizeMode(3, QHeaderView.ResizeToContents)

    #     settings_tree.header().setSectionResizeMode(0, QHeaderView.Stretch)
    #     settings_tree.header().setSectionResizeMode(1, QHeaderView.Stretch)
    #     settings_tree.header().setSectionResizeMode(2, QHeaderView.Stretch)
    #     settings_tree.header().setSectionResizeMode(3, QHeaderView.Stretch)

    #     settings_tree.setColumnCount(5)
    #     settings_tree.setSelectionMode(QAbstractItemView.SingleSelection)
    #     # 5th column holds object location in cliOpt
    #     settings_tree.setColumnHidden(4, 1)

    #     # use the text in _tree for self.ui.settings_tree field labels, build the tree
    #     for parent in SettingsTreeMethods._tree:
    #         index_of_child = 0
    #         dict_key = parent

    #         tree = self.cliOpt[dict_key]["tree"]
    #         is_config = True if dict_key == "config" else False
    #         # add parents to self.ui.settings_tree
    #         if not is_config:
    #             tree["root"] = QTreeWidgetItem(settings_tree, [dict_key, ""])
    #             tree["root"].setIcon(0, self.ui.commandLinkIcon)
    #         elif is_config:
    #             cfg_dict = self.cliOpt["config"]["tree"]["items"]
    #             cfg_path = self.session["opt"]["input_config_file_path"]
    #             tree["root"] = QTreeWidgetItem(
    #                 settings_tree, ["Input config: " + cfg_path, ""]
    #             )
    #             tree["root"].setIcon(0, self.ui.fileDialogContentsViewIcon)
    #             tree["root"].setToolTip(0, "Input config: " + cfg_path)
    #             # make these parents children of root using the keys from 'cfg_dict'

    #         if is_config:
    #             for subsection in SettingsTreeMethods._tree["config"]:
    #                 index_of_child = 0
    #                 tree["parents"][subsection]["QTreeWidgetItem"] = QTreeWidgetItem(
    #                     tree["root"], [subsection, "", "", ""]
    #                 )
    #                 for item in SettingsTreeMethods._tree["config"][subsection]:
    #                     var_initial_val = self.cliOpt["config"]["var"][subsection][item]
    #                     has_combobox = False
    #                     tooltip = SettingsTreeMethods._tree[dict_key][subsection][item][
    #                         "tooltip"
    #                     ]
    #                     combobox_tooltip = SettingsTreeMethods._tree[dict_key][
    #                         subsection
    #                     ][item]["tooltip"]
    #                     if (
    #                         SettingsTreeMethods._tree[dict_key][subsection][item][
    #                             "type"
    #                         ]
    #                         == "Enable/Disable"
    #                     ):
    #                         has_combobox = True
    #                         tooltip = ""
    #                     index_of_child = self.set_up_child(
    #                         subsection,
    #                         tree,
    #                         tree["parents"][subsection]["QTreeWidgetItem"],
    #                         index_of_child,
    #                         item,
    #                         SettingsTreeMethods._tree[dict_key][subsection][item][
    #                             "type"
    #                         ],
    #                         tooltip,
    #                         var_initial_val,
    #                         has_combobox,
    #                         combobox_tooltip,
    #                     )
    #         elif not is_config:
    #             for child in SettingsTreeMethods._tree[parent]:
    #                 var_initial_val = self.cliOpt[dict_key]["var"][child]
    #                 if (
    #                     child == "data delimiter sequences"
    #                     or child == "start stop data delimiter sequences"
    #                 ):
    #                     self.build_tree_table_widget(
    #                         index_of_child,
    #                         tree,
    #                         dict_key,
    #                         child,
    #                     )
    #                     index_of_child += 1
    #                 else:
    #                     has_combobox = False
    #                     tooltip = SettingsTreeMethods._tree[dict_key][child]["tooltip"]
    #                     combobox_tooltip = SettingsTreeMethods._tree[dict_key][child][
    #                         "tooltip"
    #                     ]
    #                     if (
    #                         SettingsTreeMethods._tree[dict_key][child]["type"]
    #                         == "Enable/Disable"
    #                     ):
    #                         has_combobox = True
    #                         tooltip = ""
    #                     index_of_child = self.set_up_child(
    #                         dict_key,
    #                         tree,
    #                         tree["root"],
    #                         index_of_child,
    #                         child,
    #                         SettingsTreeMethods._tree[dict_key][child]["type"],
    #                         tooltip,
    #                         var_initial_val,
    #                         has_combobox,
    #                         combobox_tooltip,
    #                     )

    #                 self.default_settings_tree_values.update(
    #                     {str(child).strip(): var_initial_val}
    #                 )

    #     settings_tree.setEditTriggers(self.ui.settings_tree.NoEditTriggers)
    #     # update cliOpt with new value when editing is complete
    #     settings_tree.itemChanged.connect(self.settings_tree_edit_complete)
    #     # check if user clicked on the column we want them to edit
    #     settings_tree.itemDoubleClicked.connect(
    #         self.check_if_settings_tree_col_editable
    #     )
    #     # check if user hit enter on an item
    #     settings_tree.itemActivated.connect(self.settings_tree_item_activated)
    #     self.settings_tree_button_toggles()
    #     settings_tree.setSelectionMode(QAbstractItemView.SingleSelection)

    # # end build_lib_settings_tree()

## settings_tree_table_methods.py
##
# # @file settings_tree_table_methods.py
# # @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
# # @brief MainWindow external methods
# # @version 1.0
# # @date 2022-07-08
# # @copyright Copyright (c) 2022
# # Copyright (C) 2022 Douglas Quigg (dstroy0) <dquigg123@gmail.com>
# # This program is free software; you can redistribute it and/or
# # modify it under the terms of the GNU General Public License
# # version 3 as published by the Free Software Foundation.

# from __future__ import absolute_import

# import copy

# # pyside imports
# from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex

# from PySide6.QtWidgets import (
#     QHeaderView,
#     QPushButton,
#     QTreeWidgetItem,
#     QAbstractItemView,
#     QSizePolicy,
#     QTableView,
#     QAbstractScrollArea,
# )


# class DelimitersTableViewModel(QAbstractTableModel):
#     """Display model for a delimiters table

#     Args:
#         QAbstractTableModel (class): This class specializes QAbstractTableModel
#     """

#     def __init__(self, parent, tree, cliopt, dict_pos, delimiters: dict) -> None:

#         super(DelimitersTableViewModel, self).__init__()
#         self._parent = parent
#         self.tree = tree
#         self.cliopt = cliopt
#         self.dict_pos = dict_pos
#         self.delimiters = delimiters
#         self.keys = list(self.delimiters.keys())
#         self.values = list(self.delimiters.values())
#         self.row_count = int(len(self.delimiters) + 1)
#         self.column_count = 2
#         self.editing = False
#         self.clicked_row = None

#         for i in range(self.row_count - 1):
#             parent.remove_row_buttons.append(QPushButton())
#             parent.remove_row_buttons[i].setIcon(parent.remove_row_button_icon)

#     def flags(self, index) -> Qt.ItemFlags:
#         if (
#             index.isValid()
#             and index.column() == 0
#             and index.row() < (self.rowCount() - 1)
#         ):
#             return (
#                 super().flags(index)
#                 | Qt.ItemIsSelectable
#                 | Qt.ItemIsEditable
#                 | Qt.ItemIsEnabled
#             )
#         else:
#             return super().flags(index) | Qt.ItemIsSelectable | Qt.ItemIsEnabled

#     def setData(self, index, value, role) -> bool:
#         if role in (Qt.DisplayRole, Qt.EditRole):
#             if not value:
#                 return False

#             clean_value = value.strip("<>")
#             if not clean_value:
#                 return False
#             self.cliopt[self.dict_pos[0]]["var"][self.dict_pos[2]][
#                 str(index.row())
#             ] = clean_value
#             self.dataChanged.emit(index, index)
#             table = self._parent.objectName().split(",")[2]
#             self._parent.logger.info(
#                 f"{table} table, row {index.row()+1} data changed to <{clean_value}>"
#             )
#         return True

#     def columnCount(self, parent: QModelIndex = None) -> int:        
#         return self.column_count

#     def rowCount(self, parent: QModelIndex = None) -> int:        
#         return int(len(self.cliopt[self.dict_pos[0]]["var"][self.dict_pos[2]]) + 1)

#     def ar(self) -> None:
#         row = self.rowCount() - 1
#         parent = self._parent.currentIndex()
#         self.insertRow(row, parent)

#     def insertRow(self, row: int, parent) -> bool:
#         self.beginInsertRows(parent, row, row)
#         start_len = len(self.cliopt[self.dict_pos[0]]["var"][self.dict_pos[2]])
#         self.cliopt[self.dict_pos[0]]["var"][self.dict_pos[2]].update(
#             {str(start_len): ""}
#         )        
#         self.insertRows(row, 1, parent)
#         self.endInsertRows()
#         self.insert_row_move_buttons(row)
#         self.dataChanged.emit(parent, parent)
#         self.layoutChanged.emit()
#         return super().insertRow(row, parent)

#     def insert_row_move_buttons(self, row: int):
#         self._parent.remove_row_buttons.append(QPushButton())
#         self._parent.remove_row_buttons[row].setIcon(
#             self._parent.remove_row_button_icon
#         )
#         index = self.index(row, 0)
#         self._parent.setIndexWidget(index, None)
#         index = self.index(row, 1)
#         self._parent.setIndexWidget(index, self._parent.remove_row_buttons[row])
#         self._parent.remove_row_buttons[row].clicked.connect(self.rr)
#         index = self.index(self.rowCount() - 1, 0)
#         self._parent.add_row_button = QPushButton("Add Delimiter")
#         self._parent.add_row_button.clicked.connect(self.ar)
#         self._parent.setIndexWidget(index, self._parent.add_row_button)

#     def rr(self):
#         row = self._parent.currentIndex().row()
#         parent = self._parent.currentIndex()
#         self.removeRow(row, parent)

#     def removeRow(self, row: int = None, parent=None) -> bool:
#         if not parent.isValid():
#             row = self._parent.currentIndex().row()
#             parent = self._parent.currentIndex()
#         print(f"remove row {row}")

#         self.beginRemoveRows(parent, row, row)
#         del self._parent.remove_row_buttons[row]
#         del self.cliopt[self.dict_pos[0]]["var"][self.dict_pos[2]][str(row)]
#         new_dict = copy.deepcopy(self.cliopt[self.dict_pos[0]]["var"][self.dict_pos[2]])

#         self.cliopt[self.dict_pos[0]]["var"][self.dict_pos[2]] = {}

#         i = 0
#         for key in new_dict:
#             self.cliopt[self.dict_pos[0]]["var"][self.dict_pos[2]].update(
#                 {str(i): new_dict[key]}
#             )
#             i += 1
#         self.removeRows(row, row, parent)

#         index = self.index(self.rowCount() - 1, 1)
#         self._parent.setIndexWidget(index, None)
#         index = self.index(self.rowCount() - 1, 0)
#         self._parent.setIndexWidget(index, self._parent.add_row_button)
#         self.endRemoveRows()
#         self.dataChanged.emit(parent, parent)
#         self.layoutChanged.emit()
#         return super().removeRow(row, parent)

#     def moveRow(
#         self,
#         sourceParent: QModelIndex,
#         sourceRow: int,
#         destinationParent: QModelIndex,
#         destinationChild: int,
#     ) -> bool:
#         self.beginMoveRows(
#             QModelIndex(), sourceRow, sourceRow, QModelIndex(), destinationChild
#         )

#         self.endMoveRows()
#         return super().moveRow(
#             sourceParent, sourceRow, destinationParent, destinationChild
#         )

#     def data(self, index: QModelIndex, role: int):
#         """Table data positioning.

#         Args:
#             index (QModelIndex): The model index.
#             role (Qt Role): What role is the data.

#         Returns:
#             str: data in the cell
#         """
#         if not index.isValid():
#             return None
#         elif (
#             index.column() == 0
#             and (index.row() - 1)
#             < (len(self.cliopt[self.dict_pos[0]]["var"][self.dict_pos[2]]) - 1)
#             and role == Qt.DisplayRole
#             or role == Qt.EditRole
#         ):
#             return (
#                 "<"
#                 + str(
#                     self.cliopt[self.dict_pos[0]]["var"][self.dict_pos[2]][
#                         str(index.row())
#                     ]
#                 )
#                 + ">"
#             )

#         # returns tooltips on a valid index if there are any for the cell
#         elif role == Qt.ToolTipRole:
#             if (index.row() - 1) < (len(self.cliopt[self.dict_pos[0]]["var"][self.dict_pos[2]]) - 1):
#                 if index.column() == 0:
#                     return str(f"type: {self.dict_pos[2]}, any char except the wildcard char is valid")
#                 else:
#                     return str(f"remove row {index.row()+1}")
#             else:
#                 if index.column() == 0:
#                     return str(f"add row to {self.dict_pos[2]} table")
#                 else:
#                     return None
#         else:
#             return None

#     def headerData(self, section: int, orientation: int, role: int):
#         if role == Qt.DisplayRole and orientation == Qt.Horizontal and section == 0:
#             return "Delimiters"
#         elif orientation == Qt.Vertical and role == Qt.DisplayRole:
#             if int(section) < int(self.rowCount() - 1):
#                 return str(section + 1)
#             else:
#                 return None
#         else:
#             return None

#     def edit_table_view(self, index: QModelIndex):
#         if index.isValid() and self.editing == False:
#             self.editing = True
#             self._parent.setCurrentIndex(index)
#             self._parent.edit(index)


# class DelimitersTableView(QTableView):
#     def __init__(
#         self,
#         logger,
#         cursor,
#         settings_tree,
#         cliopt,
#         tree,
#         container,
#         remove_row_button_icon,
#     ) -> None:
#         super(DelimitersTableView, self).__init__()
#         self.logger = logger
#         self.cursor_ = cursor
#         self.remove_row_button_icon = remove_row_button_icon
#         self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
#         dict_pos = container.data(4, 0).split(",")
#         self.setObjectName(str(container.data(4, 0)))

#         delimiters = cliopt[dict_pos[0]]["var"][dict_pos[2]]
#         self.remove_row_buttons = []
#         self.table_model = DelimitersTableViewModel(
#             self, tree, cliopt, dict_pos, delimiters
#         )
#         self.setModel(self.table_model)
#         self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
#         self.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
#         self.setSelectionMode(QAbstractItemView.SingleSelection)
#         settings_tree.setItemWidget(container, 0, self)

#         self.add_row_button = QPushButton("Add Delimiter")
#         self.add_row_button.clicked.connect(self.table_model.ar)
#         index = self.table_model.index(self.table_model.rowCount() - 1, 0)
#         self.setIndexWidget(index, self.add_row_button)

#         for i in range(len(self.remove_row_buttons)):
#             index = self.table_model.index(i, 1)
#             self.setIndexWidget(index, self.remove_row_buttons[i])
#             self.remove_row_buttons[i].clicked.connect(self.table_model.rr)

#         self.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
#         self.clicked.connect(self.table_model.edit_table_view)
#         self.clicked.connect(self.update_index)
#         self.pressed.connect(self.table_model.edit_table_view)

#     def update_index(self):
#         self.setCurrentIndex(self.indexAt(self.cursor_pos()))

#     def cursor_pos(self):
#         return self.cursor_.pos()

#     def dataChanged(self, topLeft, bottomRight, roles) -> None:
#         if self.table_model.editing == True:
#             self.table_model.editing = False
#             print("edit complete")
#         return super().dataChanged(topLeft, bottomRight, roles)


# # this is a helper class
# class SettingsTreeTableMethods(object):
#     ## the constructor
#     def __init__(self):
#         super(SettingsTreeTableMethods, self).__init__()
#         SettingsTreeTableMethods.logger = self.get_child_logger(__name__)

#     ## builds a table onto a tree widget item
#     def build_tree_table_widget(
#         self,
#         index,
#         tree,
#         dict_key,
#         dict_key2,
#     ):
#         dict_pos = str(dict_key) + "," + str(index) + "," + str(dict_key2)
#         # add parent tree item to root
#         tree["parents"][dict_key2] = QTreeWidgetItem(tree["root"], [dict_key2, ""])
#         # add treewidgetitem parent tree item to contain the table
#         tree["items"][dict_key2]["QTreeWidgetItem"] = QTreeWidgetItem(
#             tree["parents"][dict_key2], ["", ""]
#         )
#         tree_widget_item = tree["items"][dict_key2]["QTreeWidgetItem"]
#         # set the treewidgetitem column 4 (hidden to user) to positional data
#         tree_widget_item.setData(4, 0, dict_pos)
#         # make the treewidgetitem editable
#         tree_widget_item.setFlags(tree_widget_item.flags() | Qt.ItemIsSelectable)
#         # make the treewidgetitem span columns
#         tree_widget_item.setFirstColumnSpanned(True)

#         cursor = self.qcursor

#         logger = SettingsTreeTableMethods.logger

#         table = DelimitersTableView(
#             logger,
#             cursor,
#             self.ui.settings_tree,
#             self.cliOpt,
#             tree,
#             tree_widget_item,
#             self.ui.trashIcon,
#         )

#     # end settings_tree table functions


# # end of file


## command_tree.py
   # ## adds a single command to the tree
    # def add_qtreewidgetitem(
    #     self, parent: QTreeWidgetItem, dict_index: str
    # ) -> QTreeWidgetItem:
    #     """Adds QTreeWidgetItem at dict_index as a child to parent QTreeWidgetItem

    #     Args:
    #         parent (QTreeWidgetItem): The parent QTreeWidgetItem
    #         dict_index (str): the location of the child in the data model

    #     Returns:
    #         QTreeWidgetItem: the created QTreeWidgetItem on success, None on fail.
    #     """
    #     # error checking
    #     if dict_index == None:
    #         CommandTreeMethods.logger.info("no index, unable to add item to tree")
    #         return None
    #     elif dict_index == "" and self.loading == True:
    #         CommandTreeMethods.logger.info("loaded saved command ")
    #         return None
    #     elif dict_index == "" and self.loading == False:
    #         CommandTreeMethods.logger.info("user deleted a command from the tree")
    #         self.update_code("functions.h", "", False)
    #         self.update_code("functions.cpp", "", False)
    #         self.update_code("parameters.h", "", False)
    #         return None
    #     elif dict_index not in self.cliOpt["commands"]["parameters"]:
    #         CommandTreeMethods.logger.info("dict_index not found: " + str(dict_index))
    #         return None
    #     # end error checking
    #     command_parameters = self.cliOpt["commands"]["parameters"][dict_index]
    #     dict_pos = (
    #         dict_index + "," + dict_index + "," + command_parameters["commandString"]
    #     )
    #     self.cliOpt["commands"]["QTreeWidgetItem"]["container"][
    #         dict_index
    #     ] = QTreeWidgetItem(parent, [command_parameters["commandString"], ""])

    #     self.cliOpt["commands"]["QTreeWidgetItem"]["table"][
    #         dict_index
    #     ] = QTreeWidgetItem(
    #         self.cliOpt["commands"]["QTreeWidgetItem"]["container"][dict_index]
    #     )
    #     tree_item = self.cliOpt["commands"]["QTreeWidgetItem"]["container"][dict_index]
    #     self.cliOpt["commands"]["QTreeWidgetItem"]["table"][dict_index].setData(
    #         1, 0, dict_pos
    #     )
    #     tree_item.setData(1, 0, dict_pos)

    #     tree_item.setExpanded(True)

    #     self.build_command_parameters_table_view(
    #         dict_index, tree_item, command_parameters
    #     )
    #     self.cliOpt["commands"]["QTreeWidgetItem"]["container"][dict_index].setData(
    #         1, 0, dict_pos
    #     )
    #     self.cliOpt["commands"]["QTreeWidgetItem"]["table"][dict_index].setData(
    #         1, 0, dict_pos
    #     )
    #     self.command_tree_button_toggles()
    #     if self.loading:
    #         CommandTreeMethods.logger.info(
    #             "added saved command `"
    #             + command_parameters["commandString"]
    #             + "` to the command tree"
    #         )
    #     else:
    #         CommandTreeMethods.logger.info(
    #             "user added command `"
    #             + command_parameters["commandString"]
    #             + "` to the command tree"
    #         )
    #     self.update_code("functions.h", command_parameters["commandString"], True)
    #     self.update_code("functions.cpp", command_parameters["commandString"], True)
    #     self.update_code("parameters.h", command_parameters["commandString"], True)
    #     # return child
    #     return self.cliOpt["commands"]["QTreeWidgetItem"]["container"][dict_index]

    # ## scrubs command from data model
    # def scrub_command_from_datamodel(
    #     self, pos: str, tree_item: QTreeWidgetItem
    # ) -> None:
    #     """Removes everything related to the command from the display and data models

    #     Args:
    #         pos (str): position in self.cliOpt
    #         tree_item (QTreeWidgetItem): the tree item to be removed
    #     """
    #     # scrub the data model
    #     if pos in self.cliOpt["commands"]["parameters"]:
    #         command = self.cliOpt["commands"]["parameters"][pos]["commandString"]
    #         CommandTreeMethods.logger.info(
    #             "removing `" + command + "` from the command tree"
    #         )

    #     if tree_item != None:
    #         parent_treewidgetitem = self.cliOpt["commands"]["QTreeWidgetItem"]["root"]
    #         parent_treewidgetitem.removeChild(tree_item)

    #     if pos in self.cliOpt["commands"]["QTableView"]["models"]["arguments"]:
    #         del self.cliOpt["commands"]["QTableView"]["models"]["arguments"][pos]
    #     if pos in self.cliOpt["commands"]["QTableView"]["models"]["parameters"]:
    #         del self.cliOpt["commands"]["QTableView"]["models"]["parameters"][pos]
    #     if pos in self.cliOpt["commands"]["QTableView"]["tables"]["parameters"]:
    #         del self.cliOpt["commands"]["QTableView"]["tables"]["parameters"][pos]
    #     if pos in self.cliOpt["commands"]["QTableView"]["tables"]["arguments"]:
    #         del self.cliOpt["commands"]["QTableView"]["tables"]["arguments"][pos]
    #     if pos in self.cliOpt["commands"]["QTableView"]["container"]:
    #         del self.cliOpt["commands"]["QTableView"]["container"][pos]
    #     if pos in self.cliOpt["commands"]["QTableView"]["layout"]:
    #         del self.cliOpt["commands"]["QTableView"]["layout"][pos]
    #     if pos in self.cliOpt["commands"]["QTableView"]["splitter"]:
    #         del self.cliOpt["commands"]["QTableView"]["splitter"][pos]
    #     if str(pos) in self.cliOpt["commands"]["parameters"]:
    #         del self.cliOpt["commands"]["parameters"][str(pos)]
    #     if pos in self.cliOpt["commands"]["QTreeWidgetItem"]["container"]:
    #         del self.cliOpt["commands"]["QTreeWidgetItem"]["container"][pos]
    #     if pos in self.cliOpt["commands"]["QTreeWidgetItem"]["table"]:
    #         del self.cliOpt["commands"]["QTreeWidgetItem"]["table"][pos]
    #     if (
    #         pos in self.cliOpt["commands"]["index"]
    #         and self.cliOpt["commands"]["index"][pos]["parameters key"] == pos
    #     ):
    #         CommandTreeMethods.logger.debug(
    #             str(
    #                 "removing command index struct "
    #                 + str(pos)
    #                 + " "
    #                 + str(json.dumps(self.cliOpt["commands"]["index"][pos], indent=2))
    #             )
    #         )
    #         del self.cliOpt["commands"]["index"][pos]
    #     self.update_code("functions.h", "", False)
    #     self.update_code("functions.cpp", "", False)
    #     self.update_code("setup.cpp", "", False)
    #     self.update_code("parameters.h", "", False)

    # ## rem_qtreewidgetitem wrapper deprecated
    # def rem_command(self, object_list: list):
    #     """self.rem_qtreewidgetitem wrapper; deprecated

    #     Args:
    #         object_list (list): position of command in self.cliOpt
    #     """
    #     self.rem_qtreewidgetitem(object_list)
    #     self.prompt_to_save = True
    #     self.windowtitle_set = False
    #     self.set_main_window_title()
    #     self.command_tree_button_toggles()

    # # TODO fix rem_qtreewidgetitem
    # ## takes the command out of the tree and scrubs it from the data model and removes its QTreeWidgetItem from self.ui.command_tree
    # def rem_qtreewidgetitem(self, dict_pos: str) -> None:
    #     """removes QTreeWidgetItem and associated structures from cliOpt at dict_pos

    #     Args:
    #         dict_pos (str): cliOpt key
    #     """

    #     def pop_from_dict(pos, tree_item):
    #         match = False
    #         for _item in self.cliOpt["commands"]["index"]:
    #             if (
    #                 self.cliOpt["commands"]["index"][_item]["parameters key"]
    #                 == dict_pos[2]
    #             ):
    #                 match = True
    #                 break
    #         if match == True:
    #             result = self.cliOpt["commands"]["index"].pop(_item, None)
    #         else:
    #             result = self.cliOpt["commands"]["index"].pop(pos, None)
    #         if result != None:
    #             # the number of commands is equal to the len of the commands index
    #             self.cliOpt["var"]["number of commands"] = str(
    #                 len(self.cliOpt["commands"]["index"])
    #             )
    #             CommandTreeMethods.logger.info(
    #                 "removed key " + _item + ' from self.cliOpt["commands"]["index"]'
    #             )
    #         self.scrub_command_from_datamodel(pos, tree_item)
    #         # the number of commands is equal to the len of the commands index
    #         self.cliOpt["var"]["number of commands"] = str(
    #             len(self.cliOpt["commands"]["index"])
    #         )

    #     pos = dict_pos[1]
    #     if pos in self.cliOpt["commands"]["QTreeWidgetItem"]["container"]:
    #         tree_item = self.cliOpt["commands"]["QTreeWidgetItem"]["container"][pos]
    #     else:
    #         CommandTreeMethods.logger.info(
    #             "couldnt find QTreeWidgetItem for `" + str(pos) + "`"
    #         )
    #         tree_item = None

    #     # take the table widget out of the qtreewidgetitem ("table")
    #     if pos not in self.cliOpt["commands"]["QTreeWidgetItem"]["table"]:
    #         CommandTreeMethods.logger.info("qtreewidgetitem not in dict")
    #         return
    #     self.ui.command_tree.removeItemWidget(
    #         self.cliOpt["commands"]["QTreeWidgetItem"]["table"][pos], 0
    #     )

    #     children = []
    #     if pos in self.cliOpt["commands"]["index"]:
    #         child_list = self.cliOpt["commands"]["index"][pos]["child index key list"]
    #     else:
    #         pop_from_dict(pos, tree_item)
    #         return
    #     child_positions = [pos]
    #     pos_idx = 0
    #     prev_pos_idx = 0
    #     if bool(child_list):
    #         CommandTreeMethods.logger.info("looking for command children")
    #     else:
    #         pop_from_dict(pos, tree_item)
    #         return
    #     index_struct = self.cliOpt["commands"]["index"][pos]
    #     if index_struct["root index key"] == index_struct["parent index key"]:
    #         this_parent_index_key = self.cliOpt["commands"]["index"][pos][
    #             "parent index key"
    #         ]
    #         this_parent_index_struct = self.cliOpt["commands"]["index"][
    #             this_parent_index_key
    #         ]
    #         if pos in this_parent_index_struct["child index key list"]:
    #             this_parent_index_struct["child index key list"].remove(pos)
    #             CommandTreeMethods.logger.debug(
    #                 "pruning child "
    #                 + str(pos)
    #                 + " from child index key list of index "
    #                 + str(this_parent_index_key)
    #             )
    #     while bool(child_list):
    #         for item in child_list:
    #             if item in self.cliOpt["commands"]["QTreeWidgetItem"]["container"]:
    #                 child_treewidgetitem = self.cliOpt["commands"]["QTreeWidgetItem"][
    #                     "container"
    #                 ][item]
    #                 children.append(child_treewidgetitem)
    #                 child_positions.append(item)
    #                 pos_idx += 1
    #         child_list = self.cliOpt["commands"]["index"][child_positions[pos_idx]][
    #             "child index key list"
    #         ]
    #         if not bool(child_list):
    #             CommandTreeMethods.logger.info("no more command children found")
    #             break
    #         # increment sentinel breaks the loop if no more children are located and appended to [children]
    #         if pos_idx == prev_pos_idx:
    #             break
    #         else:
    #             prev_pos_idx = pos_idx

    #     # prune children
    #     for child in children:
    #         _object_list = child.data(1, 0).split(",")
    #         index = self.cliOpt["commands"]["index"]
    #         child_index = index[_object_list[1]]
    #         parent_index_key = child_index["parent index key"]
    #         if parent_index_key in index:
    #             parent_index = index[parent_index_key]
    #             parent_child_list = parent_index["child index key list"]
    #             if _object_list[1] in parent_child_list:
    #                 parent_child_list.remove(
    #                     _object_list[1]
    #                 )  # remove this child from the parent's list of children
    #         tree_item.removeChild(child)

    #     # remove children from cliOpt starting with the farthest leaf from Root
    #     for item in reversed(child_positions):
    #         pop_from_dict(item, tree_item)

    # ## builds a table view for a command using a custom model and populates it with the command's parameters
    # def build_command_parameters_table_view(
    #     self, dict_index: str, tree_item: QTreeWidgetItem, command_parameters: dict
    # ):
    #     """builds a table view for the QTreeWidgetItem at dict_index using command_parameters

    #     Args:
    #         dict_index (str): location in cliOpt
    #         tree_item (QTreeWidgetItem): the QTreeWidgetItem
    #         command_parameters (dict): command parameters dict
    #     """
    #     tree_item = self.cliOpt["commands"]["QTreeWidgetItem"]["table"][dict_index]
    #     table = CommandParametersTableWidget(
    #         command_parameters, tree_item, CommandTreeMethods.logger, self.qcursor
    #     )
    #     self.ui.command_tree.setItemWidget(tree_item, 0, table)

    # ## private method used by public methods rebuild_command_tree and build_command_tree
    # def _build_command_tree(self):
    #     """private method called by self.build_command_tree and self.rebuild_command_tree"""
    #     parent_index = self.cliOpt["commands"]["index"]
    #     for item in parent_index:
    #         # command root
    #         if (
    #             self.cliOpt["commands"]["index"][item]["parameters key"]
    #             == self.cliOpt["commands"]["index"][item]["root index key"]
    #             == self.cliOpt["commands"]["index"][item]["parent index key"]
    #         ):
    #             CommandTreeMethods.logger.info(
    #                 "adding "
    #                 + self.cliOpt["commands"]["parameters"][
    #                     self.cliOpt["commands"]["index"][item]["parameters key"]
    #                 ]["commandString"]
    #                 + " to self.ui.command_tree Root"
    #             )
    #             self.add_qtreewidgetitem(
    #                 self.cliOpt["commands"]["QTreeWidgetItem"]["root"],
    #                 self.cliOpt["commands"]["index"][item]["root index key"],
    #             )
    #         else:  # child command
    #             CommandTreeMethods.logger.info(
    #                 "adding "
    #                 + self.cliOpt["commands"]["parameters"][item]["commandString"]
    #                 + " to self.ui.command_tree, child of: "
    #                 + self.cliOpt["commands"]["parameters"][
    #                     self.cliOpt["commands"]["index"][item]["parent index key"]
    #                 ]["commandString"]
    #             )
    #             self.add_qtreewidgetitem(
    #                 self.cliOpt["commands"]["QTreeWidgetItem"]["container"][
    #                     self.cliOpt["commands"]["index"][item]["parent index key"]
    #                 ],
    #                 self.cliOpt["commands"]["index"][item]["parameters key"],
    #             )

    # ## rebuilds the command tree from scratch
    # def rebuild_command_tree(self):
    #     """clears self.ui.command_tree and rebuilds from scratch"""
    #     command_tree = self.ui.command_tree
    #     # empty entire tree of items
    #     command_tree.clear()
    #     self.cliOpt["commands"]["QTreeWidgetItem"][
    #         "root"
    #     ] = self.ui.command_tree.invisibleRootItem()
    #     self._build_command_tree()
    #     command_tree.setExpanded(True)
    #     self.command_tree_button_toggles()

    # ## adds items to self.ui.command_tree for display
    # # def build_command_tree(self):
    # # """adds items from cliOpt to self.ui.command_tree"""
    # # command_tree = self.ui.command_tree
    # # command_tree.setSelectionMode(QAbstractItemView.SingleSelection)
    # # # command_tree.
    # # command_tree.setHeaderLabels(["Command Tree", ""])
    # # command_tree.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)
    # # command_tree.setColumnCount(2)
    # # command_tree.setColumnHidden(1, 1)  # dict positional data
    # # # make root invisible
    # # self.cliOpt["commands"]["QTreeWidgetItem"][
    # #     "root"
    # # ] = self.ui.command_tree.invisibleRootItem()

    # # self._build_command_tree()
    # # self.command_tree = CommandTreeWidget(self, self.cliOpt, CommandTreeMethods.logger)
    # # self.command_tree_button_toggles()