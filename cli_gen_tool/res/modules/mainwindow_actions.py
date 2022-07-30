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

    # TODO save session on close, prompt user to save work if there is any
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
            self.settings.setValue("geometry", self.saveGeometry())
            self.settings.setValue("windowState", self.saveState())
            self.log.close()
            MainWindowActions.logger.info("Saved. Exiting CLI generation tool.")
            if event != None and type(event) != bool:
                event.accept()
            sys.exit(self.app.quit())
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

    def load_cli_gen_tool_json(self, path):
        session = {}
        file = QFile(path)
        if not file.exists():
            MainWindowActions.logger.info(
                "cli_gen_tool.json doesn't exist, using default options"
            )
            session = self.defaultGuiOpt
            session["opt"]["input_config_file_path"] = self.default_lib_config_path
            return session
        if not file.open(QIODevice.ReadOnly | QIODevice.Text):
            file.close()
            MainWindowActions.logger.warning(
                "open cli_gen_tool.json error; using default options"
            )
            session = self.defaultGuiOpt
            session["opt"]["input_config_file_path"] = self.default_lib_config_path
            return session
        data_in = QTextStream(file).readAll()
        file.close()
        try:
            # TODO validate session json
            session = json.loads(data_in)
            MainWindowActions.logger.info(
                "\ncli_gen_tool.json:\n"
                + str(json.dumps(session, indent=4, sort_keys=True))
            )
            return session
        except (ValueError, RuntimeError, TypeError, NameError) as e:
            MainWindowActions.logger.warning("json corrupt, removing")
            if self.json_except == 1:
                MainWindowActions.logger.warning("unable to read json, app exit")
                self.app.quit()
            self.json_except = 1
            os.remove(path)  # delete corrupt json
            self.write_cli_gen_tool_json(
                path, self.defaultGuiOpt
            )  # recreate cli_gen_tool.json
            MainWindowActions.logger.warning(e)
            session = self.defaultGuiOpt
            session["opt"]["input_config_file_path"] = self.default_lib_config_path
            return session

    def write_cli_gen_tool_json(self, path, db):
        file = QFile(path)
        if not file.open(QIODevice.WriteOnly | QIODevice.Text):
            MainWindowActions.logger.warning(
                "Unable to write new cli_gen_tool.json, please check permissions."
            )
            return -1
        out = QByteArray(json.dumps(db, indent=4, sort_keys=True))  # dump pretty json
        err = file.write(out)
        MainWindowActions.logger.info("write successful")
        file.close()
        return err

    # MainWindow actions
    def open_file(self):
        MainWindowActions.logger.info("open CLI settings file")
        # inherit from parent QMainWindow (block main window interaction while dialog box is open)
        dlg = QFileDialog(self)
        dlg.setFileMode(QFileDialog.ExistingFile)
        dlg.setNameFilter("Settings json (*.json)")
        dlg.setViewMode(QFileDialog.Detail)
        fileName = ""
        if dlg.exec():
            fileName = dlg.selectedFiles()
        else:
            return  # dialog cancelled
        file = QFile(fileName[0])
        if not file.open(QIODevice.ReadOnly | QIODevice.Text):
            MainWindowActions.logger.warning("File read error")
            self.create_popup_dialog_box(
                "File read error.", "Error", self.ui.messageBoxCriticalIcon
            )
            return  # file read error
        data_in = QTextStream(file).readAll()
        file.close()
        data_in_dict = {}
        err = False
        try:
            data_in_dict = json.loads(data_in)
        except:
            MainWindowActions.logger.warning("json encoding error")
            err = True
        try:
            if data_in_dict["type"] != "cli options":
                MainWindowActions.logger.warning("json type error")
        except:
            MainWindowActions.logger.warning("json key error")
            err = True
        if err == True:
            return  # error flag set
        else:
            self.cliOpt = json.loads(data_in)
            MainWindowActions.logger.info("CLI options json loaded.")

    def save_file(self):
        MainWindowActions.logger.info("save CLI settings file")
        if self.saveFileName == "":
            self.save_file_as()
            return
        file = QFile(self.saveFileName)
        if not file.open(QIODevice.WriteOnly | QIODevice.Text):
            MainWindowActions.logger.warning("Save file error.")
            self.create_qdialog(
                "Save file error.",
                Qt.AlignCenter,
                0,
                "Error",
                None,
                None,
                self.ui.messageBoxCriticalIcon,
            )
            return  # error

        out = QByteArray(
            json.dumps(self.cliOpt, indent=4, sort_keys=True)
        )  # dump pretty json
        file.write(out)
        file.close()

    def save_file_as(self):
        # inherit from parent QMainWindow (block main window interaction while dialog box is open)
        dlg = QFileDialog(self)
        fileName = dlg.getSaveFileName(self, "Save file name", "", ".json")
        if fileName[0] == "":
            return  # dialog cancelled
        fqname = fileName[0] + ".json"
        self.saveFileName = fqname
        MainWindowActions.logger.info("save CLI settings file as: " + str(fqname))
        file = QFile(fqname)
        if not file.open(QIODevice.WriteOnly | QIODevice.Text):
            return  # TODO error
        out = QByteArray(
            json.dumps(self.cliOpt, indent=4, sort_keys=True)
        )  # dump pretty json
        file.write(out)
        file.close()

    # TODO
    def gui_settings(self):
        MainWindowActions.logger.info("save CLI settings file as")("preferences")

    # TODO
    # generate CLI files
    def generate_cli_files(self):
        MainWindowActions.logger.info("save CLI settings file as")("generate cli files")

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

    def gui_log_history(self):
        print("t")
        if not self.log.isActiveWindow() and not self.log.isVisible():
            self.log.show()
            self.log.raise_()
            self.log.activateWindow()
            return
        if self.log.isVisible():
            self.log.raise_()
            self.log.activateWindow()

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

    def mainwindow_button_actions_setup(self):
        # buttons setup
        # tab 1
        self.ui.editButton_1.clicked.connect(self.clicked_edit_tab_one)
        self.ui.clearButton_1.clicked.connect(self.clicked_clear_tab_one)
        self.ui.defaultButton_1.clicked.connect(self.clicked_default_tab_one)
        # tab 2
        # always visible
        self.ui.newButton_2.clicked.connect(self.clicked_new_tab_two)
        self.ui.editButton_2.clicked.connect(self.clicked_edit_tab_two)
        self.ui.deleteButton_2.clicked.connect(self.clicked_delete_tab_two)
        self.ui.openCloseSettingsMenuButton.clicked.connect(
            self.clicked_open_command_settings_menu_tab_two
        )
        # end buttons setup

    # end MainWindow actions
