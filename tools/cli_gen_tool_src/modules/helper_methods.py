##
# @file helper_methods.py
# @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
# @brief MainWindow external methods
# @version 1.0
# @date 2022-07-08
# @copyright Copyright (c) 2022
# Copyright (C) 2022 Douglas Quigg (dstroy0) <dquigg123@gmail.com>
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 3 as published by the Free Software Foundation.

from __future__ import absolute_import

# pyside imports
from PySide6.QtGui import QScreen
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QVBoxLayout,
    QWidget,
    QSizePolicy,
)
from PySide6.QtCore import Qt, QPoint

# logging api
from modules.logging_setup import Logger


# helper method class
class HelperMethods(object):
    ## instance
    parent = ""
    mainwindow_screen = ""
    ## the constructor
    def __init__(self):
        super(HelperMethods, self).__init__()
        HelperMethods.logger = self.get_child_logger(__name__)
        HelperMethods.parent = self
        HelperMethods.mainwindow_screen = self.qscreen

    ## spawn a dialog box
    def create_qdialog(
        self,
        message,
        message_text_alignment,
        message_text_interaction_flags,
        window_title=None,
        buttons=None,
        button_text=None,
        icon=None,
        screen=None,
    ):
        HelperMethods.logger.info("create qdialog: " + window_title)
        _buttons = []
        dlg = QDialog(self)

        def button_box_clicked(button):
            _match = 0
            for i in range(len(_buttons)):
                if button == _buttons[i]:
                    _match = i
                    break
            b = QDialogButtonBox.StandardButton
            if buttons[_match] == b.Ok:
                dlg.accept()
            if buttons[_match] == b.Cancel:
                dlg.reject()
            if buttons[_match] == b.Save:
                dlg.done(2)
            if buttons[_match] == b.Close:
                dlg.done(3)

        # create popup
        dlg.layout = QVBoxLayout()
        dlg.label = QLabel()
        dlg.label.setMinimumSize(0, 15)
        dlg.label.setSizePolicy(
            QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding
        )
        dlg.label.setTextFormat(Qt.AutoText)
        dlg.label.setText(message)
        dlg.label.setAlignment(message_text_alignment)

        if type(message_text_interaction_flags) == Qt.TextInteractionFlag:
            dlg.label.setTextInteractionFlags(message_text_interaction_flags)
        elif type(message_text_interaction_flags) == Qt.TextInteractionFlags:
            dlg.label.setTextInteractionFlags(message_text_interaction_flags)
        dlg.label.setOpenExternalLinks(True)
        dlg.layout.addWidget(dlg.label)

        if buttons != None:
            dlg.button_box = QDialogButtonBox(dlg)
            idx = 0
            for item in buttons:
                _button = dlg.button_box.addButton(item)
                if button_text[idx] != "":
                    _button.setText(button_text[idx])
                _buttons.append(_button)
                idx += 1
            dlg.button_box.clicked.connect(button_box_clicked)
            dlg.button_box.setCenterButtons(True)
            dlg.layout.addWidget(dlg.button_box)
        dlg.setLayout(dlg.layout)
        if icon != None:
            dlg.setWindowIcon(icon)
        if window_title != None:
            dlg.setWindowTitle(window_title)
        dlg.setWindowFlags(dlg.windowFlags() | Qt.WindowStaysOnTopHint)

        dlg.activateWindow()  # brings focus to the popup

        # center dialog on screen
        if screen == None:
            _qscreen = self.mainwindow_screen
        else:
            _qscreen = HelperMethods.parent.qscreen

        _fg = dlg.frameGeometry()
        center_point = _qscreen.availableGeometry().center()
        center_point.setX(center_point.x() - (_fg.x() / 2))
        center_point.setY(center_point.y() - (_fg.y() / 2))
        _fg.moveCenter(center_point)
        self.logger.info("Creating QDialog on: " + _qscreen.name())
        ret = dlg.exec()  # return the dialog exit code
        return ret

    ## get builtin icon
    def get_icon(self, pixmapapi):
        return QWidget().style().standardIcon(pixmapapi)


# end of file
