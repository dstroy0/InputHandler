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

from PySide6.QtWidgets import QTableWidget, QComboBox
from res.modules.logging_setup import Logger


# mainwindow button methods class
class MainWindowButtons(object):
    def __init__(self):
        super(MainWindowButtons, self).__init__()
        MainWindowButtons.logger = Logger.get_child_logger(self.logger, __name__)

    def settings_tree_button_toggles(self):
        _item_selected = self.ui.settings_tree.selectedItems()
        # setting selected
        if (
            _item_selected
            and self.ui.settings_tree.indexOfTopLevelItem(_item_selected[0]) == -1
            and _item_selected[0].childCount() == 0
        ):
            table_widget = self.ui.settings_tree.itemWidget(_item_selected[0], 0)
            combobox_widget = self.ui.settings_tree.itemWidget(_item_selected[0], 3)
            object_list = _item_selected[0].data(4, 0).split(",")
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
        _builtin_commands = ["listSettings", "listCommands"]
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

        # if the list is NOT empty (truthy)
        if _items:
            # something on the command tree is selected
            _item_selected = _items[0]
            if _item_selected == _root:
                _item_selected_is_root = True

            # new/edit/delete/command settings menu button enable/disable toggling
            if _item_selected_is_root:
                # new button
                self.ui.new_cmd_button.setText("New (root command)")
                self.ui.new_cmd_button.setEnabled(True)
                # edit button
                self.ui.edit_cmd_button.setEnabled(False)
                # delete button
                self.ui.delete_cmd_button.setEnabled(False)
                # command settings menu button
                self.ui.cmd_settings_menu_button.setEnabled(False)
                return  # root tree item is selected, give user option to create new root command

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
                    # command settings menu button
                    self.ui.cmd_settings_menu_button.setEnabled(True)
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
            # command settings menu button
            self.ui.cmd_settings_menu_button.setEnabled(False)

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
    # TODO

    def clicked_edit_tab_two(self):
        print("clicked tab 2 edit")

    # TODO

    def clicked_new_cmd_button(self):
        print("clicked tab 2 new")

    # TODO

    def clicked_delete_tab_two(self):
        print("clicked tab 2 delete")

    def clicked_command_settings_menu_button_tab_two(self):
        MainWindowButtons.logger.info("clicked open command settings menu")
        self.ui.commandParameters.exec()


# end of file
