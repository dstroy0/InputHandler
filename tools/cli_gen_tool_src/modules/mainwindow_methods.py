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

import platform
import sys
import copy
import os
import json
import glob
from json import dumps as json_dumps

from PySide6.QtCore import (
    QRegularExpression,
    QEvent,
    QObject,
    QSettings,
    QDir,
    Qt,
    QFile,
    QByteArray,
    QIODevice,
    QTextStream,
)

from PySide6.QtGui import QPixmap, QIcon

from PySide6.QtWidgets import (
    QSplashScreen,
    QDialog,
    QStyle,
    QWidget,
    QDialogButtonBox,
    QFileDialog,
    QTableView,
    QComboBox,
    QTreeWidget,
)

from modules.data_models import dataModels

# MainWindow methods


class MainWindowMethods(object):
    """methods related to MainWindow interaction and operation

    Args:
        object (object): base object specialization
    """

    def __init__(self) -> None:
        """the constructor"""
        super(MainWindowMethods, self).__init__()
        MainWindowMethods.logger = self.get_child_logger(__name__)
        self.create_qdialog = self.create_qdialog
        self._parent = self
        self.old_path = ""
        self.prev_command_tree_state = 0
        self.prev_settings_tree_state = 0

    def generatedialog_set_output_dir(self):
        project_path = self.get_project_dir()
        if project_path:
            self.session["opt"]["output_dir"] = project_path
            MainWindowMethods.logger.info(
                "set session output_dir to:\n" + str(project_path)
            )
            self.ui.generateDialog.dlg.outputPathLineEdit.setText(
                self.session["opt"]["output_dir"]
            )

    def generatedialog_clicked_platformio_file_output_structure(self):
        MainWindowMethods.logger.info("platformio file output structure selected")

    def generatedialog_clicked_arduino_file_output_structure(self):
        MainWindowMethods.logger.info("arduino file output structure selected")

    def cli_generation_dialog_setup(self, ui):
        self.ui.generateDialog = QDialog(self)
        self.ui.generateDialog.setWindowIcon(
            QWidget()
            .style()
            .standardIcon(QStyle.StandardPixmap.SP_FileDialogContentsView)
        )
        self.ui.generateDialog.dlg = ui
        self.ui.generateDialog.dlg.setupUi(self.ui.generateDialog)
        # self.ui.generateDialog.setMaximumSize(0, 0)
        self.ui.generateDialog.dlg.outputPathLineEdit.setText(
            self.session["opt"]["output_dir"]
        )
        self.ui.generateDialog.dlg.pushButton.clicked.connect(
            self.generatedialog_set_output_dir
        )
        self.ui.generateDialog.dlg.buttonBox.accepted.connect(self.generate_cli_files)
        self.ui.generateDialog.dlg.buttonBox.rejected.connect(
            self.ui.generateDialog.close
        )
        project_path = self.session["opt"]["output_dir"]
        file_structure = glob.glob(os.path.join(project_path, "*.ino"))
        arduino_compatibility = False
        if file_structure:
            # arduino
            arduino_compatibility = True
        elif project_path.find("sketch"):
            arduino_compatibility = True
        if arduino_compatibility:
            self.ui.generateDialog.dlg.arduinoRadioButton.setChecked(True)
        else:
            self.ui.generateDialog.dlg.platformioRadioButton.setChecked(True)
        self.ui.generateDialog.dlg.platformioRadioButton.clicked.connect(
            self.generatedialog_clicked_platformio_file_output_structure
        )
        self.ui.generateDialog.dlg.arduinoRadioButton.clicked.connect(
            self.generatedialog_clicked_arduino_file_output_structure
        )

    def get_project_dir(self) -> str:
        """get valid os path to project

        Returns:
            str: valid os path or None
        """
        dir_dlg = QFileDialog(self)
        _dlg_result = dir_dlg.getExistingDirectory(
            self,
            "Select output directory",
            "",
            options=QFileDialog.DontUseNativeDialog
            | QFileDialog.ShowDirsOnly
            | QFileDialog.DontResolveSymlinks,
        )
        if _dlg_result == QFileDialog.Rejected:
            b = QDialogButtonBox.StandardButton
            buttons = [b.Ok, b.Close]
            button_text = ["Select output directory", "Cancel"]
            result = self.create_qdialog(
                self._parent,
                "You must select an output directory to generate files.",
                Qt.AlignCenter,
                Qt.NoTextInteraction,
                "Error, no output directory selected!",
                buttons,
                button_text,
                QIcon(
                    QWidget()
                    .style()
                    .standardIcon(QStyle.StandardPixmap.SP_MessageBoxCritical)
                ),
                self._parent.qscreen,
            )
            if result == 3:
                return None

        _dir = QDir(_dlg_result)
        _result = _dir.toNativeSeparators(_dir.absolutePath())
        if os.path.exists(_result):
            MainWindowMethods.logger.info("valid directory selected:\n" + str(_result))
            return _result
        else:
            MainWindowMethods.logger.info("invalid directory selected")
            return None

    def get_initial_config_path(self):
        """get initial path to config"""
        self.old_path = QDir(
            self._parent.session["opt"]["input_config_file_path"]
        ).absolutePath()
        self.old_path = QDir(self.old_path).toNativeSeparators(self.old_path)
        self._parent.old_path = self.old_path

    def get_config_file(self, config_path: str = None):
        """gets new valid config file

        Args:
            config_path (str, optional): path to alternate config. Defaults to None.
        """
        old_path = self.old_path
        new_path = config_path
        if new_path == None:
            cfg_path_dlg = QFileDialog(self)
            fileName = cfg_path_dlg.getOpenFileName(
                self,
                "InputHandler config file name",
                QDir(self.session["opt"]["input_config_file_path"]).toNativeSeparators(
                    self.session["opt"]["input_config_file_path"]
                ),
                "config.h",
                options=QFileDialog.DontUseNativeDialog,
            )
            if fileName[0] == "":
                MainWindowMethods.logger.info("browse for config cancelled.")
                return
            fqname = fileName[0]
            new_path = QDir(fqname).absolutePath()
            new_path = QDir(new_path).toNativeSeparators(new_path)
        if new_path == old_path:
            MainWindowMethods.logger.info("Same config file selected.")
            return
        self.session["opt"]["input_config_file_path"] = fqname
        self._parent.preferences.dlg.config_path_input.setText(str(fqname))
        self._parent.preferences.dlg.config_path_input.setToolTip(str(fqname))
        # restart to apply selected config
        self.restart(self, "New config file selected.")

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
            MainWindowMethods.logger.debug("setting mainwindow title")
            self.setWindowTitle(windowtitle)
            self.windowtitle_set = True

    def _eventFilter(self, watched: QObject, event: QEvent) -> bool:
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

    def _closeEvent(self, event: QEvent):
        """do these things on app close

        Args:
            event (QEvent): closeEvent type
        """
        MainWindowMethods.logger.info("save app states")
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

    def _readSettings(self, settings: QSettings):
        """reats QSettings

        Args:
            settings (QSettings): app settings
        """
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
        else:
            self.ui.command_tree_collapse_button.setText("Expand All")
        if self.settings.value("settings_tree_state") != None:
            self.settings_tree.restoreState(self.settings.value("settings_tree_state"))
        else:
            self.ui.settings_tree_collapse_button.setText("Expand All")

        self.command_tree_button_toggles()
        self.settings_tree_button_toggles()

    def show_splash(self):
        """shows app splashscreen if applicable"""
        MainWindowMethods.logger.info("load splash")
        self.splash = QSplashScreen(self.qscreen)

        _splash_path = QDir(self.lib_root_path + "/docs/img/")
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
        window_icon_path = QDir(self.lib_root_path + "/docs/img/")
        self.setWindowIcon(
            QIcon(
                window_icon_path.toNativeSeparators(
                    window_icon_path.absoluteFilePath("Logolarge.png")
                )
            )
        )

    def set_up_command_parameters_dialog(self, ui):
        """sets up command parameters dialog

        Args:
            ui (class): command parameters ui
        """
        # load command parameters input dialog ui
        self.ui.commandParameters = QDialog(self)
        # blue circle question icon
        self.ui.commandParameters.setWindowIcon(
            QWidget().style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxQuestion)
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
        """sets up user session json"""
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
        MainWindowMethods.logger.debug(str(event))
        if self.write_cli_gen_tool_json() > 0:
            MainWindowMethods.logger.debug("session json saved")
        result = 0
        if self.prompt_to_save == True:
            b = QDialogButtonBox.StandardButton
            buttons = [b.Save, b.Close, b.Cancel]
            button_text = ["", "Close without saving", ""]
            result = self._parent.create_qdialog(
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
            MainWindowMethods.logger.info("Exit cancelled")
        elif result == 2:
            if self.save_file() >= 0:
                self.log.close()
                MainWindowMethods.logger.info("Saved. Exiting CLI generation tool.")
                if event != None and type(event) != bool:
                    event.accept()
                if not restarting:
                    sys.exit(self.app.quit())
                else:
                    os.execl(sys.executable, sys.executable, *sys.argv)
            else:
                MainWindowMethods.logger.info("Exit cancelled")
        elif result == 3:
            self.log.close()
            MainWindowMethods.logger.info("Not saved. Exiting CLI generation tool.")
            if event != None and type(event) != bool:
                event.accept()
            if not restarting:
                sys.exit(self.app.quit())
            else:
                os.execl(sys.executable, sys.executable, *sys.argv)
        elif result == 4:
            self.log.close()
            MainWindowMethods.logger.info(
                "Nothing to Save. Exiting CLI generation tool."
            )
            if event != None and type(event) != bool:
                event.accept()
            if not restarting:
                sys.exit(self.app.quit())
            else:
                os.execl(sys.executable, sys.executable, *sys.argv)

    def create_file_error_qdialog(self, error_type: str, qfile: QFile):
        """creates an error dialog

        Args:
            error_type (str): error description
            qfile (QFile): file information
        """
        MainWindowMethods.logger.warning(
            error_type + " " + qfile.fileName() + " error."
        )
        self.create_qdialog(
            error_type,
            Qt.AlignCenter,
            0,
            error_type + " " + qfile.fileName() + " error.",
            None,
            None,
            self.ui.messageBoxCriticalIcon,
        )

    def write_json(
        self, dict_to_serialize: dict, qfile: QFile, create_error_dialog: bool = False
    ):
        """writes a json to disk

        Args:
            dict_to_serialize (dict): make this dict serializable
            qfile (QFile): the file to write
            create_error_dialog (bool, optional): create dialog on error if True. Defaults to False.

        Returns:
            int: -1 on error or filesize
        """
        if not qfile.open(QIODevice.WriteOnly | QIODevice.Text):
            MainWindowMethods.logger.info("Save " + qfile.fileName() + " error.")
            if create_error_dialog:
                self.create_file_error_qdialog("Save file", qfile)
            return -1  # file error

        # replace non serializable with null
        def default(o):
            try:
                iterable = iter(o)
            except TypeError:
                pass
            else:
                return list(iterable)

        # remove unserializable items to save disk space
        def dict_iterator(input):
            output = copy.deepcopy(input)

            def recurse(input, output):
                for key, value in input.items():
                    if input[key] == None:
                        if key.isnumeric():
                            output.pop(key)
                        else:
                            output[key] = ""
                    if isinstance(value, dict):
                        recurse(input[key], output[key])

            recurse(input, output)
            return output

        if dict_to_serialize["type"] == "cli options":
            # filter json
            dict_to_serialize["config"]["file lines"] = ""
            input_json = json.dumps(
                dict_to_serialize,
                sort_keys=False,
                default=default,
            )
            f_o = json.loads(input_json)
            filtered_output = copy.deepcopy(dict_iterator(f_o))

            output_json = json.dumps(filtered_output, indent=2, sort_keys=False)
        else:
            output_json = json.dumps(dict_to_serialize, indent=2, sort_keys=False)

        # file object
        out = QByteArray(output_json)

        size = qfile.write(out)
        if size != -1:
            MainWindowMethods.logger.info(
                "wrote " + str(size) + " bytes to " + str(qfile.fileName())
            )
            if dict_to_serialize["type"] != "session":
                if self.write_cli_gen_tool_json() > 0:
                    MainWindowMethods.logger.info("session json saved")
                regexp = QRegularExpression("[^\/]*$")
                match = regexp.match(str(self.session["opt"]["save_filename"]))
                if match.hasMatch():
                    self.setWindowTitle(
                        "InputHandler CLI generation tool - " + str(match.captured(0))
                    )
        else:
            MainWindowMethods.logger.info("Write " + qfile.fileName() + " error.")
            if create_error_dialog:
                self.create_file_error_qdialog("Write file", qfile)
        qfile.close()
        return size

    def read_json(self, qfile: QFile, create_error_dialog: bool = False):
        """reads json from disk

        Args:
            qfile (QFile): file information
            create_error_dialog (bool, optional): create dialog on error if True. Defaults to False.

        Returns:
            int: -2 if file doesnt exist, -3 on access error, -4 on zero filesize or invalid json or exception,
        """
        db = {}
        if not qfile.exists():
            MainWindowMethods.logger.info("qfile.exists() == false")
            if create_error_dialog:
                self.create_file_error_qdialog("This file does not exist: ", qfile)
            return [-2, {}]  # file doesn't exist
        if not qfile.open(QIODevice.ReadOnly | QIODevice.Text):
            qfile.close()
            MainWindowMethods.logger.warning("File access error.")
            if create_error_dialog:
                self.create_file_error_qdialog("Access", qfile)
            return [-3, {}]  # access error
        data_in = QTextStream(qfile).readAll()
        qfile.close()
        try:
            db = json.loads(data_in)
            if "type" in db:
                MainWindowMethods.logger.info("loaded json: " + db["type"])
                return [len(data_in), db]
            elif len(db) == 0:
                return [-4, {}]
            else:
                MainWindowMethods.logger.info("invalid json type")
                MainWindowMethods.logger.debug(
                    "json.loads():\n" + str(json.dumps(db, indent=2))
                )
                return [-4, {}]
        except Exception as e:
            MainWindowMethods.logger.warning(str(e))
            return [-4, {}]

    def save_file(self):
        """save working file

        Returns:
            int: filesize on success, -1 on fail, 0 on fail
        """
        MainWindowMethods.logger.info("save CLI settings file")
        MainWindowMethods.logger.debug("set tool version var in cliOpt")
        self.cliOpt["var"]["tool version"] = self.version
        if (
            self.session["opt"]["save_filename"] == ""
            or self.session["opt"]["save_filename"] == None
        ):
            ret = self.save_file_as()
            if ret >= 0:
                self.prompt_to_save = False
            return ret
        file = QFile(self.session["opt"]["save_filename"])
        ret = self.write_json(self.cliOpt, file, True)
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
            MainWindowMethods.logger.info("Save file dialog cancelled.")
            return QFileDialog.Rejected  # dialog cancelled
        fqname = fileName[0] + ".json"
        self.session["opt"]["save_filename"] = fqname
        MainWindowMethods.logger.info("save CLI settings file as: " + str(fqname))
        file = QFile(fqname)
        ret = self.write_json(self.cliOpt, file, True)
        return ret

    def load_cli_gen_tool_json(self, path):
        """load session json

        Args:
            path (str): path to json

        Returns:
            int: filesize
        """
        file = QFile(path)
        read_json_result = self.read_json(file, False)
        error = read_json_result[0]
        _json = read_json_result[1]
        if error == -2:  # file not exists
            MainWindowMethods.logger.info(
                "cli_gen_tool.json doesn't exist, using default options"
            )
            _json = self.defaultGuiOpt
            _json["opt"]["input_config_file_path"] = self.default_lib_config_path
            return _json
        if error == -3:
            file.close()
            MainWindowMethods.logger.warning(
                "open cli_gen_tool.json error; using default options"
            )
            _json = self.defaultGuiOpt
            _json["opt"]["input_config_file_path"] = self.default_lib_config_path
            return _json
        return _json

    def write_cli_gen_tool_json(self):
        """writes session json

        Returns:
            int: filesize
        """
        file = QFile(self.cli_gen_tool_json_path)
        err = self.write_json(self.session, file, False)
        return err

    # MainWindow actions
    def open_file(self):
        """open a cli settings json QFileDialog

        Returns:
            int: filesize
        """
        MainWindowMethods.logger.info("open CLI settings file dialog")
        # inherit from parent QMainWindow (block main window interaction while dialog box is open)
        dlg = QFileDialog(self)
        dlg.setFileMode(QFileDialog.ExistingFile)
        dlg.setNameFilter("Settings json (*.json)")
        dlg.setViewMode(QFileDialog.Detail)
        fileName = dlg.getOpenFileName(options=QFileDialog.DontUseNativeDialog)
        if fileName[0] == "":
            MainWindowMethods.logger.info("open CLI settings file dialog cancelled")
            return  # dialog cancelled
        else:
            file = QFile(fileName[0])
            read_json_result = self.read_json(file, True)
            if (
                read_json_result[0] >= 0
                and read_json_result[1]["type"] == "cli options"
            ):
                self.cliOpt = read_json_result[1]
            else:
                self.create_file_error_qdialog("Incorrect json type", file)
            # empty trees
            self.ui.settings_tree.clear()
            self.ui.command_tree.clear()
            # rebuild from file
            self.build_lib_settings_tree()
            self.build_command_tree()
            self.display_initial_code_preview()
            self.prompt_to_save = False
            self.windowtitle_set = False

    def gui_settings(self):
        """opens preferences dialog"""
        MainWindowMethods.logger.info("opened preferences dialog")
        self.preferences.exec()

    # TODO
    # generate CLI files
    def generate_cli_files(self):
        """generates cli files in self.session["opt"]["output_dir"]"""
        MainWindowMethods.logger.info("generate cli files")
        self.generate_cli()

    def gui_about(self):
        """opens an about dialog"""
        MainWindowMethods.logger.info("open about dialog")
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
            self.ui.messageBoxQuestionIcon,
        )

    ## opens an internet browser to the library's documentation
    def gui_documentation(self):
        """open browser to docs wrapper"""
        MainWindowMethods.logger.info("open GUI documentation")
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
        tree_state = copy.deepcopy(dataModels.button_tree_state_dict)
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
            MainWindowMethods.logger.warning("collapse button text empty")

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
        MainWindowMethods.logger.info("clicked tab 1 edit")
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
                self.update_code("CLI.h", object_list[2], True)
                return
            self.settings_tree.editItem(self.settings_tree.currentItem(), 3)

    def clicked_clear_tab_one(self):
        """MainWindow tab 1 clear button interaction"""
        MainWindowMethods.logger.info("clicked tab 1 clear")
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
                    self.update_code("CLI.h", object_list[2], True)
                self.cliOpt["process parameters"]["var"][object_list[2]] = {}
                for i in range(table_widget.rowCount() - 1):
                    self.cliOpt["process parameters"]["var"][object_list[2]].update(
                        {i: table_widget.item(i, 0).text().strip("'")}
                    )
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
                MainWindowMethods.logger.info(
                    str(
                        object_list[0]
                        + " "
                        + object_list[2]
                        + " set to default: "
                        + default_index
                    )
                )
            else:
                default_val = str(
                    self.default_settings_tree_values[str(tree_item.data(1, 0))]
                )
                tree_item.setData(3, 0, default_val)
                MainWindowMethods.logger.info(
                    str(
                        object_list[0]
                        + " "
                        + object_list[2]
                        + " set to default: "
                        + default_val
                    )
                )

    # tab 2
    def clicked_edit_tab_two(self):
        """MainWindow tab 2 edit button interaction"""
        MainWindowMethods.logger.info("edit command")
        self.clicked_command_settings_menu_button_tab_two(True)

    def clicked_new_cmd_button(self):
        """MainWindow tab 2 new command button (contextual)"""
        if "(root command)" in self.ui.new_cmd_button.text():
            MainWindowMethods.logger.info(
                "user clicked new command button with root context"
            )
            self.ui.commandParameters.setWindowTitle("Root Command Parameters")
            fields = copy.deepcopy(self.command_parameters_input_field_settings)
            fields["parentId"]["value"] = 0
            fields["parentId"]["enabled"] = False
            fields["commandId"]["value"] = 0
            fields["commandId"]["enabled"] = False
            fields["commandDepth"]["value"] = 0
            fields["commandDepth"]["enabled"] = False
            self.command_tree.active_item = self.command_tree.invisibleRootItem()
            self.commandparameters_set_fields(fields)
            self.ui.commandParameters.exec()
        elif "(child command)" in self.ui.new_cmd_button.text():
            MainWindowMethods.logger.info(
                "user clicked new command button with child context"
            )
            self.ui.commandParameters.setWindowTitle("Child Command Parameters")
            cmd_idx = self.command_tree.active_item.data(1, 0)
            prm_key = self.cliOpt["commands"]["index"][cmd_idx]["parameters key"]
            rt_idx = self.cliOpt["commands"]["index"][cmd_idx]["root index key"]
            rt_prm_idx = self.cliOpt["commands"]["index"][rt_idx]["parameters key"]
            parameters = self.cliOpt["commands"]["parameters"][prm_key]
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

            self.commandparameters_set_fields(fields)
            self.ui.commandParameters.exec()

    def clicked_delete_tab_two(self) -> None:
        """MainWindow tab 2 delete button interaction"""
        MainWindowMethods.logger.debug("clicked tab two delete")
        self.command_tree.remove_command_from_tree()
