##
# @file cli_gen_tool.py
# @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
# @brief InputHandler CLI generation tool
# @version 0.1
# @date 2022-06-10
# @copyright Copyright (c) 2022
from __future__ import absolute_import
from queue import Empty

# Copyright (C) 2022 Douglas Quigg (dstroy0) <dquigg123@gmail.com>
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 3 as published by the Free Software Foundation.

# imports
import sys
import json
import time  # logging timestamp
import qdarktheme
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QDialog,
    QStyle,
    QSplashScreen,
)
from PySide6.QtCore import (
    Qt,
    QTimer,
    QPoint,
    QSize,
    QEvent,
    QObject,
    QRect,
    QPointF,
)
from PySide6.QtGui import (
    QIcon,
    QPixmap,
    QMouseEvent, QPainter, QPaintDevice
)

# import classes generated by PySide6 uic
from res.uic.mainWindow import Ui_MainWindow  # main window with tabs
from res.uic.commandParametersDialog import (
    Ui_commandParametersDialog,
)  # tab two popup dialog box

# external class methods
from res.modules.settings_tree_table_methods import SettingsTreeTableMethods
from res.modules.helper_methods import HelperMethods
from res.modules.mainwindow_actions import MainWindowActions
from res.modules.code_preview import CodePreview
from res.modules.settings_tree import SettingsTreeMethods
from res.modules.command_parameters import CommandParametersMethods
from res.modules.mainwindow_buttons import MainWindowButtons
from res.modules.parse_config import ParseInputHandlerConfig
from res.modules.dev_qol_var import *

## This is the main display window
#
# MainWindow is the parent of all process subwindows (MainWindow is noninteractable when any of its child popups are active)
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
):
    ## The constructor.
    def __init__(self, app, parent=None):
        super().__init__(parent)

        self.app = app  # used in external methods

        # import external methods into this instance of self
        HelperMethods.__init__(self)
        MainWindowActions.__init__(self)
        MainWindowButtons.__init__(self)
        ParseInputHandlerConfig.__init__(self)
        SettingsTreeMethods.__init__(self)
        SettingsTreeTableMethods.__init__(self)
        CommandParametersMethods.__init__(self)
        CodePreview.__init__(self)

        # pathing
        self.lib_root_path = lib_root_path
        # /InputHandler/src/config/config.h
        self.default_lib_config_path = self.lib_root_path + "/src/config/config.h"
        # /InputHandler/cli_gen_tool/cli_gen_tool.json
        self.cli_gen_tool_json_path = (
            self.lib_root_path + "/cli_gen_tool/cli_gen_tool.json"
        )
        print("loading CLI generation tool")
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # self.painter = QPainter(self)
        # MainWindow icon
        window_icon_path = self.lib_root_path + "/docs/img/Logolarge.png"
        self.setWindowIcon(QIcon(window_icon_path))
        # init param popup dialog
        self.ui.commandParameters = QDialog(self)
        # blue circle question icon
        self.ui.commandParameters.setWindowIcon(
            self.get_icon(QStyle.StandardPixmap.SP_MessageBoxQuestion)
        )
        self.ui.commandParameters.dlg = Ui_commandParametersDialog()
        self.ui.commandParameters.dlg.setupUi(self.ui.commandParameters)
        self.ui.commandParameters.setMaximumSize(0, 0)

        # MainWindow var
        self.docs = ""
        self.format_docstring = file_docs_format_string
        self.file_first_line = file_first_line
        self.docs_format_list = file_docs_format_list
        self.docs_filename = self.docs_format_list[0]
        self.docs_brief = self.docs_format_list[1]
        self.docs_version = self.docs_format_list[2]

        # code preview interaction
        self.user_resizing_code_preview_box = False
        self.ui.verticalDragIconPath = self.lib_root_path + "/cli_gen_tool/res/img/drag-vertical.svg"
        
        # command parameters dict keys list
        self.commandParametersKeys = command_parameters_dict_keys_list

        # default settings dict to regen cli_gen_tool.json if it becomes corrupt
        self.defaultGuiOpt = default_session_structure

        # cli opt db
        self.cliOpt = command_line_interface_options_structure
        # session db
        self.session = self.defaultGuiOpt
        # code preview db
        self.code_preview_dict = {"files": generated_filename_dict}

        # load cli_gen_tool (session) json if exists, else use default options
        self.session = self.load_cli_gen_tool_json(self.cli_gen_tool_json_path)
        # print pretty session json
        # session json contains only serializable items, safe to print
        print(json.dumps(self.session, indent=2))

        # parse config file
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

        self.ui.codePreview_1.viewport().installEventFilter(self)
        self.ui.codePreview_2.viewport().installEventFilter(self)
        

        # end MainWindow objects
        print("CLI generation tool ready.")
        # end __init__
    
    
    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        event_type = event.type()
        mouse_button = False        
        mouse_pos = 0
        code_preview_1 = self.ui.codePreview_1
        if event_type == event.MouseButtonPress or event_type == event.MouseButtonRelease:
            mouse_button = QMouseEvent(event).button()
            mouse_pos = QMouseEvent(event).position().toPoint()
        if event_type == event.MouseMove:
            mouse_pos = QMouseEvent(event).position().toPoint()
            
        if watched is code_preview_1.viewport():
            if event_type == event.MouseButtonPress and mouse_button == Qt.LeftButton:                
                selected_item = code_preview_1.itemAt(mouse_pos)                
                self.qrect = code_preview_1.visualItemRect(selected_item)
                qrect = self.qrect
                drag_box_qrect = self.get_vertical_drag_icon_geometry(self.qrect)
                
                if drag_box_qrect.contains(mouse_pos):                    
                    self.user_resizing_code_preview_box = True                                        
                    self.drag_resize_qsize = QSize(qrect.width(), qrect.height())
                    self.selected_drag_to_resize_item = selected_item
            
            if event_type == event.MouseMove and self.user_resizing_code_preview_box == True:
                self.resize_code_preview_tree_item(mouse_pos)
                                            
            if event_type == event.MouseButtonRelease and self.user_resizing_code_preview_box == True:
                self.user_resizing_code_preview_box = False
                self.resize_code_preview_tree_item(mouse_pos)
                
        return super().eventFilter(watched, event)


# loop
if __name__ == "__main__":
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
    app.processEvents()
    splash.timer = QTimer()
    splash.timer.setSingleShot(True)
    # GUI layout
    window = MainWindow(app)  # pass app object to external methods
    window.show()
    # Show app splash for `splashscreen_duration` /res/modules/dev_qol_var.py
    splash.timer.timeout.connect(splash.close)
    splash.timer.start(splashscreen_duration)
    # exit on user command
    sys.exit(app.exec())

# end of file
