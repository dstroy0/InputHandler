##
# @file mainwindow.py
# @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
# @brief app mainwindow
# @version 1.0.0
# @date 2023-05-22
# @copyright Copyright (c) 2023
# Copyright (C) 2023 Douglas Quigg (dstroy0) <dquigg123@gmail.com>
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 3 as published by the Free Software Foundation.

from __future__ import absolute_import
import os
import sys
import copy
import platform
from PySide6.QtCore import (
    QEvent,
    QObject,
    QSettings,
    Qt,
    QTimer,
    QDir,
    QRegularExpression,
    QFile,
)
from PySide6.QtGui import QCursor, QPixmap, QIcon, QAction
from PySide6.QtWidgets import (
    QDialog,
    QMainWindow,
    QSplashScreen,
    QStyle,
    QWidget,
    QDialogButtonBox,
    QFileDialog,
    QTableView,
    QComboBox,
    QTreeWidget,
    QMenu,
)
from modules.uic.preferencesDialog import Ui_Preferences
from modules.uic.commandParametersDialog import Ui_commandParametersDialog
from modules.uic.logHistoryDialog import Ui_logHistoryDialog
from modules.uic.mainWindow import Ui_MainWindow
from modules.uic.generateCLIDialog import Ui_generateDialog
from modules.data_models import DataModels
from modules.command_tree import CommandTree
from modules.command_parameters_dialog import CommandParametersDialog
from modules.settings_tree import SettingsTree
from modules.preferences_dialog import PreferencesDialog
from modules.code_display import CodeDisplay
from modules.cli.cli_helper_methods import CLIHelperMethods
from modules.pathing import Pathing
from modules.logger import Logger
from modules.user_dialogs import UserDialogs
from modules.file_manipulation import FileManipulation


