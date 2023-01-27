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
from PySide6.QtWidgets import QLineEdit
from PySide6.QtCore import Qt, QEvent, Signal, QObject


class PreferencesMethods(object):
    """preferences dialog methods

    Args:
        object (object): base object specialization
    """

    def __init__(self) -> None:
        """the constructor"""
        super(PreferencesMethods, self).__init__()
        PreferencesMethods.logger = self.get_child_logger(__name__)
        self._parent = self
        self.create_qdialog = self._parent.create_qdialog
        self.cliopt = self._parent.cliOpt
        self.session = self._parent.session
        self.dlg = self.preferences.dlg

        self.builtin_methods = [
            key for key in dataModels.default_session_model["opt"]["builtin methods"]
        ]

        self.builtin_cmb_dict = {}

    def get_comboboxes(self):
        """get builtin method comboboxes"""
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

    # TODO
    def save_preferences(self):
        """save user preferences"""
        config_path = self.dlg.config_path_input.text()
        PreferencesMethods.logger.info("preferences set")
        self.preferences.close()

    # TODO
    def reset_preferences(self):
        """reset preferences to what they were before interaction"""
        config_path = self.session["opt"]["save_filename"]
        self.dlg.config_path_input.setText(str(config_path))
        PreferencesMethods.logger.info("preferences dialog cancelled")
        self.preferences.close()

    def set_session_log_level(self, index):
        """sets session history log level

        Args:
            index (int): combobox index
        """
        index_val = self.dlg.logLevelComboBox.currentData()
        Logger.session_log_level = index_val
        Logger.set_log_levels(self)
        self.logger.warning(
            "Session log level set to : " + Logger.level_lookup[index_val]
        )

    # TODO
    def output_preferences(self):
        """set output preferences"""
        stream = self.dlg.default_stream.text()
        size = self.dlg.default_output_buffer_size.text()

    def set_builtin_preference(self, x: int, state: Qt.CheckState):
        """set builtin preferences

        Args:
            x (int): combobox index lambda
            state (Qt.CheckState): bool
        """
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
        """sets line edit text

        Args:
            le (QLineEdit): line edit interacted with
        """
        text = ""
        if le.objectName() == "output_path_input":
            text = self._parent.get_project_dir()
            if text:
                le.setText(text)
        if le.objectName() == "config_path_input":
            text = self._parent.get_config_file()

        le.setText(text)
        le.setToolTip(text)

    def clickable(self, widget):
        """makes objects emit "clicked"

        Args:
            widget (QWidget): the widget to attach the signal to

        Returns:
            Filter (QObject): the filtered object interaction
        """

        class Filter(QObject):
            clicked = Signal()

            def eventFilter(self, obj, event):
                if (
                    obj == widget
                    and event.type() == QEvent.MouseButtonRelease
                    and obj.rect().contains(event.pos())
                ):
                    self.clicked.emit()
                    return True
                else:
                    return False

        filter = Filter(widget)
        widget.installEventFilter(filter)
        return filter.clicked

    def preferences_dialog_setup(self):
        """sets up preferences dialog"""
        pref_dlg = self.preferences.dlg
        pref_dlg.validatorDict = {
            "default stream": "^([a-zA-Z0-9_*])+$",
            "default output buffer size": "^([0-9_*])+$",
        }
        PreferencesMethods.logger.debug("preferences dialog setup")
        self.get_comboboxes()
        # set initial field text
        config_path = self.session["opt"]["inputhandler_config_file_path"]
        self.dlg.config_path_input.setText(str(config_path))
        self.dlg.config_path_input.setToolTip(str(config_path))
        project_path = self.session["opt"]["cli_output_dir"]
        self.dlg.output_path_input.setText(str(project_path))
        self.dlg.output_path_input.setToolTip(str(project_path))

        # set preferences log level combobox values to logging library log level values
        for i in range(self.dlg.logLevelComboBox.count()):
            self.dlg.logLevelComboBox.setItemData(i, (i + 1) * 10)

        # initial combobox index
        cmb = self.dlg.logLevelComboBox
        log_level = Logger.session_log_level
        cmb.setCurrentIndex(cmb.findText(Logger.level_lookup[log_level]))

        self.clickable(self.dlg.output_path_input).connect(
            lambda le=self.dlg.output_path_input: self.set_line_edit_text(le)
        )
        self.clickable(self.dlg.config_path_input).connect(
            lambda le=self.dlg.config_path_input: self.set_line_edit_text(le)
        )

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
        self.dlg.ok.clicked.connect(self.save_preferences)
        self.dlg.cancel.clicked.connect(self.reset_preferences)
        self.dlg.logLevelComboBox.currentIndexChanged.connect(
            self.set_session_log_level
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
