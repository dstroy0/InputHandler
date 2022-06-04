##
# @file cli_gen_tool.py
# @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
# @brief InputHandler CLI gen tool
# @version 0.1
# @date 2022-05-28
# @copyright Copyright (c) 2022

# Copyright (C) 2022 Douglas Quigg (dstroy0) <dquigg123@gmail.com>

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 3 as published by the Free Software Foundation.

import sys
import os
from PyQt5 import QtWidgets, uic

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method

        working_dir_path = os.path.dirname(os.path.abspath(__file__))
        # print(working_dir_path)
        ui_path = os.path.join(working_dir_path, "main.ui")
        # print(ui_path)

        uic.loadUi(ui_path, self) # Load the .ui file
        self.show() # Show the GUI

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()

# end of file