## This is the main display window
#
# MainWindow is the parent of all process subwindows
# (MainWindow is noninteractable when any of its child popups are active except log history)
class MainWindow(
    QMainWindow,
    Pathing,
    Logger,
    UserDialogs,
    FileManipulation,
    SettingsTree,
    CommandParametersDialog,
    CommandTree,
    PreferencesDialog,
    CodeDisplay,
    CLIHelperMethods,
):
    ## The constructor.
    def __init__(self, parent):
        super().__init__()
        ## app settings
        # settings object; platform independent
        # https://doc.qt.io/qt-6/qsettings.html
        self.settings = QSettings("InputHandler", "cli_gen_tool")

        self.prev_command_tree_state = 0
        self.prev_settings_tree_state = 0

        ## import parent variables, methods, and objects
        self.parent_instance = parent
        # self.set_up_session = self.parent_instance.set_up_session
        self.lib_root_path = self.parent_instance.lib_root_path
        # self.create_qdialog = parent.create_qdialog
        # self.inputhandler_save_path = parent.inputhandler_save_path

        # self.write_cli_gen_tool_json = parent.write_cli_gen_tool_json
        # self.write_json = parent.write_json
        # self.read_json = parent.read_json
        # self.create_file_error_qdialog = parent.create_file_error_qdialog
        # self.get_project_dir = parent.get_project_dir
        # self.open_file = parent.open_file

        # self.get_child_logger = self.parent_instance.get_child_logger

        self.app = parent.app  # QApplication

        # MainWindow logger
        MainWindow.logger = self.get_child_logger(__name__)
        CLIHelperMethods.__init__(self)

        # objects
        self.qcursor = QCursor()

        ## models
        # generated file min length
        self.minimum_file_len = DataModels.minimum_file_len_dict
        # cli opt db
        self.cli_options = DataModels.cliopt_model
        # code preview db
        self.code_preview_dict = DataModels.generated_filename_dict
        # default settings dict to regen cli_gen_tool.json if it becomes corrupt or doesnt exist
        self.defaultGuiOpt = DataModels.default_session_model

        # MainWindow state variables
        # ask user if they want to save their work on exit
        self.prompt_to_save = False
        self.windowtitle_set = False
        self.settings_tree_collapsed = False
        self.command_tree_collapsed = False
        self.loading = True
        # self.version = self.parent_instance.version
        # self.lib_version = parent.lib_version
        self.qscreen = self.screen()

        self.input_config_file_lines = []
        # the settings that the session started with
        self.default_settings_tree_values = {}
        # session db
        self.session = {}

        # InputHandler builtin user interactable commands
        self.ih_builtins = ["listSettings", "listCommands"]

        self.set_up_main_window(Ui_MainWindow())

        self.set_up_session()

        # Splashscreen timer
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.start(
            self.parent_instance.splashscreen_duration
        )  # Show app splash for `splashscreen_duration`
        self.show_splash()

        self.set_up_log_history_dialog(Ui_logHistoryDialog())

        # preferences dialog
        self.preferences = QDialog(self)
        self.preferences.dlg = Ui_Preferences()
        self.preferences.dlg.setupUi(self.preferences)

        # init and config classes
        self.logger.debug("Importing external classes.")
        SettingsTree.__init__(self)
        self.get_initial_config_path()
        CommandParametersDialog.__init__(self)
        CommandTree.__init__(self)
        PreferencesDialog.__init__(self)
        CodeDisplay.__init__(self)

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

    @staticmethod
    def restart(self, reason: str) -> None:
        MainWindow.logger.warning(f"Restarting app; {reason}")
        self.do_before_app_close(None, True)

    # visual indication to user of the current working file
    def set_main_window_title(self, title: str = None) -> None:
        """sets mainwindow title for save status and working filename

        Args:
            title (str, optional): the text to set. Defaults to None.
        """
        if self.windowtitle_set:
            return
        elif title != None:
            self.setWindowTitle(title)
            self.windowtitle_set = True
            return
        else:
            windowtitle = "InputHandler CLI generation tool "
            if self.prompt_to_save == True:
                windowtitle = f"{windowtitle} - *"
            else:
                windowtitle = f"{windowtitle} - "
            if self.session["opt"]["save_file_path"]:
                regexp = QRegularExpression("[^\/]*$")
                match = regexp.match(str(self.session["opt"]["save_file_path"]))
                if match.hasMatch():
                    windowtitle = f"{windowtitle} {str(match.captured(0))}"
            else:
                windowtitle = f"{windowtitle} untitled"
            MainWindow.logger.debug("setting mainwindow title")
            self.setWindowTitle(windowtitle)
            self.windowtitle_set = True

    def eventFilter(self, watched: QObject, event: QEvent):
        """MainWindow event filter

        Args:
            watched (QObject): object where trigger happened
            event (QEvent): what happened

        Returns:
            bool: None
        """
        # sets main window title
        self.set_main_window_title()

        event_type = event.type()
        # mouse button click sentinel
        mouse_button = False
        # global mouse pos
        mouse_pos = self.qcursor.pos()
        if (
            watched == self.settings_tree.viewport()
            and event_type == QEvent.MouseButtonPress
        ):
            if not self.settings_tree.itemAt(mouse_pos):
                self.settings_tree.clearSelection()
                self.settings_tree.setCurrentItem(
                    self.settings_tree.invisibleRootItem()
                )
                self.settings_tree_button_toggles()
        elif (
            watched == self.command_tree.viewport()
            and event_type == QEvent.MouseButtonPress
        ):
            if not self.command_tree.itemAt(mouse_pos):
                self.command_tree.clearSelection()
                self.command_tree.setCurrentItem(self.command_tree.invisibleRootItem())
                self.command_tree_button_toggles()
        return super(MainWindow, self).eventFilter(watched, event)

    def closeEvent(self, event: QEvent):
        """do these things on app close

        Args:
            event (QEvent): closeEvent type
        """
        MainWindow.logger.info("save app states")
        self.settings.setValue("tab", self.ui.tabWidget.currentIndex())

        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())
        self.settings.setValue(
            "settings_tab_splitter", self.ui.settings_tab_splitter.saveState()
        )
        self.settings.setValue(
            "command_tab_splitter", self.ui.command_tab_splitter.saveState()
        )
        self.settings.setValue("command_tree_state", self.command_tree.saveState())
        self.settings.setValue("settings_tree_state", self.settings_tree.saveState())
        self.do_before_app_close(event)

    def readSettings(self, settings: QSettings):
        """reats QSettings

        Args:
            settings (QSettings): app settings
        """
        MainWindow.logger.info("restore app states")
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
        MainWindow.logger.info(f"Display name: {_qscreen.name()}")

        if self.settings.value("command_tree_state") != None:
            self.command_tree.restoreState(self.settings.value("command_tree_state"))
        else:
            self.ui.command_tree_collapse_button.setText("Expand All")
        if self.settings.value("settings_tree_state") != None:
            self.settings_tree.restoreState(self.settings.value("settings_tree_state"))
        else:
            self.ui.settings_tree_collapse_button.setText("Expand All")

        self.command_tree_button_toggles()
        self.settings_tree_button_toggles()

    def get_initial_config_path(self):
        """get initial path to config"""
        self.old_path = os.path.abspath(
            os.path.join(self.session_path, "cli_gen_tool.json")
        )

    def show_splash(self):
        """shows app splashscreen if applicable"""
        MainWindow.logger.info("load splash")
        self.splash = QSplashScreen(self.qscreen)

        _splash_path = QDir(f"{self.lib_root_path}/docs/img/")
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
        self.timer.timeout.connect(self.show)
        self.timer.timeout.connect(
            lambda settings=self.settings: self.readSettings(settings)
        )
        # bring MainWindow to front, even after a restart
        # close splash and show app
        self.timer.timeout.connect(self.setWindowState(Qt.WindowActive))
        self.timer.timeout.connect(
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        )
        self.timer.timeout.connect(
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
        )

    def set_up_log_history_dialog(self, ui):
        """sets up session log history dialog

        Args:
            ui (class): the class that contains the log message widget
        """
        # log history dialog
        self.log = QDialog()
        self.log.setWindowFlags(Qt.Window)
        self.log.setWindowIcon(
            QWidget()
            .style()
            .standardIcon(QStyle.StandardPixmap.SP_FileDialogContentsView)
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
        """loads UI_MainWindow

        Args:
            ui (class): MainWindow descriptor
        """
        # load mainwindow ui
        self.logger.debug("Loading UI_MainWindow()")
        self.ui = ui
        self.ui.setupUi(self)
        self.hide()
        # MainWindow icon
        window_icon_path = QDir(f"{self.lib_root_path}/docs/img/")
        self.setWindowIcon(
            QIcon(
                window_icon_path.toNativeSeparators(
                    window_icon_path.absoluteFilePath("Logolarge.png")
                )
            )
        )

    def set_up_ui_icons(self):
        """set up ui icons"""
        # icons
        self.ui.fileDialogContentsViewIcon = (
            QWidget()
            .style()
            .standardIcon(QStyle.StandardPixmap.SP_FileDialogContentsView)
        )
        self.ui.messageBoxCriticalIcon = (
            QWidget().style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxCritical)
        )
        self.ui.fileIcon = (
            QWidget().style().standardIcon(QStyle.StandardPixmap.SP_FileIcon)
        )
        self.ui.commandLinkIcon = (
            QWidget().style().standardIcon(QStyle.StandardPixmap.SP_CommandLink)
        )
        self.ui.trashIcon = (
            QWidget().style().standardIcon(QStyle.StandardPixmap.SP_TrashIcon)
        )
        self.ui.messageBoxQuestionIcon = (
            QWidget().style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxQuestion)
        )

    # do before close
    def do_before_app_close(self, event=None, restarting=False):
        """do these things before app close

        Args:
            event (QEvent, optional): event if there is one. Defaults to None.
            restarting (bool, optional): the app is restarting if True. Defaults to False.
        """
        MainWindow.logger.debug(str(event))
        if self.write_cli_gen_tool_json() > 0:
            MainWindow.logger.debug("session json saved")
        result = 0
        if self.prompt_to_save == True:
            b = QDialogButtonBox.StandardButton
            buttons = [b.Save, b.Close, b.Cancel]
            button_text = ["", "Close without saving", ""]
            result = self.create_qdialog(
                "Save your work?",
                Qt.AlignCenter,
                0,
                "Save changes",
                buttons,
                button_text,
                QWidget()
                .style()
                .standardIcon(QStyle.StandardPixmap.SP_MessageBoxQuestion),
            )
        else:  # no work to save
            result = 4
        # log the exit type
        if result == 0:
            if event != None and type(event) != bool:
                event.ignore()
            MainWindow.logger.info("Exit cancelled")
        elif result == 2:
            if self.save_file() >= 0:
                self.log.close()
                MainWindow.logger.info("Saved. Exiting CLI generation tool.")
                if event != None and type(event) != bool:
                    event.accept()
                if not restarting:
                    sys.exit(self.app.quit())
                else:
                    os.execl(sys.executable, sys.executable, *sys.argv)
            else:
                MainWindow.logger.info("Exit cancelled")
        elif result == 3:
            self.log.close()
            MainWindow.logger.info("Not saved. Exiting CLI generation tool.")
            if event != None and type(event) != bool:
                event.accept()
            if not restarting:
                sys.exit(self.app.quit())
            else:
                os.execl(sys.executable, sys.executable, *sys.argv)
        elif result == 4:
            self.log.close()
            MainWindow.logger.info("Nothing to Save. Exiting CLI generation tool.")
            if event != None and type(event) != bool:
                event.accept()
            if not restarting:
                sys.exit(self.app.quit())
            else:
                os.execl(sys.executable, sys.executable, *sys.argv)

    def save_file(self):
        """save working file

        Returns:
            int: filesize on success, -1 on fail, 0 on fail
        """
        MainWindow.logger.info("save CLI settings file")
        MainWindow.logger.debug("set tool version var in cli_options")
        self.cli_options["var"]["tool version"] = self.version
        if (
            self.session["opt"]["save_file_path"] == ""
            or self.session["opt"]["save_file_path"] == None
        ):
            ret = self.save_file_as()
            if ret >= 0:
                self.prompt_to_save = False
            return ret
        file = QFile(self.session["opt"]["save_file_path"])
        ret = self.write_json(self.cli_options, file, True)
        if ret >= 0:
            self.prompt_to_save = False
        self.windowtitle_set = False
        self.set_main_window_title()
        return ret

    def save_file_as(self):
        """save working file as QFileDialog prompt

        Returns:
            int: filesize
        """
        # inherit from parent QMainWindow (block main window interaction while dialog box is open)
        dlg = QFileDialog(self)
        fileName = dlg.getSaveFileName(
            self,
            "Save file name",
            "./tools/interfaces/",
            "*.json",
            options=QFileDialog.DontUseNativeDialog,
        )
        if fileName[0] == "":
            MainWindow.logger.info("Save file dialog cancelled.")
            return QFileDialog.Rejected  # dialog cancelled
        fqname = f"{fileName[0]}.json"
        self.session["opt"]["save_file_path"] = fqname
        MainWindow.logger.info(f"Save CLI settings file as: {str(fqname)}")
        file = QFile(fqname)
        ret = self.write_json(self.cli_options, file, True)
        return ret

    # MainWindow actions
    def get_recent_files_menu(self) -> QMenu:
        """builds the recent files menu

        Returns:
            QMenu: recent files menu
        """
        # build menu
        menu = QMenu(self)
        paths = self.session["opt"]["recent_files"]["paths"]
        for path in paths:
            if os.path.exists(path):
                filename = os.path.basename(os.path.realpath(path))
                action = QAction(f"{filename}", menu)
                action.setToolTip(path)
                action.triggered.connect(
                    lambda c=action.triggered, p=path: self.open_file(c, p)
                )
                menu.addAction(action)
        return menu

    def gui_settings(self):
        """opens preferences dialog"""
        MainWindow.logger.info("opened preferences dialog")
        self.preferences.exec(self.actionOpen_Recent)

    # generate CLI files
    def generate_cli_files(self):
        """generates cli files in self.session["opt"]["cli_output_dir"]"""
        MainWindow.logger.info("generate cli files")
        self.generate_cli()

    def gui_about(self):
        """opens an about dialog"""
        MainWindow.logger.info("open about dialog")
        about_string = """<a href=\"https://github.com/dstroy0/InputHandler\">Link to library github</a><br><br>
        Library authors:<br>
        Douglas Quigg (dstroy0 dquigg123@gmail.com)<br>
        Brendan Doherty (2bndy5 2bndy5@gmail.com)<br>"""
        self.create_qdialog(
            about_string,
            Qt.AlignCenter,
            Qt.TextBrowserInteraction,
            "About",
            None,
            None,
            QStyle.StandardPixmap.SP_MessageBoxQuestion,
        )

    ## opens an internet browser to the library's documentation
    def gui_documentation(self):
        """open browser to docs wrapper"""
        MainWindow.logger.info("open GUI documentation")
        os_type = platform.uname().system.lower()  # lowercase os type
        # windows
        if os_type == "windows":
            os.system('start "" https://dstroy0.github.io/InputHandler/')
        # macos
        elif os_type == "darwin":
            os.system('open "" https://dstroy0.github.io/InputHandler/')
        # linux
        elif os_type == "linux":
            os.system('xdg-open "" https://dstroy0.github.io/InputHandler/')

    ## opens the log history subwindow
    def gui_log_history(self):
        """open log history window"""
        if not self.log.isActiveWindow() and not self.log.isVisible():
            self.log.show()
            self.log.raise_()
            self.log.activateWindow()
            return
        if self.log.isVisible():
            self.log.raise_()
            self.log.activateWindow()

    ## MainWindow file menu actions
    def mainwindow_menu_bar_actions_setup(self):
        """menu bar setup"""
        # file menu actions setup
        # file menu
        self.ui.actionOpen.triggered.connect(self.open_file)
        self.ui.actionOpen_Recent.setMenu(self.get_recent_files_menu())
        self.ui.actionSave.triggered.connect(self.save_file)
        self.ui.actionSave_As.triggered.connect(self.save_file_as)
        self.ui.actionPreferences.triggered.connect(self.gui_settings)
        self.ui.actionExit.triggered.connect(self.app.quit)
        # generate menu
        self.ui.actionGenerate_CLI_Files.triggered.connect(self.ui.generateDialog.exec)
        # about menu
        self.ui.actionAbout.triggered.connect(self.gui_about)
        self.ui.actionInputHandler_Documentation.triggered.connect(
            self.gui_documentation
        )
        self.ui.actionOpen_Log_History.triggered.connect(self.gui_log_history)
        # end file menu actions setup

    ## MainWindow button actions
    def mainwindow_button_actions_setup(self):
        """MainWindow button actions"""
        # buttons setup
        # tab 1
        self.ui.edit_setting_button.clicked.connect(self.clicked_edit_tab_one)
        self.ui.clear_setting_button.clicked.connect(self.clicked_clear_tab_one)
        self.ui.default_setting_button.clicked.connect(self.clicked_default_tab_one)
        self.ui.settings_tree_collapse_button.clicked.connect(
            self.settings_tree_collapse_button
        )

        # tab 2
        self.ui.new_cmd_button.clicked.connect(self.clicked_new_cmd_button)
        self.ui.edit_cmd_button.clicked.connect(self.clicked_edit_tab_two)
        self.ui.delete_cmd_button.clicked.connect(self.clicked_delete_tab_two)
        self.ui.command_tree_collapse_button.clicked.connect(
            self.command_tree_collapse_button
        )
        # end buttons setup

    # end MainWindow actions

    def get_tree_state(self, tree: QTreeWidget) -> dict:
        """gets button state and selected item in tree

        Args:
            tree (QTreeWidget): tree that was interacted with

        Returns:
            dict: tree state dict
        """
        tree_state = copy.deepcopy(DataModels.button_tree_state_dict)
        tree_state["tree"] = tree
        tsi = tree.selectedItems()
        is_root = False

        if bool(tsi):
            # get the container item if it's the command tree
            if tree == self.command_tree:
                tsi[0] = self.command_tree.get_parent_item(tsi[0])

            tree_state["items selected"] = tsi
            tree_state["item selected"] = tsi[0]
            tree_state["index of top level item"] = tree.indexOfTopLevelItem(tsi[0])
            tree_state["current item index"] = tree.indexFromItem(tsi[0])
            tree_state["root item index"] = tree.rootIndex()
            tree_state["child count"] = tsi[0].childCount()
            tree_state["table widget"] = tree.itemWidget(tsi[0], 0)
            tree_state["combobox widget"] = tree.itemWidget(tsi[0], 3)
            tree_state["is expanded"] = tsi[0].isExpanded()
            if (
                tree_state["current item index"] == tree_state["root item index"]
                and tree_state["root item index"] != None
            ):
                is_root = True
        else:
            is_root = True
            tree_state["root item index"] = tree.rootIndex()
            tree_state["current item index"] = tree.currentIndex()
            tree_state["child count"] = tree.topLevelItemCount()
            tree_state["is expanded"] = tree.invisibleRootItem().isExpanded()
        tree_state["root item selected"] = is_root

        return tree_state

    def queue_collapse_button_text(self, button_dict: dict):
        """queue collapse button text change

        Args:
            button_dict (dict): button interacted with
        """
        text = None
        if bool(button_dict["item selected"]) and not bool(
            button_dict["tree"].invisibleRootItem() == button_dict["tree"].currentItem()
        ):
            if button_dict["is expanded"] == True:
                text = "Collapse"
            else:
                text = "Expand"
        elif (
            not bool(button_dict["item selected"])
            or button_dict["tree"].invisibleRootItem()
            == button_dict["tree"].currentItem()
            or button_dict["buttons"]["collapse"]["QPushButton"].text()
            == "Collapse All"
        ):
            text = "Expand All"
        elif button_dict["buttons"]["collapse"]["QPushButton"].text() == "Expand All":
            text = "Collapse All"

        if text != None:
            button_dict["buttons"]["collapse"]["text"] = text
        else:
            MainWindow.logger.warning("collapse button text empty")

    def tree_expander(self, button_text: str, button_dict: dict):
        """expands tree based off of button information

        Args:
            button_text (str): text of button
            button_dict (dict): button information
        """
        if not bool(button_dict["root item selected"]) and button_text == "Expand":
            button_dict["item selected"].setExpanded(True)
            button_dict["buttons"]["collapse"]["QPushButton"].setText("Collapse")
        elif not bool(button_dict["root item selected"]) and button_text == "Collapse":
            button_dict["item selected"].setExpanded(False)
            button_dict["buttons"]["collapse"]["QPushButton"].setText("Expand")
        elif bool(button_dict["root item selected"]) and button_text == "Expand All":
            button_dict["tree"].expandAll()
            button_dict["buttons"]["collapse"]["QPushButton"].setText("Collapse All")
        elif bool(button_dict["root item selected"]) and button_text == "Collapse All":
            button_dict["tree"].collapseAll()
            button_dict["buttons"]["collapse"]["QPushButton"].setText("Expand All")

    def set_tree_button_context(self, button_dict: dict):
        """contextual button text

        Args:
            button_dict (dict): button to set
        """
        for i in button_dict["buttons"]:
            if i != "collapse":
                butt = button_dict["buttons"][i]
                if butt["text"] != None:
                    butt["QPushButton"].setText(butt["text"])
                    butt["text"] = None
                butt["QPushButton"].setEnabled(butt["enabled"])
            else:
                butt = button_dict["buttons"][i]
                butt["text"] = None
                if bool(button_dict["item selected"]) and not bool(
                    button_dict["root item selected"]
                ):
                    if bool(button_dict["is expanded"]):
                        butt["text"] = "Collapse"
                    else:
                        butt["text"] = "Expand"
                elif bool(button_dict["root item selected"]):
                    if bool(button_dict["is expanded"]):
                        butt["text"] = "Collapse All"
                    else:
                        butt["text"] = "Expand All"
                if butt["text"] != None:
                    butt["QPushButton"].setText(butt["text"])
                    butt["text"] = None
                butt["QPushButton"].setEnabled(butt["enabled"])

    def settings_tree_collapse_button(self):
        """settings tree collapse button"""
        tree_state = self.get_tree_state(self.settings_tree)
        tree_buttons = self.settings_tree_buttons
        tree_buttons.update(tree_state)
        self.tree_expander(
            tree_buttons["buttons"]["collapse"]["QPushButton"].text(), tree_buttons
        )
        if tree_buttons["root item selected"]:
            self.settings_tree_collapsed = (
                tree_buttons["tree"].invisibleRootItem().isExpanded()
            )

    def command_tree_collapse_button(self):
        """command tree collapse button"""
        tree_state = self.get_tree_state(self.command_tree)
        tree_buttons = self.command_tree_buttons
        tree_buttons.update(tree_state)
        if tree_buttons["root item selected"]:
            self.command_tree_collapsed = tree_buttons["is expanded"]
        self.tree_expander(
            tree_buttons["buttons"]["collapse"]["QPushButton"].text(), tree_buttons
        )

    def settings_tree_button_toggles(self):
        """settings tree button toggles"""
        tree_state = self.get_tree_state(self.settings_tree)

        if self.prev_settings_tree_state == tree_state:
            return

        self.prev_settings_tree_state = self.get_tree_state(self.settings_tree)

        tree_buttons = self.settings_tree_buttons
        tree_buttons.update(tree_state)
        if (
            tree_buttons["item selected"]
            and tree_buttons["index of top level item"] == -1
            and tree_buttons["child count"] == 0
        ):
            # table widgets get special treatment, there is no default
            if isinstance(
                tree_buttons["table widget"],
                QTableView,
            ):
                tree_buttons["buttons"]["edit"]["enabled"] = True
                tree_buttons["buttons"]["clear"]["enabled"] = True
                tree_buttons["buttons"]["default"]["enabled"] = False
            # comboboxes can be edited and set to their default
            elif isinstance(
                tree_buttons["combobox widget"],
                QComboBox,
            ):
                tree_buttons["buttons"]["edit"]["enabled"] = True
                tree_buttons["buttons"]["clear"]["enabled"] = False
                tree_buttons["buttons"]["default"]["enabled"] = True
            else:
                tree_buttons["buttons"]["edit"]["enabled"] = True
                tree_buttons["buttons"]["clear"]["enabled"] = True
                tree_buttons["buttons"]["default"]["enabled"] = True
        # nothing selected
        else:
            tree_buttons["buttons"]["edit"]["enabled"] = False
            tree_buttons["buttons"]["clear"]["enabled"] = False
            tree_buttons["buttons"]["default"]["enabled"] = False
        self.set_tree_button_context(tree_buttons)

    def command_tree_button_toggles(self):
        """command tree button toggles"""
        tree_state = self.get_tree_state(self.command_tree)

        if self.prev_command_tree_state == tree_state:
            return

        self.prev_command_tree_state = self.get_tree_state(self.command_tree)
        tree_buttons = self.command_tree_buttons
        tree_buttons.update(tree_state)
        # new/edit/delete/command settings menu button enable/disable toggling
        if bool(tree_buttons["root item selected"]):
            tree_buttons["buttons"]["new"]["text"] = "New (root command)"
            tree_buttons["buttons"]["new"]["enabled"] = True
            tree_buttons["buttons"]["edit"]["enabled"] = False
            tree_buttons["buttons"]["delete"]["enabled"] = False
        # if the list is NOT empty (truthy)
        elif not bool(tree_buttons["root item selected"]) and bool(
            tree_buttons["item selected"]
        ):
            # something on the command tree is selected
            # _object_list = tree_buttons["item selected"].data(1, 0).split(",")
            _item_matched_builtin = False
            tree_item = self.command_tree.currentItem()
            if tree_item.childCount() == 0:
                tree_item = tree_item.parent()
            command_string = tree_item.data(0, 0)

            if command_string in self.ih_builtins:
                _item_matched_builtin = True

            if _item_matched_builtin:  # item selected is an InputHandler builtin
                tree_buttons["buttons"]["new"]["text"] = "New"
                tree_buttons["buttons"]["new"]["enabled"] = False
                tree_buttons["buttons"]["edit"]["enabled"] = False
                tree_buttons["buttons"]["delete"]["enabled"] = True
            else:  # item selected is NOT an InputHandler builtin
                # give user option to add children to this command
                tree_buttons["buttons"]["new"]["text"] = "New (child command)"
                tree_buttons["buttons"]["new"]["enabled"] = True
                tree_buttons["buttons"]["edit"]["enabled"] = True
                tree_buttons["buttons"]["delete"]["enabled"] = True
        else:
            tree_buttons["buttons"]["new"]["text"] = "New"
            tree_buttons["buttons"]["new"]["enabled"] = False
            tree_buttons["buttons"]["edit"]["enabled"] = False
            tree_buttons["buttons"]["delete"]["enabled"] = False
        self.set_tree_button_context(tree_buttons)

    # MainWindow buttons
    # tab 1
    def clicked_edit_tab_one(self):
        """MainWindow tab 1 edit button click interaction"""
        MainWindow.logger.info("clicked tab 1 edit")
        if self.settings_tree.currentItem() != None:
            object_list = self.settings_tree.currentItem().data(4, 0).split(",")
            if (
                object_list[2] == "data delimiter sequences"
                or object_list[2] == "start stop data delimiter sequences"
            ):
                table_widget = self.settings_tree.itemWidget(
                    self.settings_tree.currentItem(), 0
                )
                items = table_widget.selectedItems()
                item = items[0]
                table_widget.editItem(item)
                self.update_code("cli.h", object_list[2], True)
                return
            self.settings_tree.editItem(self.settings_tree.currentItem(), 3)

    def clicked_clear_tab_one(self):
        """MainWindow tab 1 clear button interaction"""
        MainWindow.logger.info("clicked tab 1 clear")
        if self.settings_tree.currentItem() != None:
            object_list = self.settings_tree.currentItem().data(4, 0).split(",")
            if (
                object_list[2] == "data delimiter sequences"
                or object_list[2] == "start stop data delimiter sequences"
            ):
                table_widget = self.settings_tree.itemWidget(
                    self.settings_tree.currentItem(), 0
                )
                items = table_widget.selectedItems()
                item = items[0]
                row = table_widget.row(item)
                if row < table_widget.rowCount():
                    clear_item = table_widget.item(row, 0)
                    clear_item.setText("")
                    self.update_code("cli.h", object_list[2], True)
                self.cli_options["process parameters"]["var"][object_list[2]] = {}
                for i in range(table_widget.rowCount() - 1):
                    self.cli_options["process parameters"]["var"][
                        object_list[2]
                    ].update({i: table_widget.item(i, 0).text().strip("'")})
                return
            self.settings_tree.currentItem().setData(3, 0, "")

    def clicked_default_tab_one(self):
        """MainWindow tab 1 default button interaction"""
        tree_item = self.settings_tree.currentItem()
        if tree_item != None:
            widget = self.settings_tree.itemWidget(tree_item, 3)
            object_list = tree_item.data(4, 0).split(",")
            if isinstance(widget, QComboBox):
                bool_default = self.default_settings_tree_values[object_list[2]]
                if bool_default == True:
                    default_index = "Enabled"
                else:
                    default_index = "Disabled"
                widget.setCurrentIndex(widget.findText(default_index))
                MainWindow.logger.info(
                    f"{str(object_list[0])} {object_list[2]} set to default: {default_index}"
                )
            else:
                default_val = str(
                    self.default_settings_tree_values[str(tree_item.data(1, 0))]
                )
                tree_item.setData(3, 0, default_val)
                MainWindow.logger.info(
                    f"{str(object_list[0])} {object_list[2]} set to default: {default_val}"
                )

    # tab 2
    def clicked_edit_tab_two(self):
        """MainWindow tab 2 edit button interaction"""
        MainWindow.logger.info("edit command")
        parameters_key = self.cli_options["commands"]["index"][
            self.command_tree.active_item.data(1, 0)
        ]["parameters key"]
        self.edit_existing_command(parameters_key)

    def clicked_new_cmd_button(self):
        """MainWindow tab 2 new command button (contextual)"""
        if "(root command)" in self.ui.new_cmd_button.text():
            MainWindow.logger.info("user clicked new command button with root context")
            self.ui.commandParameters.setWindowTitle("Root Command Parameters")
            fields = copy.deepcopy(self.command_parameters_input_field_settings)
            fields["parentId"]["value"] = 0
            fields["parentId"]["enabled"] = False
            fields["commandId"]["value"] = 0
            fields["commandId"]["enabled"] = False
            fields["commandDepth"]["value"] = 0
            fields["commandDepth"]["enabled"] = False
            fields["commandArguments"]["value"] = "{{UITYPE::NO_ARGS}}"
            self.command_tree.active_item = self.command_tree.invisibleRootItem()

            self.commandparameters_set_fields(fields)
            self.ui.commandParameters.dlg.defaults = fields
            self.generate_commandparameters_arg_table(
                self.parse_commandarguments_string(fields["commandArguments"]["value"])
            )
            self.ui.commandParameters.exec()
        elif "(child command)" in self.ui.new_cmd_button.text():
            MainWindow.logger.info("user clicked new command button with child context")
            self.ui.commandParameters.setWindowTitle("Child Command Parameters")
            cmd_idx = self.command_tree.active_item.data(1, 0)
            prm_key = self.cli_options["commands"]["index"][cmd_idx]["parameters key"]
            rt_idx = self.cli_options["commands"]["index"][cmd_idx]["root index key"]
            rt_prm_idx = self.cli_options["commands"]["index"][rt_idx]["parameters key"]
            parameters = self.cli_options["commands"]["parameters"][prm_key]
            item_list = self.command_tree.findItems(rt_prm_idx, Qt.MatchExactly, 1)
            item = None
            if bool(item_list):
                item = item_list[0]

            child_depth = int(parameters["commandDepth"]) + 1
            root_child_count = 0

            def recursive_childcount(item, child_count):
                """gets total number of children of an item

                Args:
                    item (QTreeWidgetItem): selected item
                    child_count (int): number of children

                Returns:
                    int: number of children
                """
                for row in range(item.childCount()):
                    child_item = item.child(row)
                    if item is not None:
                        child_count += 1
                    recursive_childcount(child_item, child_count)
                return child_count

            root_child_count = recursive_childcount(item, root_child_count)

            fields = copy.deepcopy(self.command_parameters_input_field_settings)
            fields["parentId"]["value"] = parameters["commandId"]
            fields["parentId"]["enabled"] = False
            fields["commandId"]["value"] = root_child_count + 1
            fields["commandId"]["enabled"] = False
            fields["commandDepth"]["value"] = child_depth
            fields["commandDepth"]["enabled"] = False
            fields["commandArguments"]["value"] = "{{UITYPE::NO_ARGS}}"
            self.commandparameters_set_fields(fields)
            self.ui.commandParameters.dlg.defaults = fields
            self.generate_commandparameters_arg_table(
                self.parse_commandarguments_string(fields["commandArguments"]["value"])
            )
            self.ui.commandParameters.exec()

    def clicked_delete_tab_two(self) -> None:
        """MainWindow tab 2 delete button interaction"""
        MainWindow.logger.debug("clicked tab two delete")
        self.command_tree.remove_command_from_tree()


# end MainWindow
