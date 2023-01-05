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
import json
import pathlib
import argparse
import qdarktheme
from PySide6.QtCore import (
    QEvent,
    QObject,
    QSettings,
    Qt,
    QTimer,
    QDir,
)
from PySide6.QtGui import QCursor, QIcon
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
from modules.uic.preferencesDialog import Ui_Preferences
from modules.uic.commandParametersDialog import (
    Ui_commandParametersDialog,
)  # tab two popup dialog box
from modules.uic.logHistoryDialog import Ui_logHistoryDialog
from modules.uic.mainWindow import Ui_MainWindow  # main window with tabs

# external class methods
from modules.data_models import dataModels
from modules.command_tree import CommandTreeMethods
from modules.command_parameters import CommandParametersMethods
from modules.helper_methods import HelperMethods
from modules.logging_setup import Logger
from modules.settings_tree import SettingsTreeMethods
from modules.preferences import PreferencesMethods
from modules.mainwindow_methods import MainWindowMethods
from modules.code_generation import CodeGeneration

## tool version
version = 1.0  # save serialization

## The line in /InputHandler/src/config/config.h that boolean define fields start.
config_file_boolean_define_fields_line_start = 72

## How long should the splash be displayed (in ms)
splashscreen_duration = 750


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

        self.root_log_handler = self._parent.root_log_handler
        self.setup_file_handler = self._parent.setup_file_handler
        self.get_child_logger = self._parent.get_child_logger
        self.set_up_window_history_logger = self._parent.set_up_window_history_logger
        self.logger = self.root_log_handler

        self.get_inputhandler_dir_from_user = (
            self._parent.get_inputhandler_dir_from_user
        )
        self.lib_root_path = self._parent.lib_root_path
        self.headless = self._parent.headless
        self.lib_version = self._parent.lib_version


