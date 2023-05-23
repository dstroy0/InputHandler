##
# @file cli_gen_tool.py
# @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
# @brief InputHandler CLI generation tool
# @version 1.0
# @date 2023-05-22
# @copyright Copyright (c) 2023
# Copyright (C) 2023 Douglas Quigg (dstroy0) <dquigg123@gmail.com>
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 3 as published by the Free Software Foundation.

import os
import sys
import qdarktheme
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from modules.logger import Logger  # logging methods
from modules.tool_cli import ToolCLI  # cli_gen_tool CLI
from modules.file_manipulation import FileManipulation
from modules.user_dialogs import UserDialogs
from modules.mainwindow import MainWindow
from modules.widgets import RootWidget
from modules.pathing import Pathing


## tool version
version = 1.0  # save serialization

## How long should the splash be displayed (in ms)
splashscreen_duration = 750


## set up pathing, logging, splash screen
class GUI(Pathing, Logger, UserDialogs, FileManipulation, object):
    def __init__(self) -> None:
        super().__init__()
        UserDialogs.__init__(self)
        FileManipulation.__init__(self)
        self.version = version
        self.splashscreen_duration = splashscreen_duration
        # setup logger

        self.set_lib_root_path()
        self.set_pathing()
        self.setup_file_handler()
        self.root_log_handler.addHandler(self.get_file_handler())

        UserDialogs.setup_logging(self)

        # GUI container
        app = QApplication(sys.argv)
        app.setAttribute(Qt.AA_EnableHighDpiScaling)
        # GUI styling
        app.setStyleSheet(qdarktheme.load_stylesheet())
        self.app = app

        self.root = RootWidget(self)

        self.mainwindow_screen = self.app.primaryScreen()
        self.root_log_handler.info("Loading CLI generation tool.")
        self.root.import_methods()
        self.mainwindow = MainWindow(self)  # pass init object to MainWindow
        # exit on user command
        sys.exit(self.app.exec())

    def set_lib_root_path(self):
        init_abs_path = os.path.abspath(os.getcwd())
        self.root_log_handler.info("Path to me: " + str(init_abs_path))
        path_dir_list = init_abs_path.split(os.path.sep)

        if not bool(init_abs_path.find("InputHandler")):
            # prompt user for lib dir
            self.root.get_inputhandler_dir_from_user()
        else:
            num_cdup_to_lib_root = 0
            for dirname in reversed(range(len(path_dir_list))):
                if path_dir_list[dirname] == "InputHandler":
                    self.root_log_handler.info(
                        "num dir below InputHandler root: " + str(num_cdup_to_lib_root)
                    )
                    break
                num_cdup_to_lib_root += 1
            self.root_log_handler.info(
                "moving up " + str(num_cdup_to_lib_root) + " dir"
            )
            for i in range(num_cdup_to_lib_root):
                os.chdir("..")
            self.root_log_handler.info("Lib root path: " + os.path.abspath(os.getcwd()))
            self.lib_root_path = os.path.abspath(os.getcwd())


class Headless(Pathing, Logger, FileManipulation, object):
    def __init__(self) -> None:
        super(Headless, self).__init__()
        FileManipulation.__init__(self)
        self.lib_root_path = os.path.abspath(self.args.generate[0])
        self.set_pathing()
        print("creating cli with supplied arguments")
        sys.exit(0)


class Init(Pathing, Logger, ToolCLI, object):
    def __init__(self) -> None:
        super(Init, self).__init__()
        Logger.__init__(self)
        Pathing.__init__(self)
        self.setup_logging(__name__)
        self.root_log_handler = self.get_root_logger()
        self.stream_log_handler = self.get_stream_logger()
        self.args = self.script_cli()
        if self.args.headless:
            Headless()
        else:
            GUI()


# end Initialize()


## main function
def main():
    Init()


# you can run this script
if __name__ == "__main__":
    main()

# end of file
