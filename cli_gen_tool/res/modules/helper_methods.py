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

import datetime
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QVBoxLayout,
    QWidget, 
    QSizePolicy,
)
from PySide6.QtCore import Qt
from res.modules.dev_qol_var import version, file_docs_format_string
from res.modules.logging_setup import Logger


# helper method class
class HelperMethods(object):
    parent = ""

    def __init__(self):
        super(HelperMethods, self).__init__()
        HelperMethods.logger = Logger.get_child_logger(self.logger, __name__)
        HelperMethods.parent = self

    def create_qdialog(
        self,
        message,
        message_text_alignment,
        message_text_interaction_flags,
        window_title=None,
        buttons=None,
        button_text=None,
        icon=None,
    ):
        HelperMethods.logger.info(
            "message: "
            + message
            + ", windowtitle: "
            + window_title
            + ", buttons: "
            + str(buttons)
            + ", button text: "
            + str(button_text)
        )
        _buttons = []
        dlg = QDialog(HelperMethods.parent)        

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
        dlg.label = QLabel(dlg)                
        dlg.label.setMinimumSize(0,0)
        dlg.label.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
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
            dlg.layout.addWidget(dlg.button_box)
        dlg.setLayout(dlg.layout)
        if icon != None:
            dlg.setWindowIcon(icon)
        if window_title != None:
            dlg.setWindowTitle(window_title)
        ret = dlg.exec()
        return ret

    def generate_docstring_list_for_filename(self, filename, brief):
        docstring_list = []
        year = str(datetime.date.today())[0:4]
        date = datetime.date.today()
        docstring = file_docs_format_string.format(docs_version=version,docs_filename=filename,docs_brief=brief,docs_year=year,docs_date=date)
        docstring_list = docstring.split("\n")        
        return docstring_list

    def list_to_code_string(self, list):
        code_string = ""
        for line in list:
            code_string = code_string + line + "\n"
        return code_string    

    def get_icon(self, pixmapapi):
        return QWidget().style().standardIcon(pixmapapi)
