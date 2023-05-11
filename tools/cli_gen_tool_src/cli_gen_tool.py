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
from __future__ import absolute_import


# imports
import os
import sys
import qdarktheme
from PySide6.QtCore import (
    QEvent,
    QObject,
    QSettings,
    Qt,
    QTimer,
    QDir,
)
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QMainWindow,
    QStyle,
    QFileDialog,
    QWidget,
    QDialogButtonBox,
)

# import classes generated by PySide6 uic
from modules.uic.preferencesDialog import Ui_Preferences  # preferences dialog
from modules.uic.commandParametersDialog import (
    Ui_commandParametersDialog,
)  # tab two popup dialog box
from modules.uic.logHistoryDialog import Ui_logHistoryDialog  # log history dialog
from modules.uic.mainWindow import Ui_MainWindow  # main window with tabs
from modules.uic.generateCLIDialog import Ui_generateDialog  # file generation dialog

# external class methods
from modules.data_models import dataModels  # app data models
from modules.command_tree import CommandTreeMethods  # command tree interaction
from modules.command_parameters import (
    CommandParametersMethods,
)  # command parameters interaction
from modules.helper_methods import HelperMethods  # dialog creator
from modules.logging_setup import Logger  # logging methods
from modules.settings_tree import SettingsTreeMethods  # settings tree interaction
from modules.preferences import PreferencesMethods  # preferences interaction
from modules.mainwindow_methods import MainWindowMethods  # mainwindow interaction
from modules.code_generation import CodeGeneration  # code preview and generation
from modules.script_cli import ScriptCLI  # cli_gen_tool CLI
from modules.cli.cli_helper_methods import CLIHelperMethods  # file generation helpers
from modules.no_dialog_file_manipulation import NoDialogFileManipulation
from modules.user_dialogs import UserDialogs

## tool version
version = 1.0  # save serialization

## How long should the splash be displayed (in ms)
splashscreen_duration = 750


## mainwindow runs on top of "RootWidget"
class RootWidget(QWidget, object):
    def __init__(self, parent) -> None:
        super(RootWidget, self).__init__()
        self._parent = parent
        self.setObjectName("root")

    # shim
    def import_methods(self):
        self.app = self._parent.app
        self.get_app_screen = self._parent.get_app_screen
        self.create_qdialog = self._parent.create_qdialog
        self.write_cli_gen_tool_json = self._parent.write_cli_gen_tool_json
        self.write_json = self._parent.write_json
        self.read_json = self._parent.read_json
        self.create_file_error_qdialog = self._parent.create_file_error_qdialog
        self.get_project_dir = self._parent.get_project_dir
        self.open_file = self._parent.open_file

        self.root_log_handler = self._parent.root_log_handler
        self.setup_file_handler = self._parent.setup_file_handler
        self.get_child_logger = self._parent.get_child_logger
        self.set_up_window_history_logger = self._parent.set_up_window_history_logger
        self.logger = self.root_log_handler

        self.lib_root_path = self._parent.lib_root_path
        self.headless = self._parent.headless
        self.lib_version = self._parent.lib_version

        self.inputhandler_save_path = self._parent.inputhandler_save_path
        self.user_home_dir = self._parent.user_home_dir

    def get_inputhandler_dir_from_user(self):
        dir_dlg = QFileDialog(self)
        _dlg_result = dir_dlg.getExistingDirectory(
            self,
            "Select InputHandler's directory",
            "",
            options=QFileDialog.DontUseNativeDialog
            | QFileDialog.ShowDirsOnly
            | QFileDialog.DontResolveSymlinks,
        )
        if _dlg_result == QFileDialog.rejected:
            b = QDialogButtonBox.StandardButton
            buttons = [b.Ok, b.Close]
            button_text = ["Select InputHandler's directory", "Close this tool"]
            result = self.root.create_qdialog(
                "You must select InputHandler's root directory to use this tool.",
                Qt.AlignCenter,
                Qt.NoTextInteraction,
                "Error, InputHandler's directory not located!",
                buttons,
                button_text,
                QStyle.StandardPixmap.SP_MessageBoxCritical,
                self.qscreen,
            )
            if result == QDialog.Accepted:
                self.get_inputhandler_dir_from_user()
            if result == 3:
                sys.exit("Need InputHandler's directory for tool dependencies.")

        _lib_root_path = QDir(_dlg_result)
        _file_dir_list = _lib_root_path.toNativeSeparators(
            _lib_root_path.absolutePath()
        ).split(_lib_root_path.separator())
        if "InputHandler" not in _file_dir_list:
            self.get_inputhandler_dir_from_user()


