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
from modules.logging_setup import Logger
from PySide6.QtWidgets import QFileDialog, QComboBox
from PySide6.QtCore import QFile, Qt


class PreferencesMethods(object):
    dlg = ""

    def __init__(self) -> None:
        super(PreferencesMethods, self).__init__()
        PreferencesMethods.logger = Logger.get_child_logger(self.logger, __name__)
        PreferencesMethods.dlg = self.preferences.dlg

    def save_preferences(self):
        config_path = PreferencesMethods.dlg.config_path_input.text()
        PreferencesMethods.logger.info("preferences set")

    def reset_preferences(self):
        config_path = self.session["opt"]["input_config_file_path"]
        PreferencesMethods.dlg.config_path_input.setText(str(config_path))
        PreferencesMethods.logger.info(
            "preferences dialog cancelled, config path reset to: " + str(config_path)
        )

    def get_config_file(self):
        cfg_path_dlg = QFileDialog(self)
        fileName = cfg_path_dlg.getOpenFileName(
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
        PreferencesMethods.dlg.config_path_input.setText(str(fqname))
        PreferencesMethods.dlg.config_path_input.setToolTip(str(fqname))
        self.app.restart()

    def set_session_history_log_level(self, index):
        index_val = PreferencesMethods.dlg.sessionHistoryLogLevelComboBox.currentData()
        Logger.session_history_log_level = index_val
        Logger.set_log_levels()
        self.logger.warning(
            "Session history log level set to : " + Logger.level_lookup[index_val]
        )

    def set_file_log_level(self, index):
        index_val = PreferencesMethods.dlg.fileLogLevelComboBox.currentData()
        Logger.file_log_level = index_val
        Logger.set_log_levels()
        self.logger.warning("File log level set to : " + Logger.level_lookup[index_val])

    def set_stream_log_level(self, index):
        index_val = PreferencesMethods.dlg.streamLogLevelComboBox.currentData()
        Logger.stream_log_level = index_val
        Logger.set_log_levels()
        self.logger.warning(
            "Stream log level set to : " + Logger.level_lookup[index_val]
        )

    def set_global_log_level(self, index):
        index_val = PreferencesMethods.dlg.globalLogLevelComboBox.currentData()
        Logger.file_log_level = index_val
        Logger.set_log_levels()
        self.logger.warning(
            "Global log level set to : " + Logger.level_lookup[index_val]
        )

    # TODO
    def output_preferences(self):
        stream = PreferencesMethods.dlg.default_stream.text()
        size = PreferencesMethods.dlg.default_output_buffer_size.text()

    def builtin_methods_preferences(self, x: int, state: int) -> None:
        methods = ["outputToStream", "defaultFunction", "listCommands", "listSettings"]
        builtin_dict = self.cliOpt["builtin methods"]["tree"]["items"]

        def set_builtins(dict):
            for item in dict:
                cmb = dict[item]
                if isinstance(cmb, QComboBox):
                    if state == Qt.Checked:
                        cmb.setCurrentIndex(cmb.findText("Enabled"))
                        self.session["opt"]["builtin methods"][methods[x]] = True
                    else:
                        cmb.setCurrentIndex(cmb.findText("Disabled"))
                        self.session["opt"]["builtin methods"][methods[x]] = False

        set_builtins(builtin_dict[methods[x]]["QComboBox"])

    def preferences_dialog_setup(self):
        PreferencesMethods.logger.debug("preferences dialog setup")
        # set initial field text
        config_path = self.session["opt"]["input_config_file_path"]
        PreferencesMethods.dlg.config_path_input.setText(str(config_path))
        PreferencesMethods.dlg.config_path_input.setToolTip(str(config_path))

        # set preferences log level combobox values to logging library log level values
        for i in range(PreferencesMethods.dlg.sessionHistoryLogLevelComboBox.count()):
            PreferencesMethods.dlg.sessionHistoryLogLevelComboBox.setItemData(
                i, (i + 1) * 10
            )
        for i in range(PreferencesMethods.dlg.fileLogLevelComboBox.count()):
            PreferencesMethods.dlg.fileLogLevelComboBox.setItemData(i, (i + 1) * 10)
        for i in range(PreferencesMethods.dlg.streamLogLevelComboBox.count()):
            PreferencesMethods.dlg.streamLogLevelComboBox.setItemData(i, (i + 1) * 10)
        for i in range(PreferencesMethods.dlg.globalLogLevelComboBox.count()):
            PreferencesMethods.dlg.globalLogLevelComboBox.setItemData(i, (i + 1) * 10)

        # initial combobox index
        cmb = PreferencesMethods.dlg.sessionHistoryLogLevelComboBox
        log_level = Logger.session_history_log_level
        cmb.setCurrentIndex(cmb.findText(Logger.level_lookup[log_level]))
        cmb = PreferencesMethods.dlg.fileLogLevelComboBox
        log_level = Logger.file_log_level
        cmb.setCurrentIndex(cmb.findText(Logger.level_lookup[log_level]))
        cmb = PreferencesMethods.dlg.streamLogLevelComboBox
        log_level = Logger.stream_log_level
        cmb.setCurrentIndex(cmb.findText(Logger.level_lookup[log_level]))
        cmb = PreferencesMethods.dlg.globalLogLevelComboBox
        log_level = Logger.root_log_level
        cmb.setCurrentIndex(cmb.findText(Logger.level_lookup[log_level]))

        # input validation
        PreferencesMethods.dlg.default_stream.setValidator(
            self.regex_validator("^([a-zA-Z0-9_*])+$")
        )
        PreferencesMethods.dlg.default_output_buffer_size.setValidator(
            self.regex_validator("^([0-9_*])+$")
        )

        # load session defaults
        if self.session["opt"]["builtin methods"]["defaultFunction"] == True:
            PreferencesMethods.dlg.defaultfunction_checkbox.setCheckState(Qt.Checked)
        else:
            PreferencesMethods.dlg.defaultfunction_checkbox.setCheckState(Qt.Unchecked)
        if self.session["opt"]["builtin methods"]["outputToStream"] == True:
            PreferencesMethods.dlg.outputtostream_checkbox.setCheckState(Qt.Checked)
        else:
            PreferencesMethods.dlg.outputtostream_checkbox.setCheckState(Qt.Unchecked)
        if self.session["opt"]["builtin methods"]["listCommands"] == True:
            PreferencesMethods.dlg.listcommands_checkbox.setCheckState(Qt.Checked)
        else:
            PreferencesMethods.dlg.listcommands_checkbox.setCheckState(Qt.Unchecked)
        if self.session["opt"]["builtin methods"]["listSettings"] == True:
            PreferencesMethods.dlg.listsettings_checkbox.setCheckState(Qt.Checked)
        else:
            PreferencesMethods.dlg.listsettings_checkbox.setCheckState(Qt.Unchecked)

        # actions setup
        PreferencesMethods.dlg.browse_for_config.clicked.connect(self.get_config_file)
        PreferencesMethods.dlg.buttonBox.accepted.connect(self.save_preferences)
        PreferencesMethods.dlg.buttonBox.rejected.connect(self.reset_preferences)
        PreferencesMethods.dlg.sessionHistoryLogLevelComboBox.currentIndexChanged.connect(
            self.set_session_history_log_level
        )
        PreferencesMethods.dlg.fileLogLevelComboBox.currentIndexChanged.connect(
            self.set_file_log_level
        )
        PreferencesMethods.dlg.streamLogLevelComboBox.currentIndexChanged.connect(
            self.set_stream_log_level
        )
        PreferencesMethods.dlg.globalLogLevelComboBox.currentIndexChanged.connect(
            self.set_global_log_level
        )
        PreferencesMethods.dlg.default_stream.editingFinished.connect(
            self.output_preferences
        )
        PreferencesMethods.dlg.default_output_buffer_size.editingFinished.connect(
            self.output_preferences
        )
        PreferencesMethods.dlg.outputtostream_checkbox.stateChanged.connect(
            lambda state, x=0: self.builtin_methods_preferences(x, state)
        )
        PreferencesMethods.dlg.defaultfunction_checkbox.stateChanged.connect(
            lambda state, x=1: self.builtin_methods_preferences(x, state)
        )
        PreferencesMethods.dlg.listcommands_checkbox.stateChanged.connect(
            lambda state, x=2: self.builtin_methods_preferences(x, state)
        )
        PreferencesMethods.dlg.listsettings_checkbox.stateChanged.connect(
            lambda state, x=3: self.builtin_methods_preferences(x, state)
        )


# end of file
