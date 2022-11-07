##
# @file mainwindow_buttons.py
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

import copy

from PySide6.QtWidgets import QTableWidget, QComboBox, QDialogButtonBox, QTreeWidgetItem
from modules.logging_setup import Logger


# mainwindow button methods class
class MainWindowButtons(object):
    def __init__(self):
        super(MainWindowButtons, self).__init__()
        MainWindowButtons.logger = Logger.get_child_logger(self.logger, __name__)

    def settings_tree_collapse_button(self):
        item_selected = self.ui.settings_tree.selectedItems()
        button = self.ui.settings_tree_collapse_button
        if item_selected:
            if item_selected[0] and item_selected[0].isExpanded():
                self.ui.settings_tree.collapseItem(item_selected[0])
                button.setText("Expand")
            elif item_selected[0] and not item_selected[0].isExpanded():
                self.ui.settings_tree.expandItem(item_selected[0])
                button.setText("Collapse")
        else:
            if button.text() == "Collapse All":
                self.ui.settings_tree.collapseAll()
                button.setText("Expand All")
                return
            elif button.text() == "Expand All":
                self.ui.settings_tree.expandAll()
                button.setText("Collapse All")
                return

    def command_tree_collapse_button(self):
        item_selected = self.ui.command_tree.selectedItems()
        button = self.ui.command_tree_collapse_button
        if item_selected:
            if item_selected[0] and item_selected[0].isExpanded():
                self.ui.command_tree.collapseItem(item_selected[0])
                button.setText("Expand")
            elif item_selected[0] and not item_selected[0].isExpanded():
                self.ui.command_tree.expandItem(item_selected[0])
                button.setText("Collapse")
        else:
            if button.text() == "Collapse All":
                self.ui.command_tree.collapseAll()
                button.setText("Expand All")
                return
            elif button.text() == "Expand All":
                self.ui.command_tree.expandAll()
                button.setText("Collapse All")
                return
    
    def settings_tree_button_toggles(self):
        _item_selected = self.ui.settings_tree.selectedItems()
        if _item_selected and _item_selected[0].isExpanded():
            self.ui.settings_tree_collapse_button.setText("Collapse")
        elif _item_selected and not _item_selected[0].isExpanded():
            self.ui.settings_tree_collapse_button.setText("Expand")
        else:
            if self.ui.settings_tree.isExpanded(self.ui.settings_tree.rootIndex()):
                self.ui.settings_tree_collapse_button.setText("Collapse All")
            else:
                self.ui.settings_tree_collapse_button.setText("Expand All")
        # setting selected
        if (
            _item_selected
            and self.ui.settings_tree.indexOfTopLevelItem(_item_selected[0]) == -1
            and _item_selected[0].childCount() == 0
        ):
            table_widget = self.ui.settings_tree.itemWidget(_item_selected[0], 0)
            combobox_widget = self.ui.settings_tree.itemWidget(_item_selected[0], 3)
            # table widgets get special treatment, there is no default
            if isinstance(
                table_widget,
                QTableWidget,
            ):
                item = table_widget.currentItem()
                if item:
                    self.ui.edit_setting_button.setEnabled(True)
                    self.ui.clear_setting_button.setEnabled(True)
                    self.ui.default_setting_button.setEnabled(False)
            # comboboxes can be edited and set to their default
            elif isinstance(
                combobox_widget,
                QComboBox,
            ):
                self.ui.edit_setting_button.setEnabled(True)
                self.ui.clear_setting_button.setEnabled(False)
                self.ui.default_setting_button.setEnabled(True)
            else:
                self.ui.edit_setting_button.setEnabled(True)
                self.ui.clear_setting_button.setEnabled(True)
                self.ui.default_setting_button.setEnabled(True)
        # nothing selected
        else:
            self.ui.edit_setting_button.setEnabled(False)
            self.ui.clear_setting_button.setEnabled(False)
            self.ui.default_setting_button.setEnabled(False)            

    def command_menu_button_toggles(self):
        # method internal var
        # inputhandler builtin commands
        _builtin_commands = self.ih_builtins
        # command_tree root item
        _root = self.cliOpt["commands"]["QTreeWidgetItem"]["root"]
        # selected items list (only one selection possible)
        _items = self.ui.command_tree.selectedItems()
        # did the selection match a builtin
        _item_matched_builtin = False
        # populated when selection is non-root and not NULL
        _object_list = []
        # if an item is selected, this will be a memory location, else it is false
        _item_selected = False
        # if the selected item is root, this is True
        _item_selected_is_root = False
        
        
        if _items and _items[0].isExpanded():
            self.ui.command_tree_collapse_button.setText("Collapse")
        elif _items and not _items[0].isExpanded():
            self.ui.command_tree_collapse_button.setText("Expand")
        else:
            if self.ui.command_tree.currentIndex() == self.ui.command_tree.rootIndex():
                _item_selected_is_root = True
                if self.ui.command_tree.isExpanded(self.ui.command_tree.rootIndex()):
                    self.ui.command_tree_collapse_button.setText("Collapse All")
                else:
                    self.ui.command_tree_collapse_button.setText("Expand All")
        
        # new/edit/delete/command settings menu button enable/disable toggling
        if _item_selected_is_root:
            # new button
            self.ui.new_cmd_button.setText("New (root command)")
            self.ui.new_cmd_button.setEnabled(True)
            # edit button
            self.ui.edit_cmd_button.setEnabled(False)
            # delete button
            self.ui.delete_cmd_button.setEnabled(False)                
            return  # root tree item is selected, give user option to create new root command
        
        # if the list is NOT empty (truthy)
        if _items:
            # something on the command tree is selected
            _item_selected = _items[0]                                        

            if _item_selected:  # something is selected
                _object_list = _item_selected.data(1, 0).split(",")
                for (
                    item
                ) in (
                    _builtin_commands
                ):  # determine if the something selected is an InputHandler builtin
                    if _object_list[2] == item:
                        _item_matched_builtin = True
                        break
                if _item_matched_builtin:  # item selected is an InputHandler builtin
                    # new button
                    self.ui.new_cmd_button.setText("New")
                    self.ui.new_cmd_button.setEnabled(False)
                    # edit button
                    self.ui.edit_cmd_button.setEnabled(False)
                    # delete button
                    self.ui.delete_cmd_button.setEnabled(True)
                else:  # item selected is NOT an InputHandler builtin
                    # give user option to add children to this command
                    # new button
                    self.ui.new_cmd_button.setText("New (child command)")
                    self.ui.new_cmd_button.setEnabled(True)
                    # edit button
                    self.ui.edit_cmd_button.setEnabled(True)
                    # delete button
                    self.ui.delete_cmd_button.setEnabled(True)

        else:
            # nothing is selected, disable all buttons
            _item_selected = False
            # new button
            self.ui.new_cmd_button.setText("New")
            self.ui.new_cmd_button.setEnabled(False)
            # edit button
            self.ui.edit_cmd_button.setEnabled(False)
            # delete button
            self.ui.delete_cmd_button.setEnabled(False)

    # MainWindow buttons
    # tab 1
    def clicked_edit_tab_one(self):
        MainWindowButtons.logger.info("clicked tab 1 edit")
        if self.ui.settings_tree.currentItem() != None:
            object_list = self.ui.settings_tree.currentItem().data(4, 0).split(",")
            if (
                object_list[2] == "data delimiter sequences"
                or object_list[2] == "start stop data delimiter sequences"
            ):
                table_widget = self.ui.settings_tree.itemWidget(
                    self.ui.settings_tree.currentItem(), 0
                )
                items = table_widget.selectedItems()
                item = items[0]
                table_widget.editItem(item)
                self.update_code("setup.h", object_list[2], True)
                return
            self.ui.settings_tree.editItem(self.ui.settings_tree.currentItem(), 3)

    def clicked_clear_tab_one(self):
        MainWindowButtons.logger.info("clicked tab 1 clear")
        if self.ui.settings_tree.currentItem() != None:
            object_list = self.ui.settings_tree.currentItem().data(4, 0).split(",")
            if (
                object_list[2] == "data delimiter sequences"
                or object_list[2] == "start stop data delimiter sequences"
            ):
                table_widget = self.ui.settings_tree.itemWidget(
                    self.ui.settings_tree.currentItem(), 0
                )
                items = table_widget.selectedItems()
                item = items[0]
                row = table_widget.row(item)
                if row < table_widget.rowCount():
                    clear_item = table_widget.item(row, 0)
                    clear_item.setText("")
                    self.update_code("setup.h", object_list[2], True)
                self.cliOpt["process parameters"]["var"][object_list[2]] = {}
                for i in range(table_widget.rowCount() - 1):
                    self.cliOpt["process parameters"]["var"][object_list[2]].update(
                        {i: table_widget.item(i, 0).text().strip("'")}
                    )
                return
            self.ui.settings_tree.currentItem().setData(3, 0, "")

    def clicked_default_tab_one(self):
        tree_item = self.ui.settings_tree.currentItem()
        if tree_item != None:
            widget = self.ui.settings_tree.itemWidget(tree_item, 3)
            object_list = tree_item.data(4, 0).split(",")
            if isinstance(widget, QComboBox):
                bool_default = self.default_settings_tree_values[object_list[2]]
                if bool_default == True:
                    default_index = "Enabled"
                else:
                    default_index = "Disabled"
                widget.setCurrentIndex(widget.findText(default_index))
                MainWindowButtons.logger.info(
                    str(
                        object_list[0]
                        + " "
                        + object_list[2]
                        + " set to default: "
                        + default_index
                    )
                )
            else:
                default_val = str(
                    self.default_settings_tree_values[str(tree_item.data(1, 0))]
                )
                tree_item.setData(3, 0, default_val)
                MainWindowButtons.logger.info(
                    str(
                        object_list[0]
                        + " "
                        + object_list[2]
                        + " set to default: "
                        + default_val
                    )
                )

    # tab 2
    def clicked_edit_tab_two(self):
        MainWindowButtons.logger.info("edit command")
        self.clicked_command_settings_menu_button_tab_two(True)

    def clicked_new_cmd_button(self):
        if "(root command)" in self.ui.new_cmd_button.text():
            self.selected_command_is_root = True
            MainWindowButtons.logger.info(
                "user clicked new command button with root context"
            )
            self.ui.commandParameters.setWindowTitle("Root Command Parameters")
            fields = copy.deepcopy(self.command_parameters_input_field_settings)
            fields["parentId"]["value"] = 0
            fields["parentId"]["enabled"] = False
            fields["commandId"]["value"] = 0
            fields["commandId"]["enabled"] = False
            fields["commandDepth"]["value"] = 0
            fields["commandDepth"]["enabled"] = False
            self.commandparameters_set_fields(fields)
            self.ui.commandParameters.exec()
        elif "(child command)" in self.ui.new_cmd_button.text():
            self.selected_command_is_root = False
            _items = self.ui.command_tree.selectedItems()
            self.child_command_parent = _items[0]
            object_list = self.child_command_parent.data(1, 0).split(",")
            self.child_command_parent = self.cliOpt["commands"]["QTreeWidgetItem"][
                "container"
            ][object_list[0]]
            MainWindowButtons.logger.info(
                "user clicked new command button with child context"
            )
            self.ui.commandParameters.setWindowTitle("Child Command Parameters")
            self.commandparameters_set_fields(
                self.command_parameters_input_field_settings
            )
            self.ui.commandParameters.exec()

    # TODO fix delete
    def clicked_delete_tab_two(self) -> None:
        MainWindowButtons.logger.info("clicked tab two delete")
        # command_tree root item
        _root = self.cliOpt["commands"]["QTreeWidgetItem"]["root"]
        # selected items list (only one selection possible)
        _items = self.ui.command_tree.selectedItems()
        # populated when selection is non-root and not NULL
        _object_list = []
        # if an item is selected, this will be a memory location, else it is false
        _item_selected = False
        # if the selected item is root, this is True
        # _item_selected_is_root = False
        _builtin_commands = self.ih_builtins
        _item_matched_builtin = False
        _cmdprm = self.cliOpt["commands"]["parameters"]

        # if the list is NOT empty (truthy)
        if bool(_items):
            # something on the command tree is selected
            _item_selected = _items[0]
            if _item_selected == _root:
                # _item_selected_is_root = True
                MainWindowButtons.logger.warning("cannot delete tree root")
                return
            else:
                _object_list = _item_selected.data(1, 0).split(",")
                for (
                    item
                ) in (
                    _builtin_commands
                ):  # determine if the something selected is an InputHandler builtin
                    if _object_list[2] == item:
                        _item_matched_builtin = True
                        break
                if _item_matched_builtin:
                    self.cliOpt["builtin methods"]["var"][_object_list[2]] = False
                    _cmb = self.cliOpt["builtin methods"]["tree"]["items"][
                        _object_list[2]
                    ]["QComboBox"]
                    # there's only one item in the builtin but the key isn't known here.
                    for item in _cmb:
                        if not isinstance(_cmb[item], str):
                            _cmb[item].setCurrentIndex(_cmb[item].findText("Disabled"))
                self.rem_command(_object_list)

    def clicked_command_settings_menu_button_tab_two(self, edit_item=False):
        MainWindowButtons.logger.info("opened command settings menu")
        # command_tree root item
        _root = self.cliOpt["commands"]["QTreeWidgetItem"]["root"]
        # selected items list (only one selection possible)
        _items = self.ui.command_tree.selectedItems()
        # populated when selection is non-root and not NULL
        _object_list = []
        # if an item is selected, this will be a memory location, else it is false
        _item_selected = False
        # if the selected item is root, this is True
        _item_selected_is_root = False
        _builtin_commands = self.ih_builtins
        _item_matched_builtin = False
        _cmdprm = self.cliOpt["commands"]["parameters"]

        # if the list is NOT empty (truthy)
        if bool(_items):
            # something on the command tree is selected
            _item_selected = _items[0]
            if _item_selected == _root:
                _item_selected_is_root = True
            else:
                _table_widget = self.ui.command_tree.itemWidget(
                    self.ui.command_tree.currentItem(), 0
                )
                _object_list = _item_selected.data(1, 0).split(",")
                for (
                    item
                ) in (
                    _builtin_commands
                ):  # determine if the something selected is an InputHandler builtin
                    if _object_list[2] == item:
                        _item_matched_builtin = True
                        # disable the reset button if the item selected is a builtin
                        self.ui.commandParameters.dlg.buttonBox.button(
                            QDialogButtonBox.Reset
                        ).setEnabled(False)
                        break

            # if item is selected edit it
            if not _item_selected_is_root:
                if _root.indexOfChild(_item_selected) != -1:
                    self.selected_command_is_root = True
                else:
                    self.selected_command_is_root = False
                _sub = _cmdprm[_object_list[0]]
                _arg_handling = "No arguments"
                _return_function = ""
                if _sub["commandArgumentHandling"] == "UI_ARG_HANDLING::one_type":
                    _arg_handling = "Single argument type"
                    _return_function = _sub["functionName"]
                elif _sub["commandArgumentHandling"] == "UI_ARG_HANDLING::type_arr":
                    _arg_handling = "Argument type array"
                    _return_function = _sub["functionName"]
                fields = copy.deepcopy(self.command_parameters_input_field_settings)
                fields["functionName"]["value"] = _return_function
                fields["functionName"]["enabled"] = not _item_matched_builtin
                fields["commandString"]["value"] = _sub["commandString"]
                fields["commandString"]["enabled"] = not _item_matched_builtin
                fields["commandLength"]["value"] = _sub["commandLength"]
                fields["commandLength"]["enabled"] = not _item_matched_builtin
                fields["parentId"]["value"] = _sub["parentId"]
                fields["parentId"]["enabled"] = not _item_matched_builtin
                fields["commandId"]["value"] = _sub["commandId"]
                fields["commandId"]["enabled"] = not _item_matched_builtin
                fields["commandHasWildcards"]["value"] = _sub["commandHasWildcards"]
                fields["commandHasWildcards"]["enabled"] = not _item_matched_builtin
                fields["commandDepth"]["value"] = _sub["commandDepth"]
                fields["commandDepth"]["enabled"] = not _item_matched_builtin
                fields["commandSubcommands"]["value"] = _sub["commandSubcommands"]
                fields["commandSubcommands"]["enabled"] = not _item_matched_builtin
                fields["commandArgumentHandling"]["value"] = _arg_handling
                fields["commandArgumentHandling"]["enabled"] = not _item_matched_builtin
                fields["commandMinArgs"]["value"] = _sub["commandMinArgs"]
                fields["commandMinArgs"]["enabled"] = not _item_matched_builtin
                fields["commandMaxArgs"]["value"] = _sub["commandMaxArgs"]
                fields["commandMaxArgs"]["enabled"] = not _item_matched_builtin
                fields["commandArguments"]["value"] = _sub["commandArguments"]
                fields["commandArguments"]["enabled"] = not _item_matched_builtin
                self.commandparameters_set_fields(fields)
                self.ui.commandParameters.setWindowTitle(
                    str(fields["commandString"]["value"]) + " Command Parameters"
                )
                self.selected_command = _item_selected
                self.ui.commandParameters.exec()
            else:
                # if item not selected
                self.clicked_new_cmd_button()


# end of file
