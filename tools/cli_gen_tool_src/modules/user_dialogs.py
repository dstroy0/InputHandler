##
# @file user_dialogs.py
# @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
# @brief InputHandler CLI generation tool user dialogs
# @version 1.0.0
# @date 2023-05-22
# @copyright Copyright (c) 2023
# Copyright (C) 2023 Douglas Quigg (dstroy0) <dquigg123@gmail.com>
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 3 as published by the Free Software Foundation.

from __future__ import absolute_import
import os
import sys
import json
from PySide6.QtWidgets import (
    QDialog,
    QFileDialog,
    QDialogButtonBox,
    QStyle,
    QWidget,
    QVBoxLayout,
    QLabel,
    QSizePolicy,
)
from PySide6.QtCore import Qt, QFile, QDir, QRegularExpression
from PySide6.QtGui import QIcon
from modules.data_models import DataModels


class UserDialogs(object):
    def __init__(self) -> None:
        super(UserDialogs, self).__init__()

    def setup_logging(self):
        UserDialogs.logger = self.get_child_logger(__name__)

    ## spawn a dialog box
    def create_qdialog(
        self,
        message,
        message_text_alignment,
        message_text_interaction_flags,
        window_title=None,
        buttons=None,
        button_text=None,
        icon: QStyle.StandardPixmap = None,
        screen=None,
    ):
        """creates a QDialog

        Args:
            message (str): message content
            message_text_alignment (Qt): message alignment flags
            message_text_interaction_flags (Qt): text interaction flags
            window_title (str, optional): window title. Defaults to None.
            buttons (list, optional): list of QDialogButtonBox button types. Defaults to None.
            button_text (list, optional): lsit of button texts. Defaults to None.
            icon (QIcon, optional): window icon. Defaults to None.
            screen (QScreen, optional): screen to display QDialog on. Defaults to None.

        Returns:
            exitcode: QDialog exit code
        """
        _buttons = []

        if not isinstance(self, QWidget):
            self = self.root

        dlg = QDialog(self)

        def button_box_clicked(button):
            _match = 0
            for i in range(len(_buttons)):
                if button == _buttons[i]:
                    _match = i
                    break
            b = QDialogButtonBox.StandardButton
            if buttons[_match] == b.Ok:
                dlg.accept()
            if buttons[_match] == b.Cancel:
                dlg.reject()
            if buttons[_match] == b.Save:
                dlg.done(2)
            if buttons[_match] == b.Close:
                dlg.done(3)
            if buttons[_match] == b.Open:
                dlg.done(4)

        # create popup
        dlg.layout = QVBoxLayout()
        dlg.label = QLabel()
        dlg.label.setMinimumSize(0, 15)
        dlg.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        dlg.label.setTextFormat(Qt.AutoText)
        dlg.label.setText(message)
        dlg.label.setAlignment(message_text_alignment)

        if type(message_text_interaction_flags) == Qt.TextInteractionFlag:
            dlg.label.setTextInteractionFlags(message_text_interaction_flags)
        elif type(message_text_interaction_flags) == Qt.TextInteractionFlags:
            dlg.label.setTextInteractionFlags(message_text_interaction_flags)
        dlg.label.setOpenExternalLinks(True)
        dlg.layout.addWidget(dlg.label)

        if buttons != None:
            dlg.button_box = QDialogButtonBox(dlg)
            idx = 0
            for item in buttons:
                _button = dlg.button_box.addButton(item)
                if button_text[idx] != "":
                    _button.setText(button_text[idx])
                _buttons.append(_button)
                idx += 1
            dlg.button_box.clicked.connect(button_box_clicked)
            dlg.button_box.setCenterButtons(True)
            dlg.layout.addWidget(dlg.button_box)
        dlg.setLayout(dlg.layout)
        if icon != None:
            dlg.setWindowIcon(QIcon(QWidget().style().standardIcon(icon)))
        if window_title != None:
            dlg.setWindowTitle(window_title)
        dlg.setWindowFlags(dlg.windowFlags() | Qt.WindowStaysOnTopHint)

        dlg.activateWindow()  # brings focus to the popup

        # center dialog on screen
        if screen == None:
            _qscreen = self.app.primaryScreen()
        else:
            _qscreen = screen

        _fg = dlg.frameGeometry()
        center_point = _qscreen.availableGeometry().center()
        center_point.setX(center_point.x() - (_fg.x() / 2))
        center_point.setY(center_point.y() - (_fg.y() / 2))
        _fg.moveCenter(center_point)
        info = ""
        if bool(self.objectName()):
            info = self.objectName()
        else:
            info = str(self)
        self.logger.info(f"{info} creating QDialog on: {_qscreen.name()}")
        ret = dlg.exec()  # return the dialog exit code
        return ret

    # TODO fix icon
    def create_file_error_qdialog(self, error_type: str, qfile: QFile):
        """creates an error dialog

        Args:
            error_type (str): error description
            qfile (QFile): file information
        """
        UserDialogs.logger.warning(f"{error_type} {qfile.fileName()} error.")
        self.create_qdialog(
            error_type,
            Qt.AlignCenter,
            0,
            str(f"{error_type} {qfile.fileName()} error."),
            None,
            None,
            self.ui.messageBoxCriticalIcon,
        )

    def get_project_dir(self) -> str:
        """get valid os path to project

        Returns:
            str: valid os path or None
        """
        open_on_dir = ""
        output_dir = self.session["opt"]["cli_output_dir"]
        if output_dir == None:
            output_dir = self._parent.lib_root_path
        if os.path.exists(output_dir):
            open_on_dir = output_dir
        else:
            open_on_dir = QDir.homePath()
        dir_dlg = QFileDialog(self)
        _dlg_result = dir_dlg.getExistingDirectory(
            self,
            "Select output directory",
            open_on_dir,
            options=QFileDialog.DontUseNativeDialog
            | QFileDialog.ShowDirsOnly
            | QFileDialog.DontResolveSymlinks,
        )
        if _dlg_result == QFileDialog.Rejected:
            b = QDialogButtonBox.StandardButton
            buttons = [b.Ok, b.Close]
            button_text = ["Select output directory", "Cancel"]
            result = self.create_qdialog(
                self._parent,
                "You must select an output directory to generate files.",
                Qt.AlignCenter,
                Qt.NoTextInteraction,
                "Error, no output directory selected!",
                buttons,
                button_text,
                QStyle.StandardPixmap.SP_MessageBoxCritical,
                self._parent.qscreen,
            )
            if result == 3:
                return None

        _dir = QDir(_dlg_result)
        _result = _dir.toNativeSeparators(_dir.absolutePath())
        if os.path.exists(_result):
            UserDialogs.logger.info(f"valid directory selected:\n{str(_result)}")
            return _result
        else:
            UserDialogs.logger.info("invalid directory selected")
            return None

    def open_file(self, checked: bool = False, path: str = "") -> int:
        """opens a cli options file and does simple validity check

        Args:
            checked (bool, optional): action checked bool. Defaults to False.
            path (str, optional): absolute file path. Defaults to "".

        Returns:
            int: size if greater than zero, error code if zero or less.
        """
        if not os.path.exists(path):
            UserDialogs.logger.info("open CLI settings file dialog")
            # inherit from parent QMainWindow (block main window interaction while dialog box is open)
            dlg = QFileDialog(self)
            dlg.setFileMode(QFileDialog.ExistingFile)
            dlg.setNameFilter("Settings json (*.json)")
            dlg.setViewMode(QFileDialog.Detail)
            fileName = dlg.getOpenFileName(options=QFileDialog.DontUseNativeDialog)
            if dlg.Accepted:
                path = fileName[0]
            else:
                UserDialogs.logger.info("dialog cancelled")
                return 0  # dialog cancelled

        if path == "" or not os.path.exists(path):
            UserDialogs.logger.info("CLI settings file path error")
            return -1  # path error

        file = QFile(path)
        read_json_result = self.read_json(file)

        if read_json_result[0] >= 0 and read_json_result[1]["type"] == "cli options":
            if self._parent.prompt_to_save == True:
                regexp = QRegularExpression("[^\/]*$")
                match = regexp.match(path)
                if match.hasMatch():
                    filename = str(match.captured(0))
                b = QDialogButtonBox.StandardButton
                buttons = [b.Ok, b.Close]
                button_text = ["Save", "Cancel"]
                result = self.create_qdialog(
                    self._parent,
                    "Do you want to save your current work?",
                    Qt.AlignCenter,
                    Qt.NoTextInteraction,
                    f"Save before opening {filename}",
                    buttons,
                    button_text,
                    QStyle.StandardPixmap.SP_MessageBoxCritical,
                    self._parent.qscreen,
                )
                if result == QDialog.Accepted:
                    self.save_file()
            self.cli_options = read_json_result[1]
        else:
            UserDialogs.logger.info("Incorrect json type")
            self.create_file_error_qdialog("Incorrect json type", file)
            return -2  # incorrect json type

        # empty the trees
        UserDialogs.logger.debug("clearing trees")
        self.settings_tree.clear()
        self.command_tree.clear()

        # rebuild the trees from the new cli options file
        UserDialogs.logger.debug("rebuilding trees")
        self.cli_options["commands"]["primary id key"] = "0"
        self.session["opt"]["save_file_path"] = path
        self._parent.loading = True
        self.rebuild_command_tree()
        self.rebuild_settings_tree()
        self._parent.loading = False
        self.display_initial_code_preview()
        self.prompt_to_save = False
        self.windowtitle_set = False
        self.set_main_window_title()

        # move `path` to index 0
        UserDialogs.logger.debug(
            f"move this path to front of recent files list:\n{path}"
        )
        paths = self.session["opt"]["recent_files"]["paths"]
        if path in paths and paths.index(path) != 0:
            paths.insert(0, paths.pop(paths.index(path)))

        # remake menu
        UserDialogs.logger.debug("remake recent files menu")
        self.ui.actionOpen_Recent.setMenu(self.get_recent_files_menu())
        return read_json_result  # return size of file read

    def get_inputhandler_dir_from_user(self):
        dir_dlg = QFileDialog(self)
        _dlg_result = dir_dlg.getExistingDirectory(
            self,
            "Select InputHandler's directory",
            "",
            options=QFileDialog.DontUseNativeDialog
            | QFileDialog.ShowDirsOnly
            | QFileDialog.DontResolveSymlinks,
        )
        if _dlg_result == QFileDialog.rejected:
            b = QDialogButtonBox.StandardButton
            buttons = [b.Ok, b.Close]
            button_text = ["Select InputHandler's directory", "Close this tool"]
            result = self.root.create_qdialog(
                "You must select InputHandler's root directory to use this tool.",
                Qt.AlignCenter,
                Qt.NoTextInteraction,
                "Error, InputHandler's directory not located!",
                buttons,
                button_text,
                QStyle.StandardPixmap.SP_MessageBoxCritical,
                self.qscreen,
            )
            if result == QDialog.Accepted:
                self.get_inputhandler_dir_from_user()
            if result == 3:
                sys.exit("Need InputHandler's directory for tool dependencies.")

        _lib_root_path = QDir(_dlg_result)
        _file_dir_list = _lib_root_path.toNativeSeparators(
            _lib_root_path.absolutePath()
        ).split(_lib_root_path.separator())
        if "InputHandler" not in _file_dir_list:
            self.get_inputhandler_dir_from_user()

    def set_up_session(self):
        """sets up user session json"""
        self.logger.debug("Attempt session json load.")
        # load cli_gen_tool (session) json if exists, else use default options
        self.session = self.load_cli_gen_tool_json(self.cli_gen_tool_json_path)
        if not isinstance(self.session, dict):
            self.session = DataModels.default_session_model
        # pretty session json
        # session json contains only json serializable items, safe to print
        self.logger.debug(
            f"cli_gen_tool.json =\n{str(json.dumps(self.session, indent=2))}"
        )
        last_interface = QFile()
        if self.session["opt"]["save_file_path"] is not None:
            last_interface_path = QDir(self.session["opt"]["save_file_path"])
            self.logger.debug("Attempt load last interface")
            last_interface = QFile(
                last_interface_path.toNativeSeparators(
                    last_interface_path.absolutePath()
                )
            )
        if self.session["opt"]["save_file_path"] != "" and last_interface.exists():
            result = self.read_json(last_interface)
            self.cli_options = result[1]
            self.cli_options["commands"]["primary id key"] = "0"
        elif (
            self.session["opt"]["save_file_path"] != "" and not last_interface.exists()
        ):
            b = QDialogButtonBox.StandardButton
            buttons = [b.Ok, b.Cancel]
            button_text = ["Select last file", "Continue without locating"]
            result = self.create_qdialog(
                str(
                    f"Cannot locate last working file: {str(last_interface.fileName())}"
                ),
                Qt.AlignCenter,
                Qt.NoTextInteraction,
                "Error, cannot find interface file!",
                buttons,
                button_text,
                QStyle.StandardPixmap.SP_MessageBoxCritical,
            )
            if result == QDialog.Accepted:
                dlg = QFileDialog(self)
                result = dlg.getOpenFileName(
                    self,
                    str(f"Locate: {last_interface.fileName()}"),
                    last_interface_path.toNativeSeparators(
                        last_interface_path.absoluteFilePath(last_interface.fileName())
                    ),
                    "*.json",
                    options=QFileDialog.DontUseNativeDialog,
                )
                if result == QFileDialog.rejected:
                    self.logger.info(
                        "User couldn't locate last working file, continuing."
                    )
            else:
                p = self.session["opt"]["save_file_path"]
                self.logger.info(f"Couldn't locate last working file: {p}")
                self.session["opt"]["save_file_path"] = ""

                self.set_main_window_title("InputHandler CLI generation tool ")

    def get_config_file(self, config_path: str = None):
        """gets new valid config file

        Args:
            config_path (str, optional): path to alternate config. Defaults to None.
        """
        old_path = self.old_path
        new_path = config_path
        if new_path == None:
            cfg_path_dlg = QFileDialog(self)
            fileName = cfg_path_dlg.getOpenFileName(
                self,
                "InputHandler config file name",
                QDir(
                    self.session["opt"]["inputhandler_config_file_path"]
                ).toNativeSeparators(
                    self.session["opt"]["inputhandler_config_file_path"]
                ),
                "config.h",
                options=QFileDialog.DontUseNativeDialog,
            )
            if fileName[0] == "":
                UserDialogs.logger.info("browse for config cancelled.")
                return
            fqname = fileName[0]
            new_path = QDir(fqname).absolutePath()
            new_path = QDir(new_path).toNativeSeparators(new_path)
        if new_path == old_path:
            UserDialogs.logger.info("Same config file selected.")
            return
        self.session["opt"]["inputhandler_config_file_path"] = fqname
        self._parent.preferences.dlg.config_path_input.setText(str(fqname))
        self._parent.preferences.dlg.config_path_input.setToolTip(str(fqname))
        # restart to apply selected config
        self._parent.restart(self._parent, "New config file selected.")
