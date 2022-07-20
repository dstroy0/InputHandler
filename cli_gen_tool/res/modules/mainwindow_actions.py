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
import platform, json, sys, os
from PySide6.QtWidgets import QFileDialog, QDialog, QVBoxLayout, QLabel
from PySide6.QtCore import QFile, QIODevice, QTextStream, QByteArray, Qt
from res.modules.logging_setup import Logger
# mainwindow actions class
class MainWindowActions(object):    
    logger = ""
    def __init__(self):
        super().__init__()
        MainWindowActions.logger = Logger.get_logger(self, __name__)
    
    # TODO save session on close, prompt user to save work if there is any
    # do before close
    def do_before_app_close(self):
        MainWindowActions.logger.info("Exiting CLI generation tool")
        self.log.close()
    # close gui
    def gui_exit(self):
        self.do_before_app_close()        
        sys.exit(self.app.quit())
    
    def closeEvent(self, event):
        self.do_before_app_close()
        event.accept()

    def load_cli_gen_tool_json(self, path):
        session = {}
        file = QFile(path)
        if not file.exists():
            MainWindowActions.logger.info("cli_gen_tool.json doesn't exist, using default options")
            session = self.defaultGuiOpt
            session["opt"]["input_config_file_path"] = self.default_lib_config_path
            return session
        if not file.open(QIODevice.ReadOnly | QIODevice.Text):
            file.close()
            MainWindowActions.logger.warning("open cli_gen_tool.json error; using default options")
            session = self.defaultGuiOpt
            session["opt"]["input_config_file_path"] = self.default_lib_config_path
            return session
        data_in = QTextStream(file).readAll()
        file.close()
        try:
            # TODO validate session json
            session = json.loads(data_in)
            MainWindowActions.logger.info(
                "\ncli_gen_tool.json:\n" +
                str(json.dumps(session, indent=4, sort_keys=True)))
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
            MainWindowActions.logger.warning("Unable to write new cli_gen_tool.json, please check permissions.")
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
            self.create_popup_dialog_box(
                "Save file error.", "Error", self.ui.messageBoxCriticalIcon
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
        MainWindowActions.logger.info("save CLI settings file as: "+ str(fqname))
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
        # inherit from parent QMainWindow (block main window interaction while dialog box is open)
        dlg = QDialog(self)
        dlg.layout = QVBoxLayout()
        dlg.setWindowTitle("About")
        dlg.git_link_label = QLabel()
        dlg.git_link_label.setText(
            '<a href="https://github.com/dstroy0/InputHandler">Link to library git</a>'
        )
        dlg.git_link_label.setAlignment(Qt.AlignCenter)
        dlg.git_link_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        dlg.git_link_label.setOpenExternalLinks(True)
        dlg.layout.addWidget(dlg.git_link_label)
        dlg.author_credit_label = QLabel()
        dlg.author_credit_label.setText(
            "Library authors:\nDouglas Quigg (dstroy0 dquigg123@gmail.com)\nBrendan Doherty (2bndy5 2bndy5@gmail.com)"
        )
        dlg.author_credit_label.setAlignment(Qt.AlignCenter)
        dlg.layout.addWidget(dlg.author_credit_label)
        dlg.setLayout(dlg.layout)
        dlg.exec()

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
        if not self.log.isVisible():
            self.log.show()
            self.log.setWindowState(Qt.WindowState.WindowActive)
    
    def mainwindow_menu_bar_actions_setup(self):        
        # file menu actions setup
        # file menu
        self.ui.actionOpen.triggered.connect(self.open_file)
        self.ui.actionSave.triggered.connect(self.save_file)
        self.ui.actionSave_As.triggered.connect(self.save_file_as)
        self.ui.actionPreferences.triggered.connect(self.gui_settings)
        self.ui.actionExit.triggered.connect(self.gui_exit)
        # generate menu
        self.ui.actionGenerate_CLI_Files.triggered.connect(self.generate_cli_files)
        # about menu
        self.ui.actionAbout.triggered.connect(self.gui_about)
        self.ui.actionInputHandler_Documentation.triggered.connect(
            self.gui_documentation
        )
        self.ui.actionOpen_Log_History.triggered.connect(self.gui_log_history)
        # end file menu actions setup
        self.app.aboutToQuit.connect(self.gui_exit)

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
