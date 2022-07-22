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
from res.modules.logging_setup import Logger

# mainwindow button methods class
class MainWindowButtons(object):
    def __init__(self):
        super(MainWindowButtons,self).__init__()
        MainWindowButtons.logger = Logger.get_child_logger(self.logger,__name__)
    
    # MainWindow buttons
    # tab 1
    # TODO
    def clicked_edit_tab_one(self):
        MainWindowButtons.logger.info("clicked tab 1 edit")
        if self.ui.settings_tree.currentItem() != None:
            self.ui.settings_tree.editItem(self.ui.settings_tree.currentItem(),3)            

    # TODO
    def clicked_clear_tab_one(self):
        MainWindowButtons.logger.info("clicked tab 1 clear")
        if self.ui.settings_tree.currentItem() != None:
            self.ui.settings_tree.currentItem().setData(3,0,0)
    
    # TODO
    def clicked_default_tab_one(self):
        MainWindowButtons.logger.info("clicked tab 1 default")

    # tab 2
    # TODO

    def clicked_edit_tab_two(self):
        print("clicked tab 2 edit")

    # TODO

    def clicked_new_tab_two(self):
        print("clicked tab 2 new")

    # TODO

    def clicked_delete_tab_two(self):
        print("clicked tab 2 delete")

    def clicked_open_command_settings_menu_tab_two(self):
        print("clicked open command settings menu")
        self.ui.commandParameters.exec()
