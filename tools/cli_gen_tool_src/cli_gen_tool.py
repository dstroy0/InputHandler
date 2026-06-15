##
# @file cli_gen_tool.py
# @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
# @brief InputHandler CLI generation tool
# @version 1.0.0
# @date 2023-05-22
# @copyright Copyright (c) 2023
# Copyright (C) 2023 Douglas Quigg (dstroy0) <dquigg123@gmail.com>
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 3 as published by the Free Software Foundation.

import os
import sys
import copy
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
from modules.data_models import DataModels
from modules.cli.readme import ReadMe
from modules.cli.header_files.config_h import Config_H
from modules.cli.header_files.cli_h import CLI_H
from modules.cli.header_files.functions_h import Functions_H
from modules.cli.header_files.parameters_h import Parameters_H
from modules.cli.filestrings import CLIFileStrings
from modules.cli.parse_config import ParseInputHandlerConfig
from modules.cli.cli_helper_methods import CLIHelperMethods


## tool version
version = 1.0  # save serialization

## How long should the splash be displayed (in ms)
splashscreen_duration = 750


class GUI(Pathing, Logger, UserDialogs, FileManipulation, object):
    """Initializes Qt services and the tool GUI

    Args:
        Pathing (object): script/binary pathing
        Logger (object): logging services
        UserDialogs (object): user dialogs/interaction
        FileManipulation (object): cli file editing, cli settings json read
        object (object): base class extended
    """

    def __init__(self, init_instance) -> None:
        self.args = init_instance.args
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
        self.root_log_handler.info("Loading tool.")
        self.root.import_methods()
        self.mainwindow = MainWindow(self)  # pass init object to MainWindow
        # exit on user command
        sys.exit(self.app.exec())

    def set_lib_root_path(self):
        init_abs_path = os.path.abspath(os.getcwd())
        self.root_log_handler.info("Setting up Pathing.")
        self.root_log_handler.info(f"os.getcwd: {init_abs_path}")
        path_dir_list = init_abs_path.split(os.path.sep)

        if not bool(init_abs_path.find("InputHandler")):
            # prompt user for lib dir
            self.root.get_inputhandler_dir_from_user()
        else:
            cdup = 0
            for dirname in reversed(range(len(path_dir_list))):
                if path_dir_list[dirname] == "InputHandler":
                    self.root_log_handler.info("At InputHandler library root.")
                    break
                os.chdir("..")            
            self.lib_root_path = os.path.abspath(os.getcwd())
            self.root_log_handler.info(f"Moved up {cdup} directories.")            
            self.root_log_handler.info(f"InputHandler root path: {self.lib_root_path}")            


class Headless(
    ParseInputHandlerConfig,
    CLIFileStrings,
    ReadMe,
    Config_H,
    CLI_H,
    Functions_H,
    Parameters_H,
    CLIHelperMethods,
    Pathing,
    Logger,
    FileManipulation,
    object,
):
    """No Qt services loaded, completely headless use -h to see options when launching cli_gen_tool.py

    Args:
        ParseInputHandlerConfig (object): Parses config.h
        CLIFileStrings (object): CLI template/license strings
        ReadMe (object): readme generator
        Config_H (object): config.h generator
        CLI_H (object): cli.h generator
        Functions_H (object): functions.h generator
        Parameters_H (object): parameters.h generator
        CLIHelperMethods (object): formatting helpers
        Pathing (object): script/binary pathing
        Logger (object): logging services
        FileManipulation (object): cli file editing, cli settings json read
        object (object): base class extended
    """
    def __init__(self, init_instance) -> None:
        self.args = init_instance.args
        self.cli_options = init_instance.cli_options
        self.version = version
        self.headless = True
        self.lib_version = "0.0.0"
        self.default_settings_tree_values = {}
        self.session = {
            "opt": {
                "cli_output_dir": os.path.abspath(self.args.destination_path)
            }
        }
        
        super(Headless, self).__init__()
        FileManipulation.__init__(self)
        
        self.lib_root_path = os.path.abspath(self.args.library_path)
        self.set_pathing()
        
        # Reinstate versions now that pathing is set
        CLIFileStrings.__init__(self)
        
        # Initialize preview dict structure
        self.code_preview_dict = copy.deepcopy(DataModels.generated_filename_dict)
        
        self.root_log_handler.info("creating cli with supplied arguments")
        
        # Parse config.h
        if self.args.config:
            config_path = os.path.abspath(self.args.config[0])
        else:
            config_path = ""
        self.parse_config_header_file(config_path)
        
        # Run generation
        destination = os.path.abspath(self.args.destination_path)
        result = self.generate_cli(destination)
        if result == -1:
            self.root_log_handler.error("Invalid output directory")
            sys.exit(1)
        elif result == -2:
            self.root_log_handler.error("Invalid InputHandler library directory")
            sys.exit(1)
        elif result == -3:
            self.root_log_handler.error("Error creating directory <CLI>")
            sys.exit(1)
        elif result == -4:
            self.root_log_handler.error("File write error during CLI generation")
            sys.exit(1)
            
        self.root_log_handler.info("CLI generated successfully!")
        sys.exit(0)


class Init(Pathing, Logger, ToolCLI, object):
    """Pre-Qt script initialization

    Args:
        Pathing (object): script/binary pathing
        Logger (object): logging services
        ToolCLI (object): gets arguments to script
        object (object): base class extended
    """

    def __init__(self) -> None:
        super(Init, self).__init__()
        Logger.__init__(self)
        Pathing.__init__(self)
        self.setup_logging(__name__)
        self.root_log_handler = self.get_root_logger()
        self.stream_log_handler = self.get_stream_logger()
        self.args = self.get_args()
        self.version = version
        if self.args.headless:
            self.cli_options = self.args.cli_options_json
            Headless(self)
        else:
            GUI(self)


def main():
    Init()


if __name__ == "__main__":
    main()

# end of file
