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

import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile
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
    # TODO
    def gui_about(self):
        print('about')
    # TODO
    def gui_documentation(self):
        print('docs')

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