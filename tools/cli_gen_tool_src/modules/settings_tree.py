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

from PySide6.QtWidgets import QHBoxLayout

from modules.data_models import dataModels
from modules.display_models import displayModels
from modules.widgets import SettingsTreeWidget

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
            self, self.cli_options, self.session, SettingsTreeMethods.logger
        )
        container.layout.addWidget(self.settings_tree)
        container.setLayout(container.layout)
        return self.settings_tree

    def rebuild_settings_tree(self):
        container = self.ui.settings_tree_container
        container.layout.removeWidget(self.settings_tree)
        self.settings_tree = SettingsTreeWidget(
            self, self.cli_options, self.session, SettingsTreeMethods.logger
        )
        container.layout.addWidget(self.settings_tree)


# end of file
