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
from modules.data_models import dataModels
from PySide6.QtWidgets import (
    QTableView,
    QComboBox,
    QDialogButtonBox,
    QTreeWidget,
)


# mainwindow button methods class
class MainWindowButtons(object):
    def __init__(self):
        super(MainWindowButtons, self).__init__()
        MainWindowButtons.logger = self.get_child_logger(__name__)

    def get_tree_state(self, tree: QTreeWidget) -> dict:
        tree_state = copy.deepcopy(dataModels.button_tree_state_dict)
        tree_state["tree"] = tree
        tsi = tree.selectedItems()
        is_root = False
        if bool(tsi):
            tree_state["items selected"] = tsi
            tree_state["item selected"] = tsi[0]
            tree_state["index of top level item"] = tree.indexOfTopLevelItem(tsi[0])
            tree_state["current item index"] = tree.indexFromItem(tsi[0])
            tree_state["root item index"] = tree.rootIndex()
            tree_state["child count"] = tsi[0].childCount()
            tree_state["table widget"] = tree.itemWidget(tsi[0], 0)
            tree_state["combobox widget"] = tree.itemWidget(tsi[0], 3)
            tree_state["is expanded"] = tsi[0].isExpanded()
            if (
                tree_state["current item index"] == tree_state["root item index"]
                and tree_state["root item index"] != None
            ):
                is_root = True
        else:
            is_root = True
            tree_state["root item index"] = tree.rootIndex()
            tree_state["current item index"] = tree.currentIndex()
            tree_state["child count"] = tree.topLevelItemCount()
            tree_state["is expanded"] = tree.invisibleRootItem().isExpanded()
        tree_state["root item selected"] = is_root

        return tree_state

    def queue_collapse_button_text(self, button_dict: dict):
        text = None
        if bool(button_dict["item selected"]) and not bool(
            button_dict["tree"].invisibleRootItem() == button_dict["tree"].currentItem()
        ):
            if button_dict["is expanded"] == True:
                text = "Collapse"
            else:
                text = "Expand"
        elif (
            not bool(button_dict["item selected"])
            or button_dict["tree"].invisibleRootItem()
            == button_dict["tree"].currentItem()
            or button_dict["buttons"]["collapse"]["QPushButton"].text()
            == "Collapse All"
        ):
            text = "Expand All"
        elif button_dict["buttons"]["collapse"]["QPushButton"].text() == "Expand All":
            text = "Collapse All"

        if text != None:
            button_dict["buttons"]["collapse"]["text"] = text
        else:
            MainWindowButtons.logger.warning("collapse button text empty")

    def tree_expander(self, button_text: str, button_dict: dict):
        if not bool(button_dict["root item selected"]) and button_text == "Expand":
            button_dict["item selected"].setExpanded(True)
            button_dict["buttons"]["collapse"]["QPushButton"].setText("Collapse")
        elif not bool(button_dict["root item selected"]) and button_text == "Collapse":
            button_dict["item selected"].setExpanded(False)
            button_dict["buttons"]["collapse"]["QPushButton"].setText("Expand")
        elif bool(button_dict["root item selected"]) and button_text == "Expand All":
            button_dict["tree"].expandAll()
            button_dict["buttons"]["collapse"]["QPushButton"].setText("Collapse All")
        elif bool(button_dict["root item selected"]) and button_text == "Collapse All":
            button_dict["tree"].collapseAll()
            button_dict["buttons"]["collapse"]["QPushButton"].setText("Expand All")

    def set_tree_button_context(self, button_dict: dict):
        for i in button_dict["buttons"]:
            if i != "collapse":
                butt = button_dict["buttons"][i]
                if butt["text"] != None:
                    butt["QPushButton"].setText(butt["text"])
                    butt["text"] = None
                butt["QPushButton"].setEnabled(butt["enabled"])
            else:
                butt = button_dict["buttons"][i]
                butt["text"] = None
                if bool(button_dict["item selected"]) and not bool(
                    button_dict["root item selected"]
                ):
                    if bool(button_dict["is expanded"]):
                        butt["text"] = "Collapse"
                    else:
                        butt["text"] = "Expand"
                elif bool(button_dict["root item selected"]):
                    if bool(button_dict["is expanded"]):
                        butt["text"] = "Collapse All"
                    else:
                        butt["text"] = "Expand All"
                if butt["text"] != None:
                    butt["QPushButton"].setText(butt["text"])
                    butt["text"] = None
                butt["QPushButton"].setEnabled(butt["enabled"])

    def settings_tree_collapse_button(self):
        tree_state = self.get_tree_state(self.ui.settings_tree)
        tree_buttons = self.settings_tree_buttons
        tree_buttons.update(tree_state)
        self.tree_expander(
            tree_buttons["buttons"]["collapse"]["QPushButton"].text(), tree_buttons
        )
        if tree_buttons["root item selected"]:
            self.settings_tree_collapsed = (
                tree_buttons["tree"].invisibleRootItem().isExpanded()
            )

    def command_tree_collapse_button(self):
        tree_state = self.get_tree_state(self.ui.command_tree)
        tree_buttons = self.command_tree_buttons
        tree_buttons.update(tree_state)
        if tree_buttons["root item selected"]:
            self.command_tree_collapsed = tree_buttons["is expanded"]
        self.tree_expander(
            tree_buttons["buttons"]["collapse"]["QPushButton"].text(), tree_buttons
        )

    def settings_tree_button_toggles(self):
        tree_state = self.get_tree_state(self.ui.settings_tree)
        tree_buttons = self.settings_tree_buttons
        tree_buttons.update(tree_state)
        if (
            tree_buttons["item selected"]
            and tree_buttons["index of top level item"] == -1
            and tree_buttons["child count"] == 0
        ):
            # table widgets get special treatment, there is no default
            if isinstance(
                tree_buttons["table widget"],
                QTableView,
            ):
                tree_buttons["buttons"]["edit"]["enabled"] = True
                tree_buttons["buttons"]["clear"]["enabled"] = True
                tree_buttons["buttons"]["default"]["enabled"] = False
            # comboboxes can be edited and set to their default
            elif isinstance(
                tree_buttons["combobox widget"],
                QComboBox,
            ):
                tree_buttons["buttons"]["edit"]["enabled"] = True
                tree_buttons["buttons"]["clear"]["enabled"] = False
                tree_buttons["buttons"]["default"]["enabled"] = True
            else:
                tree_buttons["buttons"]["edit"]["enabled"] = True
                tree_buttons["buttons"]["clear"]["enabled"] = True
                tree_buttons["buttons"]["default"]["enabled"] = True
        # nothing selected
        else:
            tree_buttons["buttons"]["edit"]["enabled"] = False
            tree_buttons["buttons"]["clear"]["enabled"] = False
            tree_buttons["buttons"]["default"]["enabled"] = False
        self.set_tree_button_context(tree_buttons)

    def command_tree_button_toggles(self):
        tree_state = self.get_tree_state(self.ui.command_tree)
        tree_buttons = self.command_tree_buttons
        tree_buttons.update(tree_state)
        # new/edit/delete/command settings menu button enable/disable toggling
        if bool(tree_buttons["root item selected"]):
            tree_buttons["buttons"]["new"]["text"] = "New (root command)"
            tree_buttons["buttons"]["new"]["enabled"] = True
            tree_buttons["buttons"]["edit"]["enabled"] = False
            tree_buttons["buttons"]["edit"]["delete"] = False
        # if the list is NOT empty (truthy)
        elif not bool(tree_buttons["root item selected"]) and bool(
            tree_buttons["item selected"]
        ):
            # something on the command tree is selected
            _object_list = tree_buttons["item selected"].data(1, 0).split(",")
            _item_matched_builtin = False
            for item in self.ih_builtins:
                # determine if the something selected is an InputHandler builtin
                if _object_list[2] == item:
                    _item_matched_builtin = True
                    break
            if _item_matched_builtin:  # item selected is an InputHandler builtin
                tree_buttons["buttons"]["new"]["text"] = "New"
                tree_buttons["buttons"]["new"]["enabled"] = False
                tree_buttons["buttons"]["edit"]["enabled"] = False
                tree_buttons["buttons"]["edit"]["delete"] = True
            else:  # item selected is NOT an InputHandler builtin
                # give user option to add children to this command
                tree_buttons["buttons"]["new"]["text"] = "New (child command)"
                tree_buttons["buttons"]["new"]["enabled"] = True
                tree_buttons["buttons"]["edit"]["enabled"] = True
                tree_buttons["buttons"]["edit"]["delete"] = True
        else:
            tree_buttons["buttons"]["new"]["text"] = "New"
            tree_buttons["buttons"]["new"]["enabled"] = False
            tree_buttons["buttons"]["edit"]["enabled"] = False
            tree_buttons["buttons"]["edit"]["delete"] = False
        self.set_tree_button_context(tree_buttons)

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
