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

# imports
import copy
from PySide6.QtWidgets import QHBoxLayout
from modules.data_models import DataModels
from modules.widgets import CommandTreeWidget


## self.ui.command_tree methods
class CommandTree(object):
    ## CommandTree constructor
    def __init__(self) -> None:
        """constructor method"""
        super(CommandTree, self).__init__()
        CommandTree.logger = self.get_child_logger(__name__)

        # new cmd button
        self.ui.new_cmd_button.setEnabled(False)
        # edit button
        self.ui.edit_cmd_button.setEnabled(False)
        # delete button
        self.ui.delete_cmd_button.setEnabled(False)

        self.command_tree_buttons = copy.deepcopy(DataModels.button_dict)
        self.command_tree_buttons["buttons"].update(
            {
                "new": copy.deepcopy(DataModels.button_sub_dict),
                "edit": copy.deepcopy(DataModels.button_sub_dict),
                "delete": copy.deepcopy(DataModels.button_sub_dict),
                "collapse": copy.deepcopy(DataModels.button_sub_dict),
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
            self, self.cli_options, CommandTree.logger
        )
        container.layout.addWidget(self.command_tree)
        container.setLayout(container.layout)
        return self.command_tree

    def rebuild_command_tree(self):
        container = self.ui.command_tree_container
        container.layout.removeWidget(self.command_tree)
        self.command_tree = CommandTreeWidget(
            self, self.cli_options, CommandTree.logger
        )
        container.layout.addWidget(self.command_tree)


# end of file
