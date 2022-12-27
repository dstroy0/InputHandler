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
import os
import sys
from modules.logging_setup import Logger
from modules.data_models import dataModels
from PySide6.QtWidgets import (
    QFileDialog,
    QLineEdit,
    QDialogButtonBox,
    QDialog,
    QWidget,
    QStyle,
)
from PySide6.QtCore import Qt, QDir, QRegularExpression
from PySide6.QtGui import QIcon


class PreferencesMethods(object):
    def __init__(self) -> None:
        super(PreferencesMethods, self).__init__()
        PreferencesMethods.logger = self.get_child_logger(__name__)
        self._parent = self
        self.create_qdialog = self._parent.create_qdialog
        self.cliopt = self._parent.cliOpt
        self.dlg = self.preferences.dlg

        self.builtin_methods = [
            key for key in dataModels.default_session_model["opt"]["builtin methods"]
        ]

        self.builtin_cmb_dict = {}

    def get_comboboxes(self):
        for i in range(len(self.builtin_methods)):
            items = self.settings_tree.findItems(
                self.builtin_methods[i],
                Qt.MatchExactly | Qt.MatchWrap | Qt.MatchRecursive,
                1,
            )
            item = items[0]
            cmb = self.settings_tree.itemWidget(item, 3)
            self.builtin_cmb_dict.update(
                {self.builtin_methods[i]: {"cmb": cmb, "item": item}}
            )

    def save_preferences(self):
        config_path = self.dlg.config_path_input.text()
        PreferencesMethods.logger.info("preferences set")

    def reset_preferences(self):
        config_path = self.session["opt"]["save_filename"]
        self.dlg.config_path_input.setText(str(config_path))
        PreferencesMethods.logger.info("preferences dialog cancelled")

    def set_session_history_log_level(self, index):
        index_val = self.dlg.sessionHistoryLogLevelComboBox.currentData()
        Logger.session_history_log_level = index_val
        Logger.set_log_levels(self)
        self.logger.warning(
            "Session history log level set to : " + Logger.level_lookup[index_val]
        )

    def set_file_log_level(self, index):
        index_val = self.dlg.fileLogLevelComboBox.currentData()
        Logger.file_log_level = index_val
        Logger.set_log_levels(self)
        self.logger.warning("File log level set to : " + Logger.level_lookup[index_val])

    def set_stream_log_level(self, index):
        index_val = self.dlg.streamLogLevelComboBox.currentData()
        Logger.stream_log_level = index_val
        Logger.set_log_levels(self)
        self.logger.warning(
            "Stream log level set to : " + Logger.level_lookup[index_val]
        )

    def set_global_log_level(self, index):
        index_val = self.dlg.globalLogLevelComboBox.currentData()
        Logger.file_log_level = index_val
        Logger.set_log_levels(self)
        self.logger.warning(
            "Global log level set to : " + Logger.level_lookup[index_val]
        )

    # TODO
    def output_preferences(self):
        stream = self.dlg.default_stream.text()
        size = self.dlg.default_output_buffer_size.text()

    def set_builtin_preference(self, x: int, state: Qt.CheckState):
        if x > len(self.builtin_methods):
            PreferencesMethods.logger.warning(
                "builtin method checkbox index out of range"
            )
            return
        cmb = self.builtin_cmb_dict[self.builtin_methods[x]]["cmb"]
        item = self.builtin_cmb_dict[self.builtin_methods[x]]["item"]
        self.active_builtins = []
        for builtin in self.builtin_cmb_dict:
            if str(self.builtin_cmb_dict[builtin]["cmb"].currentText()) == "Enabled":
                self.active_builtins.append(builtin)

        _state = "Enabled" if state == Qt.Checked else "Disabled"

        # this sets InputHandler builtin methods to the user's preference on startup
        if self.loading == False:
            PreferencesMethods.logger.info(
                "User builtin method preference for "
                + self.builtin_methods[x]
                + " is "
                + _state
            )
            if state == Qt.Checked:
                self.session["opt"]["builtin methods"][self.builtin_methods[x]] = True
            elif state == Qt.Unchecked:
                self.session["opt"]["builtin methods"][self.builtin_methods[x]] = False
        else:
            PreferencesMethods.logger.info(
                "Loaded user preference: " + self.builtin_methods[x] + " " + _state
            )

        if self.builtin_methods[x] in self.active_builtins and state == Qt.Unchecked:
            if str(cmb.currentText()) != "Disabled":
                self.settings_tree.setCurrentItem(item)
                cmb.setCurrentIndex(cmb.findText("Disabled"))
                self.cliOpt["builtin methods"]["var"][self.builtin_methods[x]] = False
        elif (
            self.builtin_methods[x] not in self.active_builtins and state == Qt.Checked
        ):
            if str(cmb.currentText()) != "Enabled":
                self.settings_tree.setCurrentItem(item)
                cmb.setCurrentIndex(cmb.findText("Enabled"))
                self.cliOpt["builtin methods"]["var"][self.builtin_methods[x]] = True

    def set_line_edit_text(self, le: QLineEdit):
        qdir = QDir()
        dir = qdir.toNativeSeparators(le.text())
        has_file = False
        sep = qdir.separator()
        regexp_str = "(\S*\\" + sep + ")(.*)"
        regexp = QRegularExpression(regexp_str)

        dir_component_list = []
        str_pos = 0

        result = regexp.match(dir, str_pos)
        if result.hasMatch():
            dir_component_list.append(result.captured(1))
            dir_component_list.append(result.captured(2))

        if le.objectName() == "output_path_input":
            if len(dir_component_list) == 0:
                b = QDialogButtonBox.StandardButton
                buttons = [b.Open, b.Ok, b.Cancel]
                button_text = ["Select output path","Ok", "Cancel"]
                result = self.create_qdialog(                    
                    "An output path must be selected to generate files.",
                    Qt.AlignCenter,
                    Qt.NoTextInteraction,
                    "Remember to set an output path before attempting file generation!",
                    buttons,
                    button_text,
                    QIcon(
                        QWidget()
                        .style()
                        .standardIcon(QStyle.StandardPixmap.SP_MessageBoxWarning)
                    ),
                    self._parent.qscreen,
                )
                if result == QDialog.Accepted:
                    le.clear()
                    le.setPlaceholderText("Not set...")
                    return None
                elif result == 3:
                    le.clear()
                    le.setText(self.cliopt)
                    return None
                elif result == 4:
                    le.clear()
                    le.setText(self._parent.get_project_dir())            
            else:
                if os.path.exists(dir):
                    le.clear()
                    le.setText(dir)
                    self.cliopt["session"]["opt"]["output_dir"]                

        if le.objectName() == "config_path_input":
            if len(dir_component_list) == 2:
                if self._parent.old_path.strip() == dir.strip():
                    PreferencesMethods.logger.info("same config path entered")
                    le.setText(self._parent.old_path)
                    return
                elif os.path.exists(dir):
                    self._parent.get_config_file(dir)
                else:
                    PreferencesMethods.logger.info(
                        "Invalid path entered, trying to get new config file."
                    )
                    self._parent.get_config_file()
            else:
                self._parent.get_config_file()

        # le.setToolTip(le.text())

    def preferences_dialog_setup(self):
        pref_dlg = self.preferences.dlg
        pref_dlg.validatorDict = {
            "default stream": "^([a-zA-Z0-9_*])+$",
            "default output buffer size": "^([0-9_*])+$",
        }
        PreferencesMethods.logger.debug("preferences dialog setup")
        self.get_comboboxes()
        # set initial field text
        config_path = self.session["opt"]["input_config_file_path"]
        self.dlg.config_path_input.setText(str(config_path))
        self.dlg.config_path_input.setToolTip(str(config_path))
        project_path = self.session["opt"]["output_dir"]
        self.dlg.output_path_input.setText(str(project_path))
        self.dlg.output_path_input.setToolTip(str(project_path))

        # set preferences log level combobox values to logging library log level values
        for i in range(self.dlg.sessionHistoryLogLevelComboBox.count()):
            self.dlg.sessionHistoryLogLevelComboBox.setItemData(i, (i + 1) * 10)
        for i in range(self.dlg.fileLogLevelComboBox.count()):
            self.dlg.fileLogLevelComboBox.setItemData(i, (i + 1) * 10)
        for i in range(self.dlg.streamLogLevelComboBox.count()):
            self.dlg.streamLogLevelComboBox.setItemData(i, (i + 1) * 10)
        for i in range(self.dlg.globalLogLevelComboBox.count()):
            self.dlg.globalLogLevelComboBox.setItemData(i, (i + 1) * 10)

        # initial combobox index
        cmb = self.dlg.sessionHistoryLogLevelComboBox
        log_level = Logger.session_history_log_level
        cmb.setCurrentIndex(cmb.findText(Logger.level_lookup[log_level]))
        cmb = self.dlg.fileLogLevelComboBox
        log_level = Logger.file_log_level
        cmb.setCurrentIndex(cmb.findText(Logger.level_lookup[log_level]))
        cmb = self.dlg.streamLogLevelComboBox
        log_level = Logger.stream_log_level
        cmb.setCurrentIndex(cmb.findText(Logger.level_lookup[log_level]))
        cmb = self.dlg.globalLogLevelComboBox
        log_level = Logger.root_log_level
        cmb.setCurrentIndex(cmb.findText(Logger.level_lookup[log_level]))

        self.dlg.config_path_input.editingFinished.connect(
            lambda le=self.dlg.config_path_input: self.set_line_edit_text(le)
        )
        # self.dlg.config_path_input.textEdited.connect(
        #     lambda text, le=self.dlg.config_path_input: self.set_line_edit_text(text, le)
        # )
        self.dlg.output_path_input.editingFinished.connect(
            lambda le=self.dlg.output_path_input: self.set_line_edit_text(le)
        )
        # self.dlg.output_path_input.textEdited.connect(
        #     lambda text, le=self.dlg.output_path_input: self.set_line_edit_text(text, le)
        # )

        # input validation
        self.dlg.default_stream.setValidator(
            self.regex_validator(self.dlg.validatorDict["default stream"])
        )
        self.dlg.default_output_buffer_size.setValidator(
            self.regex_validator(self.dlg.validatorDict["default output buffer size"])
        )

        # actions setup
        self.dlg.browse_for_config.clicked.connect(self._parent.get_config_file)
        self.dlg.browse_for_output_dir.clicked.connect(self._parent.get_project_dir)
        self.dlg.buttonBox.accepted.connect(self.save_preferences)
        self.dlg.buttonBox.rejected.connect(self.reset_preferences)
        self.dlg.sessionHistoryLogLevelComboBox.currentIndexChanged.connect(
            self.set_session_history_log_level
        )
        self.dlg.fileLogLevelComboBox.currentIndexChanged.connect(
            self.set_file_log_level
        )
        self.dlg.streamLogLevelComboBox.currentIndexChanged.connect(
            self.set_stream_log_level
        )
        self.dlg.globalLogLevelComboBox.currentIndexChanged.connect(
            self.set_global_log_level
        )
        self.dlg.default_stream.editingFinished.connect(self.output_preferences)
        self.dlg.default_output_buffer_size.editingFinished.connect(
            self.output_preferences
        )
        self.dlg.outputtostream_checkbox.stateChanged.connect(
            lambda state, x=0: self.set_builtin_preference(x, state)
        )
        self.dlg.defaultfunction_checkbox.stateChanged.connect(
            lambda state, x=1: self.set_builtin_preference(x, state)
        )
        self.dlg.listcommands_checkbox.stateChanged.connect(
            lambda state, x=2: self.set_builtin_preference(x, state)
        )
        self.dlg.listsettings_checkbox.stateChanged.connect(
            lambda state, x=3: self.set_builtin_preference(x, state)
        )

        # load session defaults
        _obj_list = [
            self.dlg.outputtostream_checkbox,
            self.dlg.defaultfunction_checkbox,
            self.dlg.listcommands_checkbox,
            self.dlg.listsettings_checkbox,
        ]
        i = 0
        for item in self.builtin_methods:
            if self.session["opt"]["builtin methods"][item] == True:
                _obj_list[i].setCheckState(Qt.Checked)
                i += 1
            else:
                _obj_list[i].setCheckState(Qt.Unchecked)
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
            items = self.settings_tree.findItems(
                "buffer size", Qt.MatchExactly | Qt.MatchWrap | Qt.MatchRecursive, 1
            )
            item = items[0]
            item.setData(3, 0, str(self.cliOpt["process output"]["var"]["buffer size"]))
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
            items = self.settings_tree.findItems(
                "output stream", Qt.MatchExactly | Qt.MatchWrap | Qt.MatchRecursive, 1
            )
            item = items[0]
            item.setData(
                3, 0, str(self.cliOpt["process output"]["var"]["output stream"])
            )
        PreferencesMethods.logger.info("User preferences set.")


# end of file
