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
import qdarktheme
from PySide6.QtCore import (
    QEvent,
    QObject,
    QPoint,
    QSettings,
    Qt,
    QTimer,
    QDir,
    QRegularExpression,
    QFile,
)
from PySide6.QtGui import QCursor, QIcon, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QMainWindow,
    QSplashScreen,
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
from modules.cli.filestrings import CLIfilestrings
from modules.data_models import dataModels
from modules.command_tree import CommandTreeMethods
from modules.code_preview import CodePreview
from modules.command_parameters import CommandParametersMethods
from modules.helper_methods import HelperMethods
from modules.logging_setup import Logger
from modules.mainwindow_actions import MainWindowActions
from modules.mainwindow_buttons import MainWindowButtons
from modules.parse_config import ParseInputHandlerConfig
from modules.settings_tree import SettingsTreeMethods
from modules.settings_tree_table_methods import SettingsTreeTableMethods
from modules.preferences import PreferencesMethods

## tool version
version = 1.0  # save serialization

## The line in /InputHandler/src/config/config.h that boolean define fields start.
config_file_boolean_define_fields_line_start = 72

## How long should the splash be displayed (in ms)
splashscreen_duration = 750


## set up pathing, logging, splash screen
class Initialize(Logger, object):
    def __init__(self) -> None:
        super(Initialize, self).__init__(__name__)

        Logger.__init__(self, __name__)

        # GUI container
        self.app = QApplication(sys.argv)
        self.app.setAttribute(Qt.AA_EnableHighDpiScaling)        
        
        self.root_log_handler.info("CLI gen tool pathing")

        ## Library pathing
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
            # self.logger.info("Dir list: " + str(path_dir_list))
            num_cdup_to_lib_root = 0
            for dirname in reversed(range(len(path_dir_list))):
                if path_dir_list[dirname] == "InputHandler":
                    self.root_log_handler.info(
                        "num dir below InputHandler root: " + str(num_cdup_to_lib_root)
                    )
                    break
                num_cdup_to_lib_root += 1
            self.root_log_handler.info("moving up " + str(num_cdup_to_lib_root) + " dir")
            for i in range(num_cdup_to_lib_root):
                path.cdUp()
            self.root_log_handler.info(
                "Lib root path: " + str(path.toNativeSeparators(path.absolutePath()))
            )
            self.lib_root_path = path.toNativeSeparators(path.absolutePath())
        self.setup_file_handler()
        self.root_log_handler.addHandler(self.get_file_handler())

        # GUI styling
        self.app.setStyleSheet(qdarktheme.load_stylesheet())

        # Splashscreen timer
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.start(
            splashscreen_duration
        )  # Show app splash for `splashscreen_duration`

        self.root_log_handler.info("Loading CLI generation tool.")
        self.window = MainWindow(
            self
        )  # pass init objects to MainWindow, these are used by MainWindow and external subclass methods
        # exit on user command
        sys.exit(self.app.exec())

    def get_inputhandler_dir_from_user(self):
        dir_dlg = QFileDialog(self)
        _dlg_result = dir_dlg.getExistingDirectory(
            self,
            "Open Directory",
            "",
            options=QFileDialog.DontUseNativeDialog
            | QFileDialog.ShowDirsOnly
            | QFileDialog.DontResolveSymlinks,
        )
        if dir_dlg.rejected:
            b = QDialogButtonBox.StandardButton
            buttons = [b.Ok, b.Close]
            button_text = ["Select InputHandler's directory", "Close this tool"]
            result = HelperMethods.create_qdialog(
                self,
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
            if result == QDialog.accept():
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
    SettingsTreeTableMethods,
    HelperMethods,
    MainWindowActions,
    CodePreview,
    SettingsTreeMethods,
    CommandParametersMethods,
    MainWindowButtons,
    ParseInputHandlerConfig,
    CLIfilestrings,
    CommandTreeMethods,
    PreferencesMethods,
):
    ## The constructor.
    def __init__(
        self,        
        parent,
    ):
        super(MainWindow, self).__init__()
        
        self.loading = True
        
        # settings object; platform independent
        # https://doc.qt.io/qt-6/qsettings.html
        self.settings = QSettings("InputHandler", "cli_gen_tool")
        
        self.get_child_logger = parent.get_child_logger
        MainWindow.logger = self.get_child_logger(__name__)

        self.qscreen = self.screen()
        self.timer = parent.timer

        self.windowtitle_set = False

        MainWindow.logger.info("load splash")
        self.splash = QSplashScreen(self.qscreen)

        _splash_path = QDir(parent.lib_root_path + "/docs/img/")
        self.splash.setPixmap(
            QPixmap(
                _splash_path.toNativeSeparators(
                    _splash_path.absoluteFilePath("_Logolarge.png")
                )
            )
        )
        self.splash.showMessage(
            "Copyright (c) 2022 Douglas Quigg (dstroy0) <dquigg123@gmail.com>",
            (Qt.AlignHCenter | Qt.AlignBottom),
            Qt.white,
        )
        self.splash.setWindowFlags(
            self.splash.windowFlags() | Qt.WindowStaysOnTopHint
        )  # or the windowstaysontophint into QSplashScreen window flags
        self.splash.show()
        _fg = self.splash.frameGeometry()
        center_point = self.pos()
        center_point.setX(center_point.x() - (_fg.x() / 2))
        center_point.setY(center_point.y() - (_fg.y() / 2))
        _fg.moveCenter(center_point)
        self.timer.timeout.connect(self.splash.close)  # close splash

        self.version = version
        # input config file boolean define fields (ie // DISABLE_listSettings)
        self.config_file_boolean_define_fields_line_start = (
            config_file_boolean_define_fields_line_start
        )

        # pathing
        self.lib_root_path = parent.lib_root_path
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

        self.app = parent.app  # used in external methods
        # ask user if they want to save their work on exit
        self.prompt_to_save = False

        # log history dialog
        self.log = QDialog()
        self.log.setWindowFlags(Qt.Window)
        self.log.setWindowIcon(
            self.get_icon(QStyle.StandardPixmap.SP_FileDialogContentsView)
        )
        self.log.dlg = Ui_logHistoryDialog()
        # MainWindow still interactable with log history open
        self.log.dlg.setupUi(self.log)
        # ensure log history popup is closed by default
        self.log.close()
        # attach the logging process to the text widget        
        parent.set_up_window_history_logger(self.log.dlg.logHistoryPlainTextEdit)

        # preferences dialog
        self.preferences = QDialog(self)
        self.preferences.dlg = Ui_Preferences()
        self.preferences.dlg.setupUi(self.preferences)

        # import external classes
        self.logger.debug("Importing external classes.")
        CLIfilestrings.__init__(self)
        HelperMethods.__init__(self)
        MainWindowActions.__init__(self)
        MainWindowButtons.__init__(self)
        ParseInputHandlerConfig.__init__(self)
        SettingsTreeMethods.__init__(self)
        SettingsTreeTableMethods.__init__(self)
        CommandParametersMethods.__init__(self)
        CommandTreeMethods.__init__(self)
        CodePreview.__init__(self)

        # load mainwindow ui
        self.logger.debug("Loading UI_MainWindow()")
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.hide()
        # MainWindow icon
        window_icon_path = QDir(self.lib_root_path + "/docs/img/")
        self.setWindowIcon(
            QIcon(
                window_icon_path.toNativeSeparators(
                    window_icon_path.absoluteFilePath("Logolarge.png")
                )
            )
        )

        # load command parameters input dialog ui
        self.ui.commandParameters = QDialog(self)
        # blue circle question icon
        self.ui.commandParameters.setWindowIcon(
            self.get_icon(QStyle.StandardPixmap.SP_MessageBoxQuestion)
        )
        self.ui.commandParameters.dlg = Ui_commandParametersDialog()
        self.ui.commandParameters.dlg.setupUi(self.ui.commandParameters)
        self.ui.commandParameters.setMaximumSize(0, 0)
        self.ui.commandParameters.dlg.argumentsPlainTextCSV.clear()
        self.ui.commandParameters.dlg.argumentsPlainTextCSV.setPlaceholderText(
            "Enter your argument types in order, separated by a comma."
        )

        # CommandParameters user input objects
        self.command_parameters_user_input_objects = {
            # line edit
            "returnFunctionName": self.ui.commandParameters.dlg.returnFunctionName,
            # line edit
            "commandString": self.ui.commandParameters.dlg.commandString,
            # read only label
            "commandLength": self.ui.commandParameters.dlg.commandLengthLabel,
            # line edit
            "parentId": self.ui.commandParameters.dlg.commandParentId,
            # line edit
            "commandId": self.ui.commandParameters.dlg.commandId,
            # check box
            "commandHasWildcards": self.ui.commandParameters.dlg.commandHasWildcards,
            # spinbox
            "commandDepth": self.ui.commandParameters.dlg.commandDepth,
            # spinbox
            "commandSubcommands": self.ui.commandParameters.dlg.commandSubcommands,
            # combobox
            "commandArgumentHandling": self.ui.commandParameters.dlg.commandArgumentHandling,
            # spinbox
            "commandMinArgs": self.ui.commandParameters.dlg.commandMinArgs,
            # spinbox
            "commandMaxArgs": self.ui.commandParameters.dlg.commandMaxArgs,
            # plain text edit
            "commandArguments": self.ui.commandParameters.dlg.argumentsPlainTextCSV,
        }

        # MainWindow var
        self.adding_child_command = False
        self.child_command_parent = None
        self.selected_command = None  # currently selected editable command or None
        self.selected_command_is_root = (
            False  # root commands one level below the root tree item
        )
        self.command_parameters_input_field_settings = (
            dataModels.command_parameters_input_field_settings_dict
        )
        # set input field defaults
        self.set_commandparameters_field_defaults()

        #
        self.default_settings_tree_values = {}

        # InputHandler builtin user interactable commands
        self.ih_builtins = ["listSettings", "listCommands"]

        # code preview interaction
        self.user_resizing_code_preview_box = False
        self.init_mouse_pos = QPoint()
        self.init_height = 0
        self.qcursor = QCursor()

        # cli opt db
        self.cliOpt = dataModels.cliopt_model
        # code preview db
        self.code_preview_dict = dataModels.generated_filename_dict

        # default settings dict to regen cli_gen_tool.json if it becomes corrupt
        self.defaultGuiOpt = dataModels.default_session_model
        # session db
        self.session = {}
        self.logger.debug("Attempt session json load.")

        # icons
        self.ui.fileDialogContentsViewIcon = self.get_icon(
            QStyle.StandardPixmap.SP_FileDialogContentsView
        )
        self.ui.messageBoxCriticalIcon = self.get_icon(
            QStyle.StandardPixmap.SP_MessageBoxCritical
        )
        self.ui.fileIcon = self.get_icon(QStyle.StandardPixmap.SP_FileIcon)
        self.ui.commandLinkIcon = self.get_icon(QStyle.StandardPixmap.SP_CommandLink)
        self.ui.trashIcon = self.get_icon(QStyle.StandardPixmap.SP_TrashIcon)
        self.ui.messageBoxQuestionIcon = self.get_icon(
            QStyle.StandardPixmap.SP_MessageBoxQuestion
        )

        # load cli_gen_tool (session) json if exists, else use default options
        self.session = self.load_cli_gen_tool_json(self.cli_gen_tool_json_path)
        # pretty session json
        # session json contains only json serializable items, safe to print
        self.logger.debug(
            "cli_gen_tool.json =\n" + str(json.dumps(self.session, indent=2))
        )
        last_interface = QFile()
        if self.session["opt"]["save_filename"] is not None:
            last_interface_path = QDir(self.session["opt"]["save_filename"])
            self.logger.debug("Attempt load last interface")
            last_interface = QFile(
                last_interface_path.toNativeSeparators(
                    last_interface_path.absolutePath()
                )
            )
        if self.session["opt"]["save_filename"] != "" and last_interface.exists():
            result = self.read_json(last_interface, True)
            self.cliOpt = result[1]
        elif self.session["opt"]["save_filename"] != "" and not last_interface.exists():
            b = QDialogButtonBox.StandardButton
            buttons = [b.Ok, b.Cancel]
            button_text = ["Select last file", "Continue without locating"]
            result = self.create_qdialog(
                "Cannot locate last working file: " + str(last_interface.fileName()),
                Qt.AlignCenter,
                Qt.NoTextInteraction,
                "Error, cannot find interface file!",
                buttons,
                button_text,
                QIcon(
                    QWidget()
                    .style()
                    .standardIcon(QStyle.StandardPixmap.SP_MessageBoxCritical)
                ),
            )
            if result == QDialog.Accepted:
                dlg = QFileDialog(self)
                result = dlg.getOpenFileName(
                    self,
                    "Locate: " + last_interface.fileName(),
                    last_interface_path.toNativeSeparators(
                        last_interface_path.absoluteFilePath(last_interface.fileName())
                    ),
                    "*.json",
                    options=QFileDialog.DontUseNativeDialog,
                )
                if result == QFileDialog.rejected:
                    self.logger.info(
                        "User couldn't locate last working file, continuing."
                    )
            else:
                self.logger.info(
                    "Couldn't locate last working file: "
                    + str(self.session["opt"]["save_filename"])
                )
                self.session["opt"]["save_filename"] = ""

                self.set_main_window_title("InputHandler CLI generation tool ")
        # parse config file
        self.logger.debug("Attempt parse config.h")
        self.parse_config_header_file(self.session["opt"]["input_config_file_path"])

        # end MainWindow var

        # MainWindow actions
        self.mainwindow_menu_bar_actions_setup()
        self.mainwindow_button_actions_setup()
        # end MainWindow actions

        # tab 1
        # settings_tree widget setup
        self.build_lib_settings_tree()

        # code preview trees
        self.minimum_file_len = dataModels.minimum_file_len_dict
        self.build_code_preview_tree()
        self.display_initial_code_preview()

        # uncomment to print self.cliOpt as pretty json
        # print(json.dumps(self.cliOpt, indent=4, sort_keys=False, default=lambda o: 'object'))

        # tab 2
        # command_tree widget setup
        self.build_command_tree()
        # command parameters dialog box setup
        cmd_dlg = self.ui.commandParameters.dlg
        # This dict contains regexp strings and int limits for user input
        # the values are placeholder values and will change on user interaction
        cmd_dlg.validatorDict = {
            "returnFunctionName": "^([a-zA-Z_])+$",
            "commandString": "^([a-zA-Z_*])+$",
            "commandParentId": "^([0-9])+$",
            "commandId": "^([0-9])+$",
            "commandDepth": 255,
            "commandSubcommands": 255,
            "commandMinArgs": 255,
            "commandMaxArgs": 255,
        }
        # set validators to user preset or defaults
        self.set_command_parameter_validators()
        # user interaction triggers
        self.set_command_parameters_triggers()
        # argumentsPane QWidget is automatically enabled/disabled with the setting of the arguments handling combobox
        # set False by default
        cmd_dlg.argumentsPane.setEnabled(False)

        # viewports are QAbstractScrollArea, we filter events in them to react to user interaction in specific ways
        self.log.dlg.logHistoryPlainTextEdit.viewport().installEventFilter(self)
        self.ui.codePreview_1.viewport().installEventFilter(self)
        self.ui.codePreview_2.viewport().installEventFilter(self)
        self.ui.settings_tree.viewport().installEventFilter(self)
        self.ui.command_tree.viewport().installEventFilter(self)

        # load preferences
        PreferencesMethods.__init__(self)
        self.preferences_dialog_setup()
        # close splash and show app
        self.splash.close()
        self.readSettings(self.settings)
        self.show()
        self.logger.info("CLI generation tool ready.")
        self.loading = False
        # end MainWindow.__init__()

    # visual indication to user of the current working file
    def set_main_window_title(self, title: str = None) -> None:
        if self.windowtitle_set:
            return
        elif title != None:
            self.setWindowTitle(title)
            self.windowtitle_set = True
            return
        else:
            windowtitle = "InputHandler CLI generation tool "
            if self.prompt_to_save == True:
                windowtitle = windowtitle + " - *"
            else:
                windowtitle = windowtitle + " - "
            if self.session["opt"]["save_filename"]:
                regexp = QRegularExpression("[^\/]*$")
                match = regexp.match(str(self.session["opt"]["save_filename"]))
                if match.hasMatch():
                    windowtitle = windowtitle + str(match.captured(0))
            else:
                windowtitle = windowtitle + "untitled"
            self.setWindowTitle(windowtitle)
            self.windowtitle_set = True

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        # event_type to avoid repetitive calls to .type() method; events are granular.

        # sets main window title
        self.set_main_window_title()

        event_type = event.type()
        # mouse button click sentinel
        mouse_button = False
        # global mouse pos
        mouse_pos = self.qcursor.pos()
        # drag to resize, change cursor to vertical drag and back to arrow
        if (
            watched == self.ui.codePreview_1.viewport()
            or watched == self.ui.codePreview_2.viewport()
        ):
            self.code_preview_events(
                watched, event, event_type, mouse_button, mouse_pos
            )
        elif (
            watched == self.ui.settings_tree.viewport()
            and event_type == QEvent.MouseButtonPress
        ):
            if not self.ui.settings_tree.itemAt(mouse_pos):
                self.ui.settings_tree.clearSelection()
        elif (
            watched == self.ui.command_tree.viewport()
            and event_type == QEvent.MouseButtonPress
        ):
            if not self.ui.command_tree.itemAt(mouse_pos):
                self.ui.command_tree.clearSelection()
                self.ui.command_tree.setCurrentItem(
                    self.cliOpt["commands"]["QTreeWidgetItem"]["root"]
                )
                self.command_menu_button_toggles()
        return super().eventFilter(watched, event)

    def closeEvent(self, event):
        MainWindow.logger.info("save window settings")
        self.settings.setValue("tab", self.ui.tabWidget.currentIndex())
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())
        self.do_before_app_close(event)

    def readSettings(self, settings: QSettings):
        MainWindow.logger.info("restore window settings")
        self.restoreGeometry(settings.value("geometry"))
        self.restoreState(settings.value("windowState"))
        if self.settings.value("tab") == None:
            index = 0
        else:
            index = int(self.settings.value("tab"))
        self.ui.tabWidget.setCurrentIndex(index)
        _qscreen = self.screen()
        MainWindow.logger.info("Display name: " + _qscreen.name())

    @staticmethod
    def restart():
        MainWindow.singleton = MainWindow()


# end MainWindow

## main function
def main():
    Initialize()


# you can run this script
if __name__ == "__main__":
    main()

# end of file
