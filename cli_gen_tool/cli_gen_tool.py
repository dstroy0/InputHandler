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

import sys
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QFile, QIODevice

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    ui_file_name = "main.ui"
    
    working_dir_path = os.path.dirname(os.path.abspath(__file__))
    # print(working_dir_path)
    ui_path = os.path.join(working_dir_path, ui_file_name)
    # print(ui_path)
    
    ui_file = QFile(ui_path)
    if not ui_file.open(QIODevice.ReadOnly):
        print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
        sys.exit(-1)
    loader = QUiLoader()
    window = loader.load(ui_file)
    ui_file.close()
    if not window:
        print(loader.errorString())
        sys.exit(-1)
    window.show()

    sys.exit(app.exec())

# end of file
