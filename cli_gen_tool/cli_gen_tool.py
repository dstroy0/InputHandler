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

import os 
import sys
import json
from PySide6.QtWidgets import (QApplication, QMainWindow, QDialog, QLabel, QVBoxLayout)
from PySide6.QtCore import (QFile, Qt, QIODevice, QTextStream)
from ui import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # connect objects to methods
        # file menu
        self.ui.actionOpen.triggered.connect(self.open_file)
        self.ui.actionSave.triggered.connect(self.save_file)
        self.ui.actionPreferences.triggered.connect(self.gui_settings)
        # TODO
        # exit item
        # generate menu
        # TODO
        # about menu
        self.ui.actionAbout.triggered.connect(self.gui_about)
        self.ui.actionInputHandler_Documentation.triggered.connect(self.gui_documentation)
        # buttons
        # tab 1
        self.ui.editButton_1.clicked.connect(self.clicked_edit_tab_one)
        self.ui.clearButton_1.clicked.connect(self.clicked_clear_tab_one)
        self.ui.defaultButton_1.clicked.connect(self.clicked_default_tab_one)
        # tab 2
        self.ui.newButton_2.clicked.connect(self.clicked_new_tab_two)
        self.ui.editButton_2.clicked.connect(self.clicked_edit_tab_two)
        self.ui.deleteButton_2.clicked.connect(self.clicked_delete_tab_two)
        
        # load preferences json
        file = QFile("preferences.json")
        if (not file.open(QIODevice.ReadOnly | QIODevice.Text)):
            return # TODO error
        out = QTextStream(file)
        self.preferences = json.loads(out)

        # load defaults json
        file = QFile("default.json")
        if (not file.open(QIODevice.ReadOnly | QIODevice.Text)):
            return # TODO error
        out = QTextStream(file)
        self.cli_settings = json.loads(out)

    # actions
    # TODO
    def open_file(self):
        print('open file')
    # TODO
    def save_file(self):
        print('save file')
    # TODO
    def gui_settings(self):
        print('preferences')
    
    def gui_about(self):
        print('about')
        dlg = QDialog(self) # inherit from parent QMainWindow (block main window interaction while dialog box is open)
        dlg.layout = QVBoxLayout()
        dlg.setWindowTitle('About')
        dlg.git_link_label = QLabel()
        dlg.git_link_label.setText("<a href=\"https://github.com/dstroy0/InputHandler\">Link to library git</a>")
        dlg.git_link_label.setAlignment(Qt.AlignCenter)
        dlg.git_link_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        dlg.git_link_label.setOpenExternalLinks(True)
        dlg.layout.addWidget(dlg.git_link_label)
        dlg.author_credit_label = QLabel()
        dlg.author_credit_label.setText("Library authors:\nDouglas Quigg (dstroy0 dquigg123@gmail.com)\nBrendan Doherty (2bndy5 2bndy5@gmail.com)")
        dlg.author_credit_label.setAlignment(Qt.AlignCenter)
        dlg.layout.addWidget(dlg.author_credit_label)
        dlg.setLayout(dlg.layout)
        dlg.exec()

    # TODO
    def gui_documentation(self):
        # print('docs')
        # windows
        os.system("start \"\" https://dstroy0.github.io/InputHandler/")
        # macos
        # os.system("open \"\" https://dstroy0.github.io/InputHandler/")
        # linux
        # os.system("xdg-open \"\" https://dstroy0.github.io/InputHandler/")

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

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())