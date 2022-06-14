##
# @file cli_gen_tool.py
# @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
# @brief InputHandler CLI generation tool
# @version 0.1
# @date 2022-06-10
# @copyright Copyright (c) 2022

# Copyright (C) 2022 Douglas Quigg (dstroy0) <dquigg123@gmail.com>

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 3 as published by the Free Software Foundation.

from __future__ import absolute_import  # easy import pathing
import os
import sys
import json
import platform
from PySide6.QtWidgets import (QApplication, QMainWindow, QDialog, QLabel,
                               QVBoxLayout, QFileDialog, QHeaderView)
from PySide6.QtCore import (QFile, Qt, QIODevice, QTextStream,
                            QByteArray, QDir)
# import class generated by PySide6 uic
from res.uic.mainWindow import Ui_MainWindow

# MainWindow setup
# settings_tree widget setup


def settings_tree_setup(self):
    # print('settings_tree setup')
    self.ui.settings_tree.setHeaderLabels(("Setting", "Type", "Value"))
    self.ui.settings_tree.header().setSectionResizeMode(0, QHeaderView.Stretch)
    self.ui.settings_tree.header().setSectionResizeMode(2, QHeaderView.Stretch)

# actions setup


def actions_setup(self):
    # print('actions setup')
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
        self.gui_documentation)

# button setup


def buttons_setup(self):
    # print('buttons setup')
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
        self.clicked_open_close_command_settings_menu_tab_two)
    # visible if self.ui.command_settings.isVisible()
    self.ui.closeSettingsMenuButton.clicked.connect(
        self.clicked_close_command_settings_menu_tab_two)
    self.ui.commandSettingsMenuApplyButton.clicked.connect(
        self.clicked_apply_command_settings_menu_tab_two)

# change-driven events


def triggers_setup(self):
    # print('triggers setup')
    # tab 2
    self.ui.commandString.textChanged.connect(self.command_string_text_changed)
# end MainWindow setup

