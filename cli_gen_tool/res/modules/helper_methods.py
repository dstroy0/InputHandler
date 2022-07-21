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
from PySide6.QtWidgets import QDialog, QHBoxLayout, QLabel, QDialogButtonBox, QVBoxLayout, QMessageBox
from res.modules.dev_qol_var import version

# helper method class
class HelperMethods(object):
    def create_popup_dialog_box(self, message, window_title=None, icon=None):
        print(message)
        # create popup
        dlg = QDialog(self)
        dlg.layout = QHBoxLayout()
        label = QLabel(message)
        dlg.layout.addWidget(label)
        dlg.setLayout(dlg.layout)
        if icon != None:
            dlg.setWindowIcon(icon)
        if window_title != None:
            dlg.setWindowTitle(window_title)
        dlg.exec()
        
    def create_popup_dialog_box_with_buttons(self, message, window_title=None, icon=None):
        print(message)
        # create popup        
        dlg = QMessageBox(self)
        dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)        
        dlg.setText(message)                   
        if icon != None:
            dlg.setWindowIcon(icon)
        if window_title != None:
            dlg.setWindowTitle(window_title)
        ret = dlg.exec()
        return ret

    def generate_docstring_list_for_filename(self, filename):
        docstring_list = []
        docstring_list.append(self.file_first_line.strip("\n"))
        self.update_file_docstring(
            filename, "autogenerated InputHandler CLI " + filename, str(version)
        )
        docs_list = self.docs.split("\n")
        # docs_list.pop()
        for line in docs_list:
            docstring_list.append(line)
        return docstring_list

    def list_to_code_string(self, list):
        code_string = ""
        for line in list:
            code_string = code_string + line + "\n"
        return code_string

    def update_file_docstring(self, file, brief, version):
        self.docs_format_list[0] = file
        self.docs_format_list[1] = brief
        self.docs_format_list[2] = version
        self.docs = self.format_docstring.format(*self.docs_format_list)

    def get_icon(self, pixmapapi):
        return self.style().standardIcon(pixmapapi)
