##
# @file mainwindow_actions.py
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

import json
import os
import platform
import sys

from PySide6.QtCore import QByteArray, QFile, QIODevice, Qt, QTextStream
from PySide6.QtWidgets import (
    QDialogButtonBox,
    QFileDialog,
    QStyle,
)
from res.modules.helper_methods import HelperMethods
from res.modules.logging_setup import Logger


# mainwindow actions class
class MainWindowActions(object):
    def __init__(self):
        super(MainWindowActions, self).__init__()
        MainWindowActions.logger = Logger.get_child_logger(self.logger, __name__)

    # do before close
    def do_before_app_close(self, event=None):
        MainWindowActions.logger.debug(event)
        result = 0
        if self.prompt_to_save == True:
            b = QDialogButtonBox.StandardButton
            buttons = [b.Save, b.Close, b.Cancel]
            button_text = ["", "Close without saving", ""]
            result = self.create_qdialog(
                "Save your work?",
                Qt.AlignCenter,
                0,
                "Save changes",
                buttons,
                button_text,
                HelperMethods.get_icon(
                    self, QStyle.StandardPixmap.SP_MessageBoxQuestion
                ),
            )
        else:  # no work to save
            result = 4
        # log the exit type
        if result == 0:
            if event != None and type(event) != bool:
                event.ignore()
            MainWindowActions.logger.info("Exit cancelled")
        elif result == 2:
            if self.save_file() >= 0:
                self.log.close()
                MainWindowActions.logger.info("Saved. Exiting CLI generation tool.")
                if self.write_cli_gen_tool_json() > 0:
                    MainWindowActions.logger.info("session json saved")
                if event != None and type(event) != bool:
                    event.accept()
                sys.exit(self.app.quit())
            else:
                MainWindowActions.logger.info("Exit cancelled")
        elif result == 3:
            self.log.close()
            MainWindowActions.logger.info("Not saved. Exiting CLI generation tool.")
            if event != None and type(event) != bool:
                event.accept()
            sys.exit(self.app.quit())
        elif result == 4:
            self.log.close()
            MainWindowActions.logger.info(
                "Nothing to Save. Exiting CLI generation tool."
            )
            if event != None and type(event) != bool:
                event.accept()
            sys.exit(self.app.quit())

    def create_file_error_qdialog(self, error_type: str, qfile: QFile):
        MainWindowActions.logger.warning(error_type + " file error.")
        self.create_qdialog(
            error_type + " error.",
            Qt.AlignCenter,
            0,
            error_type + " " + qfile.fileName() + " error",
            None,
            None,
            self.ui.messageBoxCriticalIcon,
        )

    def write_json(self, dict: dict, qfile: QFile, create_error_dialog: bool = False):
        if not qfile.open(QIODevice.WriteOnly | QIODevice.Text):
            MainWindowActions.logger.info("Save " + qfile.fileName() + " error.")
            if create_error_dialog:
                self.create_file_error_qdialog("Save", qfile)
            return -1  # file error
        out = QByteArray(
            json.dumps(
                dict,
                indent=2,
                sort_keys=False,
                default=lambda o: "non-serializable object",
            )
        )  # dump pretty json
        size = qfile.write(out)
        if size != -1:
            MainWindowActions.logger.info(
                "wrote " + str(size) + " bytes to " + str(qfile.fileName())
            )
        else:
            MainWindowActions.logger.info("Write " + qfile.fileName() + " error.")
            if create_error_dialog:
                self.create_file_error_qdialog("Write", qfile)
        qfile.close()
        return size

    def read_json(self, qfile: QFile, create_error_dialog: bool = False):
        db = {}
        if not qfile.exists():
            MainWindowActions.logger.info("qfile.exists() == false")
            if create_error_dialog:
                self.create_file_error_qdialog("File not exists", qfile)
            return [-2, {}]  # file doesn't exist
        if not qfile.open(QIODevice.ReadOnly | QIODevice.Text):
            qfile.close()
            MainWindowActions.logger.warning("File access error.")
            if create_error_dialog:
                self.create_file_error_qdialog("Access", qfile)
            return [-3, {}]  # access error
        data_in = QTextStream(qfile).readAll()
        qfile.close()
        try:
            db = json.loads(data_in)
            MainWindowActions.logger.info("loaded json: " + db["type"])
            return [len(data_in), db]
        except Exception as e:
            MainWindowActions.logger.warning(str(e))
            return [-4, {}]

    def save_file(self):
        MainWindowActions.logger.info("save CLI settings file")
        MainWindowActions.logger.debug("set tool version var in cliOpt")
        self.cliOpt["var"]["tool_version"] = self.version
        if (
            self.session["opt"]["save_filename"] == ""
            or self.session["opt"]["save_filename"] == None
        ):
            ret = self.save_file_as()
            return ret
        file = QFile(self.session["opt"]["save_filename"])
        ret = self.write_json(self.cliOpt, file, True)
        self.prompt_to_save = False
        return ret

    def save_file_as(self):
        # inherit from parent QMainWindow (block main window interaction while dialog box is open)
        dlg = QFileDialog(self)
        fileName = dlg.getSaveFileName(
            self, "Save file name", "", ".json", options=QFileDialog.DontUseNativeDialog
        )
        if fileName[0] == "":
            MainWindowActions.logger.info("Save file dialog cancelled.")
            return QFileDialog.Rejected  # dialog cancelled
        fqname = fileName[0] + ".json"
        self.session["opt"]["save_filename"] = fqname
        MainWindowActions.logger.info("save CLI settings file as: " + str(fqname))
        file = QFile(fqname)
        ret = self.write_json(self.cliOpt, file, True)
        return ret

    def load_cli_gen_tool_json(self, path):
        file = QFile(path)
        read_json_result = self.read_json(file, False)
        error = read_json_result[0]
        _json = read_json_result[1]
        if error == -2:  # file not exists
            MainWindowActions.logger.info(
                "cli_gen_tool.json doesn't exist, using default options"
            )
            _json = self.defaultGuiOpt
            _json["opt"]["input_config_file_path"] = self.default_lib_config_path
            return _json
        if error == -3:
            file.close()
            MainWindowActions.logger.warning(
                "open cli_gen_tool.json error; using default options"
            )
            _json = self.defaultGuiOpt
            _json["opt"]["input_config_file_path"] = self.default_lib_config_path
            return _json
        return _json

    def write_cli_gen_tool_json(self):
        file = QFile(self.cli_gen_tool_json_path)
        err = self.write_json(self.session, file, False)
        return err

    # MainWindow actions
    def open_file(self):
        MainWindowActions.logger.info("open CLI settings file dialog")
        # inherit from parent QMainWindow (block main window interaction while dialog box is open)
        dlg = QFileDialog(self)
        dlg.setFileMode(QFileDialog.ExistingFile)
        dlg.setNameFilter("Settings json (*.json)")
        dlg.setViewMode(QFileDialog.Detail)
        fileName = dlg.getOpenFileName(options=QFileDialog.DontUseNativeDialog)
        if fileName[0] == "":
            MainWindowActions.logger.info("open CLI settings file dialog cancelled")
            return  # dialog cancelled
        else:
            file = QFile(fileName[0])
            read_json_result = self.read_json(file, True)
            self.cliOpt = read_json_result[1]
            # empty trees
            self.ui.settings_tree.clear()
            self.ui.command_tree.clear()
            # rebuild from file
            self.build_lib_settings_tree()
            self.build_command_tree()
            self.display_initial_code_preview()
            self.prompt_to_save = False

    # TODO
    def gui_settings(self):
        MainWindowActions.logger.info("opened preferences dialog")
        self.preferences.exec()

    # TODO
    # generate CLI files
    def generate_cli_files(self):
        MainWindowActions.logger.info("generate cli files")

    def gui_about(self):
        MainWindowActions.logger.info("open about dialog")
        about_string = """<a href=\"https://github.com/dstroy0/InputHandler\">Link to library github</a><br><br>
        Library authors:<br>
        Douglas Quigg (dstroy0 dquigg123@gmail.com)<br>
        Brendan Doherty (2bndy5 2bndy5@gmail.com)<br>"""
        self.create_qdialog(
            about_string,
            Qt.AlignCenter,
            Qt.TextBrowserInteraction,
            "About",
            None,
            None,
            self.ui.messageBoxQuestionIcon,
        )

    ## opens an internet browser to the library's documentation
    def gui_documentation(self):
        MainWindowActions.logger.info("open GUI documentation")
        os_type = platform.uname().system.lower()  # lowercase os type
        # windows
        if os_type == "windows":
            os.system('start "" https://dstroy0.github.io/InputHandler/')
        # macos
        elif os_type == "darwin":
            os.system('open "" https://dstroy0.github.io/InputHandler/')
        # linux
        elif os_type == "linux":
            os.system('xdg-open "" https://dstroy0.github.io/InputHandler/')

    ## opens the log history subwindow
    def gui_log_history(self):
        if not self.log.isActiveWindow() and not self.log.isVisible():
            self.log.show()
            self.log.raise_()
            self.log.activateWindow()
            return
        if self.log.isVisible():
            self.log.raise_()
            self.log.activateWindow()

    ## MainWindow file menu actions
    def mainwindow_menu_bar_actions_setup(self):
        # file menu actions setup
        # file menu
        self.ui.actionOpen.triggered.connect(self.open_file)
        self.ui.actionSave.triggered.connect(self.save_file)
        self.ui.actionSave_As.triggered.connect(self.save_file_as)
        self.ui.actionPreferences.triggered.connect(self.gui_settings)
        self.ui.actionExit.triggered.connect(self.app.quit)
        # generate menu
        self.ui.actionGenerate_CLI_Files.triggered.connect(self.generate_cli_files)
        # about menu
        self.ui.actionAbout.triggered.connect(self.gui_about)
        self.ui.actionInputHandler_Documentation.triggered.connect(
            self.gui_documentation
        )
        self.ui.actionOpen_Log_History.triggered.connect(self.gui_log_history)
        # end file menu actions setup

    ## MainWindow button actions
    def mainwindow_button_actions_setup(self):
        # buttons setup
        # tab 1
        self.ui.editButton_1.clicked.connect(self.clicked_edit_tab_one)
        self.ui.clearButton_1.clicked.connect(self.clicked_clear_tab_one)
        self.ui.defaultButton_1.clicked.connect(self.clicked_default_tab_one)
        # tab 2
        # always visible
        self.ui.new_cmd_button.clicked.connect(self.clicked_new_cmd_button)
        self.ui.editButton_2.clicked.connect(self.clicked_edit_tab_two)
        self.ui.deleteButton_2.clicked.connect(self.clicked_delete_tab_two)
        self.ui.cmd_settings_menu_button.clicked.connect(
            self.clicked_command_settings_menu_button_tab_two
        )
        self.ui.command_tree.itemSelectionChanged.connect(self.command_menu_button_toggles)
        # end buttons setup

    # end MainWindow actions


# end of file
