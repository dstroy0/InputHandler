##
# @file preferences.py
# @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
# @brief MainWindow external methods
# @version 1.0
# @date 2022-08-23
# @copyright Copyright (c) 2022
# Copyright (C) 2022 Douglas Quigg (dstroy0) <dquigg123@gmail.com>
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 3 as published by the Free Software Foundation.

from __future__ import absolute_import
from res.modules.logging_setup import Logger
from PySide6.QtWidgets import QFileDialog
from PySide6.QtCore import QFile, Qt


class PreferencesMethods(object):
    def __init__(self) -> None:
        super(PreferencesMethods, self).__init__()
        PreferencesMethods.logger = Logger.get_child_logger(self.logger, __name__)

    def save_preferences(self):
        config_path = self.preferences.dlg.config_path_input.text()
        PreferencesMethods.logger.info("preferences set")

    def reset_preferences(self):
        config_path = self.session["opt"]["input_config_file_path"]
        self.preferences.dlg.config_path_input.setText(str(config_path))
        PreferencesMethods.logger.info(
            "preferences dialog cancelled, config path reset to: " + str(config_path)
        )

    def get_config_file(self):
        dlg = QFileDialog(self)
        fileName = dlg.getOpenFileName(
            self,
            "InputHandler config file name",
            "",
            "config.h",
            options=QFileDialog.DontUseNativeDialog,
        )
        if fileName[0] == "":
            PreferencesMethods.logger.info("browse for config cancelled.")
            return
        fqname = fileName[0]
        file = QFile(fqname)
        self.session["opt"]["input_config_file_path"] = fqname
        self.preferences.dlg.config_path_input.setText(str(fqname))
        self.preferences.dlg.config_path_input.setToolTip(str(fqname))
        self.app.restart()

    def set_window_log_level(self, index):
        index_val = self.preferences.dlg.windowLogLevelComboBox.currentData()
        Logger.session_history_log_level = index_val
        self.set_log_levels()
        PreferencesMethods.logger.warning(
            "Session history log level set to : " + Logger.level_lookup[index_val]
        )

    def set_file_log_level(self, index):
        index_val = self.preferences.dlg.fileLogLevelComboBox.currentData()
        Logger.file_log_level = index_val
        Logger.stream_log_level = index_val
        self.set_log_levels()
        PreferencesMethods.logger.warning(
            "File and terminal log level set to : " + Logger.level_lookup[index_val]
        )

    def set_log_levels(self):
        Logger.log_file_handler.setLevel(Logger.file_log_level)
        Logger.stream_handler.setLevel(Logger.stream_log_level)
        Logger.session_handler.setLevel(Logger.session_history_log_level)

    def preferences_dialog_setup(self):
        PreferencesMethods.logger.debug("preferences dialog setup")
        # set initial field text
        config_path = self.session["opt"]["input_config_file_path"]
        self.preferences.dlg.config_path_input.setText(str(config_path))
        self.preferences.dlg.config_path_input.setToolTip(str(config_path))

        for i in range(self.preferences.dlg.windowLogLevelComboBox.count()):
            self.preferences.dlg.windowLogLevelComboBox.setItemData(i, (i + 1) * 10)

        for i in range(self.preferences.dlg.fileLogLevelComboBox.count()):
            self.preferences.dlg.fileLogLevelComboBox.setItemData(i, (i + 1) * 10)

        # actions setup
        self.preferences.dlg.browse_for_config.clicked.connect(self.get_config_file)
        self.preferences.dlg.buttonBox.accepted.connect(self.save_preferences)
        self.preferences.dlg.buttonBox.rejected.connect(self.reset_preferences)
        self.preferences.dlg.windowLogLevelComboBox.currentIndexChanged.connect(
            self.set_window_log_level
        )
        self.preferences.dlg.fileLogLevelComboBox.currentIndexChanged.connect(
            self.set_file_log_level
        )
