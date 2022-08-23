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
import sys
import json
import qdarktheme
from PySide6.QtCore import QEvent, QObject, QPoint, QSettings, Qt, QTimer, QDir
from PySide6.QtGui import QCursor, QIcon, QPixmap
from PySide6.QtWidgets import QApplication, QDialog, QMainWindow, QSplashScreen, QStyle

# import classes generated by PySide6 uic
from res.uic.preferencesDialog import Ui_Preferences
from res.uic.commandParametersDialog import (
    Ui_commandParametersDialog,
)  # tab two popup dialog box
from res.uic.logHistoryDialog import Ui_logHistoryDialog
from res.uic.mainWindow import Ui_MainWindow  # main window with tabs

# external class methods
from res.modules.cli.filestrings import CLIfilestrings
from res.modules.data_models import dataModels
from res.modules.command_tree import CommandTreeMethods
from res.modules.code_preview import CodePreview
from res.modules.command_parameters import CommandParametersMethods
from res.modules.helper_methods import HelperMethods
from res.modules.logging_setup import Logger
from res.modules.mainwindow_actions import MainWindowActions
from res.modules.mainwindow_buttons import MainWindowButtons
from res.modules.parse_config import ParseInputHandlerConfig
from res.modules.settings_tree import SettingsTreeMethods
from res.modules.settings_tree_table_methods import SettingsTreeTableMethods
from res.modules.preferences import PreferencesMethods

## tool version
version = 1.0  # save serialization

## The line in /InputHandler/src/config/config.h that boolean define fields start.
config_file_boolean_define_fields_line_start = 71

## How long should the splash be displayed (in ms)
splashscreen_duration = 750

## Library pathing
path = QDir()
path.cdUp()
lib_root_path = path.currentPath()

## This is the main display window
#
# MainWindow is the parent of all process subwindows
# (MainWindow is noninteractable when any of its child popups are active)
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
    def __init__(self, app, parent=None):
        super().__init__(parent)
        # tool version
        self.version = version
        # input config file boolean define fields (ie // DISABLE_listSettings)
        self.config_file_boolean_define_fields_line_start = (
            config_file_boolean_define_fields_line_start
        )
        # pathing
        self.lib_root_path = lib_root_path
        # /InputHandler/src/config/config.h
        self.default_lib_config_path = self.lib_root_path + "/src/config/config.h"
        # /InputHandler/cli_gen_tool/cli_gen_tool.json
        self.cli_gen_tool_json_path = (
            self.lib_root_path + "/cli_gen_tool/cli_gen_tool.json"
        )
        # settings object; platform independent
        # https://doc.qt.io/qt-6/qsettings.html
        self.settings = QSettings("InputHandler", "cli_gen_tool.py")
        self.app = app  # used in external methods
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

        # preferences dialog
        self.preferences = QDialog(self)
        self.preferences.dlg = Ui_Preferences()
        self.preferences.dlg.setupUi(self.preferences)

        # set up logging api
        Logger.setup_file_handler(self.lib_root_path)
        self.logger = Logger.get_logger(self, __name__)
        self.logger.debug("App pathing set.")
        self.logger.info("Loading CLI generation tool.")

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
        PreferencesMethods.__init__(self)

        # load mainwindow ui
        self.logger.debug("Loading UI_MainWindow()")
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # MainWindow icon
        window_icon_path = self.lib_root_path + "/docs/img/Logolarge.png"
        self.setWindowIcon(QIcon(window_icon_path))

        # load command parameters input dialog ui
        self.ui.commandParameters = QDialog(self)
        # blue circle question icon
        self.ui.commandParameters.setWindowIcon(
            self.get_icon(QStyle.StandardPixmap.SP_MessageBoxQuestion)
        )
        self.ui.commandParameters.dlg = Ui_commandParametersDialog()
        self.ui.commandParameters.dlg.setupUi(self.ui.commandParameters)
        self.ui.commandParameters.setMaximumSize(0, 0)

        # MainWindow var
        self.default_settings_tree_values = {}

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
        # load cli_gen_tool (session) json if exists, else use default options
        self.session = self.load_cli_gen_tool_json(self.cli_gen_tool_json_path)
        # pretty session json
        # session json contains only json serializable items, safe to print
        self.logger.debug(
            "cli_gen_tool.json =\n" + str(json.dumps(self.session, indent=2))
        )

        # parse config file
        self.logger.debug("Attempt parse config.h")
        self.parse_config_header_file(self.session["opt"]["input_config_file_path"])

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
        # end MainWindow var

        # MainWindow actions
        self.mainwindow_menu_bar_actions_setup()
        self.mainwindow_button_actions_setup()
        # end MainWindow actions

        # tab 1
        # settings_tree widget setup
        self.build_lib_settings_tree()

        # code preview trees
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
            "functionName": "^([a-zA-Z_])+$",
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

        # viewports are "QAbstractScrollArea"s; we filter events in them to react to user interaction in specific ways
        self.log.dlg.logHistoryPlainTextEdit.viewport().installEventFilter(self)
        self.ui.codePreview_1.viewport().installEventFilter(self)
        self.ui.codePreview_2.viewport().installEventFilter(self)

        # end MainWindow objects
        # read QSettings
        self.readSettings(self.settings)
        self.logger.info("CLI generation tool ready.")
        # end __init__

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        # event_type to avoid repetitive calls to .type() method; events are granular.
        event_type = event.type()
        # mouse button click sentinel
        mouse_button = False
        # global mouse pos
        mouse_pos = self.qcursor.pos()
        # drag to resize, change cursor to vertical drag and back to arrow
        self.code_preview_events(watched, event, event_type, mouse_button, mouse_pos)
        return super().eventFilter(watched, event)

    def closeEvent(self, event):
        MainWindow.logger.info("save window settings")
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())
        self.do_before_app_close(event)

    def readSettings(self, settings: QSettings):
        MainWindow.logger.info("restore window settings")
        self.restoreGeometry(settings.value("geometry"))
        self.restoreState(settings.value("windowState"))


## main function
def main():
    # GUI container
    app = QApplication(sys.argv)
    # GUI styling
    app.setStyleSheet(qdarktheme.load_stylesheet())
    # app splashscreen
    splash = QSplashScreen()
    splash.setPixmap(QPixmap(lib_root_path + "/docs/img/_Logolarge.png"))
    splash.showMessage(
        "Copyright (c) 2022 Douglas Quigg (dstroy0) <dquigg123@gmail.com>",
        (Qt.AlignHCenter | Qt.AlignBottom),
        Qt.white,
    )
    splash.setWindowFlags(
        splash.windowFlags() | Qt.WindowStaysOnTopHint
    )  # or the windowstaysontophint into QSplashScreen window flags
    splash.show()

    # GUI layout
    window = MainWindow(app)  # pass app object to external methods

    # Splashscreen timer
    splash.timer = QTimer()
    splash.timer.setSingleShot(True)
    splash.timer.start(
        splashscreen_duration
    )  # Show app splash for `splashscreen_duration`
    splash.timer.timeout.connect(splash.close)  # close splash
    splash.timer.timeout.connect(window.show)  # show window to user

    # exit on user command
    sys.exit(app.exec())


# you can run this script
if __name__ == "__main__":
    main()

# end of file
