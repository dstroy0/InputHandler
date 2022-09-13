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
from PySide6.QtCore import QFile


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

    def set_session_history_log_level(self, index):
        index_val = self.preferences.dlg.sessionHistoryLogLevelComboBox.currentData()
        Logger.session_history_log_level = index_val
        self.set_log_levels()
        self.logger.warning(
            "Session history log level set to : " + Logger.level_lookup[index_val]
        )

    def set_file_log_level(self, index):
        index_val = self.preferences.dlg.fileLogLevelComboBox.currentData()
        Logger.file_log_level = index_val
        self.set_log_levels()
        self.logger.warning("File log level set to : " + Logger.level_lookup[index_val])

    def set_stream_log_level(self, index):
        index_val = self.preferences.dlg.streamLogLevelComboBox.currentData()
        Logger.stream_log_level = index_val
        self.set_log_levels()
        self.logger.warning(
            "Stream log level set to : " + Logger.level_lookup[index_val]
        )

    def set_global_log_level(self, index):
        index_val = self.preferences.dlg.globalLogLevelComboBox.currentData()
        Logger.file_log_level = index_val
        self.set_log_levels()
        self.logger.warning(
            "Global log level set to : " + Logger.level_lookup[index_val]
        )

    def set_log_levels(self):
        Logger.root_log_handler.setLevel(Logger.root_log_level)
        Logger.file_log_handler.setLevel(Logger.file_log_level)
        Logger.stream_log_handler.setLevel(Logger.stream_log_level)
        Logger.session_log_handler.setLevel(Logger.session_history_log_level)

    def preferences_dialog_setup(self):
        PreferencesMethods.logger.debug("preferences dialog setup")
        # set initial field text
        config_path = self.session["opt"]["input_config_file_path"]
        self.preferences.dlg.config_path_input.setText(str(config_path))
        self.preferences.dlg.config_path_input.setToolTip(str(config_path))

        for i in range(self.preferences.dlg.sessionHistoryLogLevelComboBox.count()):
            self.preferences.dlg.sessionHistoryLogLevelComboBox.setItemData(
                i, (i + 1) * 10
            )

        for i in range(self.preferences.dlg.fileLogLevelComboBox.count()):
            self.preferences.dlg.fileLogLevelComboBox.setItemData(i, (i + 1) * 10)

        for i in range(self.preferences.dlg.streamLogLevelComboBox.count()):
            self.preferences.dlg.streamLogLevelComboBox.setItemData(i, (i + 1) * 10)

        for i in range(self.preferences.dlg.globalLogLevelComboBox.count()):
            self.preferences.dlg.globalLogLevelComboBox.setItemData(i, (i + 1) * 10)

        # initial index
        cmb = self.preferences.dlg.sessionHistoryLogLevelComboBox
        log_level = Logger.session_history_log_level
        cmb.setCurrentIndex(cmb.findText(Logger.level_lookup[log_level]))
        cmb = self.preferences.dlg.fileLogLevelComboBox
        log_level = Logger.file_log_level
        cmb.setCurrentIndex(cmb.findText(Logger.level_lookup[log_level]))
        cmb = self.preferences.dlg.streamLogLevelComboBox
        log_level = Logger.stream_log_level
        cmb.setCurrentIndex(cmb.findText(Logger.level_lookup[log_level]))
        cmb = self.preferences.dlg.globalLogLevelComboBox
        log_level = Logger.root_log_level
        cmb.setCurrentIndex(cmb.findText(Logger.level_lookup[log_level]))
        
        # actions setup
        self.preferences.dlg.browse_for_config.clicked.connect(self.get_config_file)
        self.preferences.dlg.buttonBox.accepted.connect(self.save_preferences)
        self.preferences.dlg.buttonBox.rejected.connect(self.reset_preferences)
        self.preferences.dlg.sessionHistoryLogLevelComboBox.currentIndexChanged.connect(
            self.set_session_history_log_level
        )
        self.preferences.dlg.fileLogLevelComboBox.currentIndexChanged.connect(
            self.set_file_log_level
        )
        self.preferences.dlg.streamLogLevelComboBox.currentIndexChanged.connect(
            self.set_stream_log_level
        )
        self.preferences.dlg.globalLogLevelComboBox.currentIndexChanged.connect(
            self.set_global_log_level
        )