# MainWindow runs everything


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # MainWindow var
        # session db
        self.session = ''
        # active save filename
        self.saveFileName = ''
        
        # cli opt  
        self.command_settings_dict = {'var': {'num_commands': 0},
                                      'commands': {}}
        
        # command parameters dict keys list
        self.commandParametersKeys = ['functionName',
                                      'commandString',
                                      'commandLength',
                                      'parentId',
                                      'commandId',
                                      'commandHasWildCards',
                                      'commandDepth',
                                      'commandSubcommands',
                                      'commandArgumentHandling',
                                      'commandMinArgs',
                                      'commandMaxArgs']
        
        # default settings dict to regen cli_gen_tool.json if it becomes corrupt
        self.defaultOpt = {"opt": 
                            {"save_filename":None,
                             "recent_files":{},
                             "output_dir":"default",
                             "window_size":"default"}}

        # tab 1
        settings_tree_setup(self)  # settings_tree widget setup

        # tab 2
        self.ui.command_settings.hide()  # hide command settings menu widget

        # connect objects to methods
        actions_setup(self)  # actions setup
        buttons_setup(self)  # buttons setup
        triggers_setup(self)  # triggers setup

        # load cli_gen_tool (session) json
        path = QDir.currentPath() + "/cli_gen_tool/cli_gen_tool.json"
        file = QFile(path)
        if (not file.open(QIODevice.ReadOnly | QIODevice.Text)):
            return  # TODO generate new cli_gen_tool json
        out = QTextStream(file).readAll()
        file.close()
        print('cli_gen_tool.json opened')
        # print(path)
        try:
            self.session = json.loads(out)
            print(self.session)
        except (ValueError, RuntimeError, TypeError, NameError) as e:
            # TODO generate new cli_gen_tool json
            print(e)

    # actions
    def open_file(self):
        print('open file')
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
        if (not file.open(QIODevice.ReadOnly | QIODevice.Text)):
            return  # TODO error
        f_text = QTextStream(file).readAll()
        file.close()
        self.command_settings_dict = json.loads(f_text)  # TODO try/except

    def save_file(self):
        print('save file')
        if self.saveFileName == '':
            self.save_file_as()
            return
        file = QFile(self.saveFileName)
        if (not file.open(QIODevice.WriteOnly | QIODevice.Text)):
            return  # TODO error
        out = QByteArray(json.dumps(self.command_settings_dict,
                         indent=4, sort_keys=True))  # dump pretty json
        file.write(out)
        file.close()

    def save_file_as(self):
        print('save file as')
        # inherit from parent QMainWindow (block main window interaction while dialog box is open)
        dlg = QFileDialog(self)
        fileName = dlg.getSaveFileName(self, "Save file name", "", ".json")
        if fileName[0] == '':
            return  # dialog cancelled
        fqname = fileName[0] + ".json"
        self.saveFileName = fqname
        file = QFile(fqname)
        if (not file.open(QIODevice.WriteOnly | QIODevice.Text)):
            return  # TODO error
        out = QByteArray(json.dumps(self.cli_settings, indent=4,
                         sort_keys=True))  # dump pretty json
        file.write(out)
        file.close()

    # TODO
    def gui_settings(self):
        print('preferences')

    # close gui
    def gui_exit(self):
        sys.exit(app.exit())

    # TODO
    # generate CLI files
    def generate_cli_files(self):
        print('generate cli files')

    def gui_about(self):
        # print('about')
        # inherit from parent QMainWindow (block main window interaction while dialog box is open)
        dlg = QDialog(self)
        dlg.layout = QVBoxLayout()
        dlg.setWindowTitle('About')
        dlg.git_link_label = QLabel()
        dlg.git_link_label.setText(
            "<a href=\"https://github.com/dstroy0/InputHandler\">Link to library git</a>")
        dlg.git_link_label.setAlignment(Qt.AlignCenter)
        dlg.git_link_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        dlg.git_link_label.setOpenExternalLinks(True)
        dlg.layout.addWidget(dlg.git_link_label)
        dlg.author_credit_label = QLabel()
        dlg.author_credit_label.setText(
            "Library authors:\nDouglas Quigg (dstroy0 dquigg123@gmail.com)\nBrendan Doherty (2bndy5 2bndy5@gmail.com)")
        dlg.author_credit_label.setAlignment(Qt.AlignCenter)
        dlg.layout.addWidget(dlg.author_credit_label)
        dlg.setLayout(dlg.layout)
        dlg.exec()

    def gui_documentation(self):
        os_type = platform.uname().system.lower()  # lowercase os type
        # windows
        if os_type == "windows":
            os.system("start \"\" https://dstroy0.github.io/InputHandler/")
        # macos
        elif os_type == "darwin":
            os.system("open \"\" https://dstroy0.github.io/InputHandler/")
        # linux
        elif os_type == "linux":
            os.system("xdg-open \"\" https://dstroy0.github.io/InputHandler/")

    # buttons
    # tab 1
    # TODO
    def clicked_edit_tab_one(self):
        print('clicked tab 1 edit')
    # TODO

    def clicked_clear_tab_one(self):
        print('clicked tab 1 clear')
    # TODO

    def clicked_default_tab_one(self):
        print('clicked tab 1 default')
    # tab 2
    # TODO

    def clicked_edit_tab_two(self):
        print('clicked tab 2 edit')
    # TODO

    def clicked_new_tab_two(self):
        print('clicked tab 2 new')
    # TODO

    def clicked_delete_tab_two(self):
        print('clicked tab 2 delete')

    def clicked_open_close_command_settings_menu_tab_two(self):
        print('clicked open/close command settings menu')
        if self.ui.command_settings.isVisible():
            self.ui.command_settings.hide()
        else:
            self.ui.command_settings.show()

    def clicked_close_command_settings_menu_tab_two(self):
        print('clicked close command settings menu')
        self.ui.command_settings.hide()

    def clicked_apply_command_settings_menu_tab_two(self):
        print('clicked apply in command settings menu')
        settings_to_validate = dict.fromkeys(self.commandParametersKeys, False)
        settings_to_validate['functionName'] = self.ui.functionName.text()
        settings_to_validate['commandString'] = self.ui.commandString.text()
        settings_to_validate['commandLength'] = len(settings_to_validate['commandString'])
        settings_to_validate['parentId'] = self.ui.commandParentId.text()
        settings_to_validate['commandId'] = self.ui.commandId.text()
        settings_to_validate['commandHasWildcards'] = self.ui.commandHasWildcards.isChecked()
        settings_to_validate['commandDepth'] = self.ui.commandDepth.text()
        settings_to_validate['commandSubcommands'] = self.ui.commandSubcommands.text()
        settings_to_validate['commandArgumentHandling'] = self.ui.commandArgumentHandling.currentIndex()
        settings_to_validate['commandMinArgs'] = self.ui.commandMinArgs.text()
        settings_to_validate['commandMaxArgs'] = self.ui.commandMaxArgs.text()
        # validate
        # TODO
        settings_are_valid = True
        if not settings_are_valid:
            return # invalid setting detected
        # get array index
        cmd_idx = self.command_settings_dict['var']['num_commands']
        # make dict from defined keys
        self.command_settings_dict['commands'][cmd_idx] = dict.fromkeys(self.commandParametersKeys, False)
        # assign result to command dictionary at cmd_idx        
        self.command_settings_dict['commands'][cmd_idx] = settings_to_validate 
        # command parameters were accepted, so increment the array index
        self.command_settings_dict['var']['num_commands'] = self.command_settings_dict['var']['num_commands'] + 1

    def command_string_text_changed(self):
        self.ui.commandLengthLabel.setText(
            str(len(self.ui.commandString.text())))

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

# end of file