## set up pathing, logging, splash screen
class Initialize(
    HelperMethods, NoDialogFileManipulation, UserDialogs, Logger, ScriptCLI, object
):
    def __init__(self) -> None:
        super(Initialize, self).__init__()

        # set save pathing and make save directories
        self.user_home_dir = os.path.expanduser("~")
        self.inputhandler_save_path = os.path.join(
            self.user_home_dir, "Documents", "InputHandler"
        )
        if not os.path.exists(self.inputhandler_save_path):
            os.mkdir(self.inputhandler_save_path)
            if not os.path.exists(self.inputhandler_save_path):
                print(
                    f"failed to make necessary directory:\n{self.inputhandler_save_path}\nexiting."
                )
                sys.exit(1)
        interfaces_path = os.path.join(self.inputhandler_save_path, "interfaces")
        if not os.path.exists(interfaces_path):
            os.mkdir(interfaces_path)
            if not os.path.exists(interfaces_path):
                print(f"failed to make necessary directory:\n{interfaces_path}")
                sys.exit(1)
        session_path = os.path.join(self.inputhandler_save_path, "session")
        if not os.path.exists(session_path):
            os.mkdir(session_path)
            if not os.path.exists(session_path):
                print(f"failed to make necessary directory:\n{session_path}")
                sys.exit(1)
        logs_path = os.path.join(self.inputhandler_save_path, "logs")
        if not os.path.exists(logs_path):
            os.mkdir(logs_path)
            if not os.path.exists(logs_path):
                print(f"failed to make necessary directory:\n{logs_path}")
                sys.exit(1)

        Logger.__init__(self, __name__)

        ScriptCLI.__init__(self)
        args = self.script_cli()

        self.headless = args.headless
        if self.headless:
            self.root_log_handler.info("Generating CLI with supplied arguments")
            sys.exit(0)

        # GUI container
        app = QApplication(sys.argv)
        app.setAttribute(Qt.AA_EnableHighDpiScaling)
        # GUI styling
        app.setStyleSheet(qdarktheme.load_stylesheet())
        self.app = app

        self.root = RootWidget(self)

        HelperMethods.__init__(self)
        NoDialogFileManipulation.__init__(self)
        UserDialogs.__init__(self)
        self.get_app_screen()

        self.root_log_handler.info("CLI gen tool pathing")

        # set lib root path
        self.set_lib_root_path()
        inputhandler_h_path = os.path.join(self.lib_root_path, "src", "InputHandler.h")
        with open(inputhandler_h_path, "r") as file:
            firstline = file.readline()
        file.close()
        if "library version" not in firstline:
            # bad config.h
            self.root_log_handler.warning(
                "this .h file:\n<"
                + str(args.config[0])
                + ">\nis not valid, please enter the full path to a valid InputHandler.h"
            )
            sys.exit(0)
        self.lib_version = (
            firstline.strip()
            .replace("/*", "")
            .replace("*/", "")
            .replace("library version", "")
            .replace(" ", "")
        )

        # setup logger
        self.setup_file_handler()
        self.root_log_handler.addHandler(self.get_file_handler())

        self.root_log_handler.info("Loading CLI generation tool.")
        self.root.import_methods()
        self.window = MainWindow(self.root)  # pass init object to MainWindow
        # exit on user command
        sys.exit(self.app.exec())

    def set_lib_root_path(self):
        file_path = os.getcwd()
        _file_path = QDir(file_path)
        self.file_path = _file_path.toNativeSeparators(_file_path.absolutePath())
        path = QDir(self.file_path)
        self.root_log_handler.info("Path to me: " + str(self.file_path))
        path_dir_list = self.file_path.split(path.separator())
        if not bool(self.file_path.find("InputHandler")):
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
                path.cdUp()
            self.root_log_handler.info(
                "Lib root path: " + str(path.toNativeSeparators(path.absolutePath()))
            )
            self.lib_root_path = path.toNativeSeparators(path.absolutePath())


# end Initialize()


