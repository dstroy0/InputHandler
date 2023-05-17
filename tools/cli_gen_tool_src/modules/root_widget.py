##
# @file root_widget.py
# @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
# @brief InputHandler CLI generation tool
# @version 1.0
# @date 2023-05-16
# @copyright Copyright (c) 2023
# Copyright (C) 2023 Douglas Quigg (dstroy0) <dquigg123@gmail.com>
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 3 as published by the Free Software Foundation.


from PySide6.QtWidgets import QWidget
## mainwindow runs on top of "RootWidget"
class RootWidget(QWidget, object):
    def __init__(self, parent) -> None:
        super(RootWidget, self).__init__()
        self._parent = parent
        self.setObjectName("root")
        

    # shim
    def import_methods(self):
        self.app = self._parent.app
        self.mainwindow_screen = self._parent.mainwindow_screen
        self.create_qdialog = self._parent.create_qdialog
        self.write_cli_gen_tool_json = self._parent.write_cli_gen_tool_json
        self.write_json = self._parent.write_json
        self.read_json = self._parent.read_json
        self.create_file_error_qdialog = self._parent.create_file_error_qdialog
        self.get_project_dir = self._parent.get_project_dir
        self.open_file = self._parent.open_file

        self.root_log_handler = self._parent.root_log_handler
        self.setup_file_handler = self._parent.setup_file_handler
        self.get_child_logger = self._parent.get_child_logger
        self.set_up_window_history_logger = self._parent.set_up_window_history_logger
        self.logger = self.root_log_handler

        self.lib_root_path = self._parent.lib_root_path

        self.lib_version = self._parent.lib_version

        self.inputhandler_save_path = self._parent.inputhandler_save_path
        self.user_home_dir = self._parent.user_home_dir
        self.set_up_session = self._parent.set_up_session
        
        self.version = self._parent.version
        self.splashscreen_duration = self._parent.splashscreen_duration

