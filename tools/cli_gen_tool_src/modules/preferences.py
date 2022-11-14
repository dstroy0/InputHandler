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
from modules.data_models import dataModels
from PySide6.QtWidgets import QFileDialog, QComboBox, QTreeWidgetItem
from PySide6.QtCore import QFile, Qt, QDir


class PreferencesMethods(object):
    dlg = ""
    builtin_methods = ""

    def __init__(self) -> None:
        super(PreferencesMethods, self).__init__()
        PreferencesMethods.logger = Logger.get_child_logger(self.logger, __name__)
        PreferencesMethods.dlg = self.preferences.dlg
        PreferencesMethods.builtin_methods = [
            key for key in dataModels.default_session_model["opt"]["builtin methods"]
        ]

    def save_preferences(self):
        config_path = PreferencesMethods.dlg.config_path_input.text()
        PreferencesMethods.logger.info("preferences set")

    def reset_preferences(self):
        config_path = self.session["opt"]["save_filename"]
        PreferencesMethods.dlg.config_path_input.setText(str(config_path))
        PreferencesMethods.logger.info("preferences dialog cancelled")

    def get_config_file(self):
        old_path = ""
        new_path = ""
        cfg_path_dlg = QFileDialog(self)
        fileName = cfg_path_dlg.getOpenFileName(
            self,
            "InputHandler config file name",
            QDir(self.session["opt"]["input_config_file_path"]).toNativeSeparators(
                self.session["opt"]["input_config_file_path"]
            ),
            "config.h",
            options=QFileDialog.DontUseNativeDialog,
        )
        if fileName[0] == "":
            PreferencesMethods.logger.info("browse for config cancelled.")
            return
        fqname = fileName[0]
        new_path = QDir(fqname).absolutePath()
        new_path = QDir(new_path).toNativeSeparators(new_path)
        old_path = QDir(self.session["opt"]["input_config_file_path"]).absolutePath()
        old_path = QDir(old_path).toNativeSeparators(old_path)
        if new_path == old_path:
            PreferencesMethods.logger.info("Same config file selected.")
            return
        self.session["opt"]["input_config_file_path"] = fqname
        PreferencesMethods.dlg.config_path_input.setText(str(fqname))
        PreferencesMethods.dlg.config_path_input.setToolTip(str(fqname))
        self.restart()

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

    def set_builtin_preference(self, x: int, state: Qt.CheckState):
        if x > len(PreferencesMethods.builtin_methods):
            PreferencesMethods.logger.warning(
                "builtin method checkbox index out of range"
            )
            return

        # this searches the tree for active builtins to exclude them from being set
        active_builtins = [
            [],
        ]
        for iterator in range(self.ui.command_tree.topLevelItemCount()):
            toplevelitem = self.ui.command_tree.topLevelItem(iterator)
            object_list = toplevelitem.data(1, 0).split(",")
            active_builtins.append(object_list)

        builtin_dict = self.cliOpt["builtin methods"]["tree"]["items"]
        cmb_container = builtin_dict[PreferencesMethods.builtin_methods[x]]["QComboBox"]

        _state = "Enabled" if state == Qt.Checked else "Disabled"

        # this sets InputHandler builtin methods to the user's preference on startup
        object_list = []
        for item in cmb_container:
            cmb = cmb_container[item]
            if isinstance(cmb, QComboBox):
                object_list = cmb.objectName().split(",")
                active_builtin = False
                for item in active_builtins:
                    if bool(item):
                        if object_list[2] == item[2]:
                            active_builtin = True

                if (
                    state == Qt.Checked
                    and active_builtin == False
                    and cmb.currentText() != _state
                    and self.cliOpt["builtin methods"]["var"][
                        PreferencesMethods.builtin_methods[x]
                    ]
                    == False
                ):
                    cmb.setCurrentIndex(cmb.findText(_state))
                    self.cliOpt["builtin methods"]["var"][
                        PreferencesMethods.builtin_methods[x]
                    ] = True
                    PreferencesMethods.logger.info(
                        "User preference: "
                        + _state
                        + " "
                        + PreferencesMethods.builtin_methods[x]
                    )
                    if self.loading != True:
                        self.session["opt"]["builtin methods"][
                            PreferencesMethods.builtin_methods[x]
                        ] = True
                elif (
                    state == Qt.Unchecked
                    and active_builtin == True
                    and cmb.currentText() != _state
                    and self.cliOpt["builtin methods"]["var"][
                        PreferencesMethods.builtin_methods[x]
                    ]
                    == True
                ):
                    self.rem_command(item)
                    cmb.setCurrentIndex(cmb.findText(_state))
                    self.cliOpt["builtin methods"]["var"][
                        PreferencesMethods.builtin_methods[x]
                    ] = False
                    PreferencesMethods.logger.info(
                        "User preference: "
                        + _state
                        + " "
                        + PreferencesMethods.builtin_methods[x]
                    )
                    if self.loading != True:
                        self.session["opt"]["builtin methods"][
                            PreferencesMethods.builtin_methods[x]
                        ] = False

                if self.loading == False:
                    PreferencesMethods.logger.info(
                        "User builtin method preference for "
                        + PreferencesMethods.builtin_methods[x]
                        + " is "
                        + _state
                    )

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
            lambda state, x=0: self.set_builtin_preference(x, state)
        )
        PreferencesMethods.dlg.defaultfunction_checkbox.stateChanged.connect(
            lambda state, x=1: self.set_builtin_preference(x, state)
        )
        PreferencesMethods.dlg.listcommands_checkbox.stateChanged.connect(
            lambda state, x=2: self.set_builtin_preference(x, state)
        )
        PreferencesMethods.dlg.listsettings_checkbox.stateChanged.connect(
            lambda state, x=3: self.set_builtin_preference(x, state)
        )

        # load session defaults
        _obj_list = [
            PreferencesMethods.dlg.outputtostream_checkbox,
            PreferencesMethods.dlg.defaultfunction_checkbox,
            PreferencesMethods.dlg.listcommands_checkbox,
            PreferencesMethods.dlg.listsettings_checkbox,
        ]
        i = 0
        for item in PreferencesMethods.builtin_methods:
            if self.session["opt"]["builtin methods"][item] == True:
                _obj_list[i].setCheckState(Qt.Checked)
                self.set_builtin_preference(i, Qt.Checked)
                i += 1
            else:
                _obj_list[i].setCheckState(Qt.Unchecked)
                self.set_builtin_preference(i, Qt.Unchecked)
                i += 1

        if int(self.cliOpt["process output"]["var"]["buffer size"]) < int(
            self.session["opt"]["output"]["buffer size"]
        ):
            PreferencesMethods.logger.info(
                "Buffer size in loaded file doesn't match user preference, changing to "
                + str(self.session["opt"]["output"]["buffer size"])
                + " bytes."
            )
            self.cliOpt["process output"]["var"]["buffer size"] = str(
                self.session["opt"]["output"]["buffer size"]
            )
            container = self.cliOpt["process output"]["tree"]["items"]["buffer size"][
                "QTreeWidgetItem"
            ]
            for item in container:
                if isinstance(container[item], QTreeWidgetItem):
                    container[item].setData(
                        3, 0, str(self.cliOpt["process output"]["var"]["buffer size"])
                    )
        if (
            self.cliOpt["process output"]["var"]["output stream"]
            != self.session["opt"]["output"]["stream"]
        ):
            PreferencesMethods.logger.info(
                "Output Stream in loaded file doesn't match user preference, changing to "
                + str(self.session["opt"]["output"]["stream"])
                + "."
            )
            self.cliOpt["process output"]["var"]["output stream"] = str(
                self.session["opt"]["output"]["stream"]
            )
            container = self.cliOpt["process output"]["tree"]["items"]["output stream"][
                "QTreeWidgetItem"
            ]
            for item in container:
                if isinstance(container[item], QTreeWidgetItem):
                    container[item].setData(
                        3, 0, str(self.cliOpt["process output"]["var"]["output stream"])
                    )
        PreferencesMethods.logger.info("User preferences set.")

# end of file
