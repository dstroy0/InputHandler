##
# @file mainwindow_methods.py
# @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
# @brief MainWindow methods
# @version 1.0
# @date 2022-11-16
# @copyright Copyright (c) 2022
# Copyright (C) 2022 Douglas Quigg (dstroy0) <dquigg123@gmail.com>
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 3 as published by the Free Software Foundation.

from __future__ import absolute_import

from modules.data_models import dataModels
from json import dumps as json_dumps
from PySide6.QtCore import (
    QRegularExpression,
    QEvent,
    QObject,
    QSettings,
    QDir,
    Qt,
    QFile,
)
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import (
    QSplashScreen,
    QDialog,
    QStyle,
    QWidget,
    QDialogButtonBox,
    QFileDialog,
)

# MainWindow methods


class MainWindowMethods(object):
    def __init__(self) -> None:
        super(MainWindowMethods, self).__init__()
        MainWindowMethods.logger = self.get_child_logger(__name__)

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
            MainWindowMethods.logger.info("setting mainwindow title")
            self.windowtitle_set = True

    def _eventFilter(self, watched: QObject, event: QEvent) -> bool:
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
            watched == self.settings_tree.viewport()
            and event_type == QEvent.MouseButtonPress
        ):
            if not self.settings_tree.itemAt(mouse_pos):
                self.settings_tree.clearSelection()
                self.settings_tree.setCurrentItem(self.settings_tree.invisibleRootItem())
                self.settings_tree_button_toggles()
        elif (
            watched == self.command_tree.viewport()
            and event_type == QEvent.MouseButtonPress
        ):
            if not self.command_tree.itemAt(mouse_pos):
                self.command_tree.clearSelection()
                self.command_tree.setCurrentItem(self.command_tree.invisibleRootItem())
                self.command_tree_button_toggles()

    def _closeEvent(self, event: QEvent):
        MainWindowMethods.logger.info("save app states")
        self.settings.setValue("tab", self.ui.tabWidget.currentIndex())
        #self.settings.setValue("command_tree_collapsed", self.command_tree_collapsed)
        #self.settings.setValue("settings_tree_collapsed", self.settings_tree_collapsed)
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())
        self.settings.setValue(
            "settings_tab_splitter", self.ui.settings_tab_splitter.saveState()
        )
        self.settings.setValue(
            "command_tab_splitter", self.ui.command_tab_splitter.saveState()
        )
        self.settings.setValue("command_tree_state", self.command_tree.saveState())
        self.do_before_app_close(event)

    def _readSettings(self, settings: QSettings):
        MainWindowMethods.logger.info("restore app states")
        self.restoreGeometry(settings.value("geometry"))
        self.restoreState(settings.value("windowState"))
        self.ui.settings_tab_splitter.restoreState(
            self.settings.value("settings_tab_splitter")
        )
        self.ui.command_tab_splitter.restoreState(
            self.settings.value("command_tab_splitter")
        )
        if self.settings.value("tab") == None:
            index = 0
        else:
            index = int(self.settings.value("tab"))
        self.ui.tabWidget.setCurrentIndex(index)
        _qscreen = self.screen()
        MainWindowMethods.logger.info("Display name: " + _qscreen.name())

        if self.settings.value("command_tree_state") != None:
            self.command_tree.restoreState(self.settings.value("command_tree_state"))

        #self.command_tree_button_toggles()
        #self.settings_tree_button_toggles()

    def show_splash(self):
        # splashscreen timer
        self.timer = self.parent_instance.timer
        MainWindowMethods.logger.info("load splash")
        self.splash = QSplashScreen(self.qscreen)

        _splash_path = QDir(self.parent_instance.lib_root_path + "/docs/img/")
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

    def set_up_log_history_dialog(self, ui):
        # log history dialog
        self.log = QDialog()
        self.log.setWindowFlags(Qt.Window)
        self.log.setWindowIcon(
            self.get_icon(QStyle.StandardPixmap.SP_FileDialogContentsView)
        )
        self.log.dlg = ui
        # MainWindow still interactable with log history open
        self.log.dlg.setupUi(self.log)
        # ensure log history popup is closed by default
        self.log.close()
        # attach the logging process to the text widget
        self.parent_instance.set_up_window_history_logger(
            self.log.dlg.logHistoryPlainTextEdit
        )

    def set_up_main_window(self, ui):
        # load mainwindow ui
        self.logger.debug("Loading UI_MainWindow()")
        self.ui = ui
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

    def set_up_command_parameters_dialog(self, ui):
        # load command parameters input dialog ui
        self.ui.commandParameters = QDialog(self)
        # blue circle question icon
        self.ui.commandParameters.setWindowIcon(
            self.get_icon(QStyle.StandardPixmap.SP_MessageBoxQuestion)
        )
        self.ui.commandParameters.dlg = ui
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

        self.command_parameters_input_field_settings = (
            dataModels.command_parameters_input_field_settings_dict
        )
        # set input field defaults
        self.set_commandparameters_field_defaults()
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

    def set_up_session(self):
        self.logger.debug("Attempt session json load.")
        # load cli_gen_tool (session) json if exists, else use default options
        self.session = self.load_cli_gen_tool_json(self.cli_gen_tool_json_path)
        # pretty session json
        # session json contains only json serializable items, safe to print
        self.logger.debug(
            "cli_gen_tool.json =\n" + str(json_dumps(self.session, indent=2))
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
            self.cliOpt["commands"]["primary id key"] = "0"
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

    def set_up_ui_icons(self):
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