## set up pathing, logging, splash screen
class Initialize(HelperMethods, Logger, object):
    def __init__(self) -> None:
        super(Initialize, self).__init__()
        Logger.__init__(self, __name__)

        # cli_gen_tool script command line interface
        self.parser = argparse.ArgumentParser(
            prog=os.path.basename(__file__),
            description="generate a CLI in target directory",
        )
        self.parser.add_argument(
            "-g",
            "--generate",
            nargs=2,
            type=pathlib.Path,
            required=False,
            help="-g <dest dir> <path to cli options json> generates a CLI",
            metavar="",
        )
        self.parser.add_argument(
            "-s",
            "--session",
            nargs=1,
            type=pathlib.Path,
            required=False,
            help="-s <path to session json> path to alternate session file",
            metavar="",
        )
        self.parser.add_argument(
            "-c",
            "--config",
            nargs=1,
            type=pathlib.Path,
            required=False,
            help="-c <path to Inputhandler config.h> path to alternate config file",
            metavar="",
        )
        args = self.parser.parse_args(sys.argv[1:])

        # script cli only (no gui) when true
        self.headless = False
        # validate argparser input further
        if bool(args.generate):
            self.headless = True
            self.root_log_handler.info("output path: " + str(args.generate[0]))
            self.root_log_handler.info("cli options path: " + str(args.generate[1]))
            if not os.path.exists(str(args.generate[0])):
                self.root_log_handler.warning(
                    "the selected output directory:\n<"
                    + str(args.generate[0])
                    + ">\ndoes not exist, please enter the full path to the output directory"
                )
                sys.exit(0)
            if ".json" not in str(args.generate[1]):
                # no cliopt json
                self.root_log_handler.warning(
                    "invalid path:\n<"
                    + str(args.generate[1])
                    + ">\nplease enter the full path to the cli options json"
                )
                sys.exit(0)
            try:
                with open(str(args.generate[1]), "r") as file:
                    filedata = file.read()
                file.close()
            except Exception as e:
                self.root_log_handler.warning(
                    "cannot open:\n<"
                    + str(args.generate[1])
                    + ">\nmsg: "
                    + str(e.message)
                    + "\nargs: "
                    + str(e.args)
                )
                sys.exit(0)
            try:
                filedata = json.loads(filedata)
            except:
                # bad json
                self.root_log_handler.warning(
                    "this json:\n<"
                    + str(args.generate[1])
                    + ">\nis not valid, please enter the full path to a valid cli options json"
                )
                sys.exit(0)
            if filedata["type"] != "cli options":
                # wrong json
                self.root_log_handler.warning(
                    "this json:\n<"
                    + str(args.generate[1])
                    + ">\nis not a cli options json, please enter the full path to a valid cli options json"
                )
                sys.exit(0)

        if bool(args.session):
            self.root_log_handler.info("session json path: " + str(args.session[0]))
            if ".json" not in str(args.session[0]):
                # no session json
                self.root_log_handler.warning(
                    "this path:\n<"
                    + str(args.session[0])
                    + ">\nis not valid, please enter the full path to a session json"
                )
                sys.exit(0)
            try:
                with open(str(args.session[0]), "r") as file:
                    filedata = file.read()
                file.close()
            except Exception as e:
                self.root_log_handler.warning(
                    "cannot open:\n<"
                    + str(args.generate[1])
                    + ">\nmsg: "
                    + str(e.message)
                    + "\nargs: "
                    + str(e.args)
                )
                sys.exit(0)
            try:
                filedata = json.loads(filedata)
            except:
                # bad json
                self.root_log_handler.warning(
                    "this json:\n<"
                    + str(args.session[0])
                    + ">\nis not valid, please enter the full path to a valid cli options json"
                )
                sys.exit(0)
            if filedata["type"] != "session":
                # wrong json
                self.root_log_handler.warning(
                    "this json:\n<"
                    + str(args.session[0])
                    + ">\nis not a session json please enter the full path to a valid session json"
                )
                sys.exit(0)

        if bool(args.config):
            self.root_log_handler.info(
                "InputHandler config.h path:\n<" + str(args.config[0]) + ">"
            )
            if ".h" not in str(args.config[0]):
                # no config.h
                self.root_log_handler.warning(
                    "please enter the full path to an InputHandler config.h"
                )
                sys.exit(0)
            try:
                with open(str(args.config[0]), "r") as file:
                    filedata = file.read()
                file.close()
            except Exception as e:
                self.root_log_handler.warning(
                    "cannot open:\n<"
                    + str(args.generate[1])
                    + ">\nmsg: "
                    + str(e.message)
                    + "\nargs: "
                    + str(e.args)
                )
                sys.exit(0)
            if "#if !defined(__INPUTHANDLER_CONFIG_H__)" not in filedata:
                # bad config.h
                self.root_log_handler.warning(
                    "this .h file:\n<"
                    + str(args.config[0])
                    + ">\nis not valid, please enter the full path to a valid InputHandler config.h"
                )
                sys.exit(0)

        # GUI container
        app = QApplication(sys.argv)
        app.setAttribute(Qt.AA_EnableHighDpiScaling)
        # GUI styling
        app.setStyleSheet(qdarktheme.load_stylesheet())
        self.app = app

        self.root = RootWidget(self)

        HelperMethods.__init__(self)

        if self.headless:
            self.root_log_handler.info("Generating CLI with supplied arguments")
            sys.exit(0)

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
        file_path = os.path.abspath(__file__)
        _file_path = QDir(file_path)
        self.file_path = _file_path.toNativeSeparators(_file_path.absolutePath())
        path = QDir(self.file_path)
        self.root_log_handler.info("Path to me: " + str(self.file_path))
        path_dir_list = self.file_path.split(path.separator())
        if "InputHandler" not in path_dir_list:
            # prompt user for lib dir
            self.get_inputhandler_dir_from_user()
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
                QIcon(
                    QWidget()
                    .style()
                    .standardIcon(QStyle.StandardPixmap.SP_MessageBoxCritical)
                ),
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

        self.get_child_logger = self.parent_instance.get_child_logger

        self.app = parent.app  # QApplication

        # MainWindow logger
        MainWindow.logger = self.get_child_logger(__name__)

        # pathing
        # /InputHandler/src/config/config.h
        default_lib_config_path = QDir(self.lib_root_path + "/src/config/")
        self.default_lib_config_path = default_lib_config_path.toNativeSeparators(
            default_lib_config_path.absoluteFilePath("config.h")
        )

        # /InputHandler/cli_gen_tool/cli_gen_tool.json
        cli_gen_tool_json_path = QDir(self.lib_root_path + "/tools/session/")
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
        # input config file boolean define fields (ie // DISABLE_listSettings)
        self.config_file_boolean_define_fields_line_start = (
            config_file_boolean_define_fields_line_start
        )
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

        if not self.headless:
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

        # bring MainWindow to front, even after a restart
        # close splash and show app
        # self.splash.close()
        self.setWindowState(Qt.WindowActive)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        # self.show()
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
        # self.show()

        self.logger.info("CLI generation tool ready.")
        self.loading = False
        if self.headless:
            # self.generate_cli(self.cli_project_path)
            self.logger.info("finished, exiting")
            sys.exit()
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
