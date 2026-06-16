##
# @file settings_tree.py
# @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
# @brief settings tree
# @version 1.0.0
# @date 2023-05-22
# @copyright Copyright (c) 2023
# Copyright (C) 2023 Douglas Quigg (dstroy0) <dquigg123@gmail.com>
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 3 as published by the Free Software Foundation.

from __future__ import absolute_import
import copy
from PySide6.QtWidgets import QHBoxLayout
from modules.data_models import DataModels
from modules.display_models import DisplayModels
from modules.widgets import SettingsTreeWidget


# settings_tree methods
class SettingsTree(object):
    ## the constructor
    def __init__(self):
        super(SettingsTree, self).__init__()
        SettingsTree.logger = self.get_child_logger(__name__)
        SettingsTree._tree = DisplayModels._settings_tree_display
        self.settings_tree_buttons = copy.deepcopy(DataModels.button_dict)
        self.settings_tree_buttons["buttons"].update(
            {
                "edit": copy.deepcopy(DataModels.button_sub_dict),
                "clear": copy.deepcopy(DataModels.button_sub_dict),
                "default": copy.deepcopy(DataModels.button_sub_dict),
                "collapse": copy.deepcopy(DataModels.button_sub_dict),
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
            self, self.cli_options, self.session, SettingsTree.logger
        )
        container.layout.addWidget(self.settings_tree)
        container.setLayout(container.layout)
        return self.settings_tree

    def rebuild_settings_tree(self):
        container = self.ui.settings_tree_container
        container.layout.removeWidget(self.settings_tree)
        self.settings_tree = SettingsTreeWidget(
            self, self.cli_options, self.session, SettingsTree.logger
        )
        container.layout.addWidget(self.settings_tree)


# end of file