## This is the main display window
#
# MainWindow is the parent of all process subwindows
# (MainWindow is noninteractable when any of its child popups are active except log history)
class MainWindow(
    QMainWindow,
    SettingsTreeMethods,
    CommandParametersMethods,
    CommandTreeMethods,
    PreferencesMethods,
    MainWindowMethods,
    CodeGeneration,
    CLIHelperMethods,
):
    ## The constructor.
    def __init__(
        self,
        parent,
    ):
        super(MainWindow, self).__init__()
        ## app settings
        # settings object; platform independent
        # https://doc.qt.io/qt-6/qsettings.html
        self.settings = QSettings("InputHandler", "cli_gen_tool")

        ## import parent variables, methods, and objects
        self.parent_instance = parent
        self.headless = parent.headless
        self.lib_root_path = self.parent_instance.lib_root_path
        self.create_qdialog = parent.create_qdialog
        self.inputhandler_save_path = parent.inputhandler_save_path

        self.write_cli_gen_tool_json = parent.write_cli_gen_tool_json
        self.write_json = parent.write_json
        self.read_json = parent.read_json
        self.create_file_error_qdialog = parent.create_file_error_qdialog
        self.get_project_dir = parent.get_project_dir
        self.open_file = parent.open_file

        self.get_child_logger = self.parent_instance.get_child_logger

        self.app = parent.app  # QApplication

        # MainWindow logger
        MainWindow.logger = self.get_child_logger(__name__)
        CLIHelperMethods.__init__(self)
        # pathing
        # /InputHandler/src/config/config.h
        default_lib_config_path = QDir(self.lib_root_path + "/src/config/")
        self.default_lib_config_path = default_lib_config_path.toNativeSeparators(
            default_lib_config_path.absoluteFilePath("config.h")
        )

        # /InputHandler/session/cli_gen_tool.json
        cli_gen_tool_json_path = QDir(self.inputhandler_save_path + "/session/")
        self.cli_gen_tool_json_path = cli_gen_tool_json_path.toNativeSeparators(
            cli_gen_tool_json_path.absoluteFilePath("cli_gen_tool.json")
        )

        # objects
        self.qcursor = QCursor()

        ## models
        # generated file min length
        self.minimum_file_len = dataModels.minimum_file_len_dict
        # cli opt db
        self.cliOpt = dataModels.cliopt_model
        # code preview db
        self.code_preview_dict = dataModels.generated_filename_dict
        # default settings dict to regen cli_gen_tool.json if it becomes corrupt or doesnt exist
        self.defaultGuiOpt = dataModels.default_session_model

        # MainWindow state variables
        # ask user if they want to save their work on exit
        self.prompt_to_save = False
        self.windowtitle_set = False
        self.settings_tree_collapsed = False
        self.command_tree_collapsed = False
        self.loading = True
        self.version = version
        self.lib_version = parent.lib_version
        self.qscreen = self.screen()

        self.input_config_file_lines = []
        # the settings that the session started with
        self.default_settings_tree_values = {}
        # session db
        self.session = {}

        # InputHandler builtin user interactable commands
        self.ih_builtins = ["listSettings", "listCommands"]

        self.set_up_main_window(Ui_MainWindow())
        MainWindowMethods.__init__(self)

        self.set_up_session()

        # Splashscreen timer
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.start(
            splashscreen_duration
        )  # Show app splash for `splashscreen_duration`
        self.show_splash()

        self.set_up_log_history_dialog(Ui_logHistoryDialog())

        # preferences dialog
        self.preferences = QDialog(self)
        self.preferences.dlg = Ui_Preferences()
        self.preferences.dlg.setupUi(self.preferences)

        # init and config classes
        self.logger.debug("Importing external classes.")
        SettingsTreeMethods.__init__(self)
        self.get_initial_config_path()
        CommandParametersMethods.__init__(self)
        CommandTreeMethods.__init__(self)
        PreferencesMethods.__init__(self)
        CodeGeneration.__init__(self)

        self.set_up_ui_icons()
        self.cli_generation_dialog_setup(Ui_generateDialog())
        # MainWindow actions
        self.mainwindow_menu_bar_actions_setup()
        self.mainwindow_button_actions_setup()
        # end MainWindow actions

        # settings and command trees
        self.parse_config()
        self.build_code_preview_widgets()
        self.command_tree = self.build_command_tree()
        self.settings_tree = self.build_settings_tree()
        self.command_tree.get_settings_tree()

        self.preferences_dialog_setup()
        self.set_up_command_parameters_dialog(Ui_commandParametersDialog())
        self.display_initial_code_preview()

        # viewports are QAbstractScrollArea, we filter events in them to react to user interaction in specific ways
        self.log.dlg.logHistoryPlainTextEdit.viewport().installEventFilter(self)
        self.settings_tree.viewport().installEventFilter(self)
        self.command_tree.viewport().installEventFilter(self)

        # bring MainWindow in focus
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
        self.logger.info("CLI generation tool ready.")
        self.loading = False
        # end MainWindow.__init__()

    def closeEvent(self, event: QEvent):
        self._closeEvent(event)

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        self._eventFilter(watched, event)
        return super().eventFilter(watched, event)

    def readSettings(self, settings: QSettings):
        self._readSettings(settings)

    @staticmethod
    def restart(self, reason: str) -> None:
        MainWindow.logger.warning("Restarting app; " + reason)
        self.do_before_app_close(None, True)


# end MainWindow


## main function
def main():
    Initialize()


# you can run this script
if __name__ == "__main__":
    main()

# end of file
