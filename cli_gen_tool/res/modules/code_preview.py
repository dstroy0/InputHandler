##
# @file code_preview.py
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
from PySide6.QtWidgets import (
    QHeaderView,
    QTreeWidgetItem,
    QPlainTextEdit,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QTextCursor
from res.modules.dev_qol_var import (
    code_preview_text_line_offset,
    setup_h_filestring,
    setup_h_addcommand_string,
    setup_h_options_string_list,
)


# code preview methods
class CodePreview(object):
    # build code preview trees
    def build_code_preview_tree(self):
        for tab in range(0, 2):
            if tab == 0:
                tree = self.ui.codePreview_1
            else:
                tree = self.ui.codePreview_2
            tree.setHeaderLabels(["File", "Contents"])
            tree.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)
            tree.header().setSectionResizeMode(1, QHeaderView.ResizeToContents)
            tree.setColumnCount(2)
            for key in self.code_preview_dict["files"]:
                self.code_preview_dict["files"][key]["tree_item"][
                    tab
                ] = QTreeWidgetItem(tree, [key, ""])
                self.code_preview_dict["files"][key]["tree_item"][tab].setIcon(
                    0, self.ui.fileIcon
                )
                self.code_preview_dict["files"][key]["text_widget"][
                    tab
                ] = QPlainTextEdit()
                self.code_preview_dict["files"][key]["text_widget"][
                    tab
                ].setLineWrapMode(QPlainTextEdit.NoWrap)
                self.code_preview_dict["files"][key]["text_widget"][tab].setReadOnly(
                    True
                )
                self.code_preview_dict["files"][key]["text_widget"][tab].setObjectName(
                    str(key)
                )
                self.code_preview_dict["files"][key]["text_widget"][
                    tab
                ].setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
                self.code_preview_dict["files"][key]["contents_item"][
                    tab
                ] = QTreeWidgetItem(
                    self.code_preview_dict["files"][key]["tree_item"][tab]
                )
                tree.setItemWidget(
                    self.code_preview_dict["files"][key]["contents_item"][tab],
                    0,
                    self.code_preview_dict["files"][key]["text_widget"][tab],
                )
                self.code_preview_dict["files"][key]["contents_item"][
                    tab
                ].setFirstColumnSpanned(True)

    # end build_code_preview_tree()

    def set_text_cursor(self, text_widget, tree_object):
        object_string = ""
        if tree_object == None:
            object_string = self.sender().objectName()
        else:
            object_string = str(tree_object.data(4, 0))
            object_list = object_string.strip("\n").split(",")
            sub_dict = self.cliOpt["config"]["tree"]["items"][object_list[0]][
                int(object_list[1])
            ]["fields"]
            line_num = int(sub_dict[0])
            cursor = QTextCursor(
                text_widget.document().findBlockByLineNumber(
                    line_num + code_preview_text_line_offset
                )
            )
            text_widget.setTextCursor(cursor)

    def update_config_h(self, tree_object, place_cursor=False):
        self.code_preview_dict["files"]["config.h"]["file_lines_list"] = self.cliOpt[
            "config"
        ]["file_lines"]
        cfg_dict = self.cliOpt["config"]["tree"]["items"]
        for key in cfg_dict:
            for item in cfg_dict[key]:
                sub_dict = cfg_dict[key][item]["fields"]
                if sub_dict[4] == True or sub_dict[4] == False:
                    val = ""
                else:
                    val = sub_dict[4]
                    line = (
                        str(sub_dict[1])
                        + str(sub_dict[2])
                        + str(sub_dict[3])
                        + str(val)
                    )
                    self.code_preview_dict["files"]["config.h"]["file_lines_list"][
                        int(sub_dict[0])
                    ] = line
            code_string = self.list_to_code_string(
                self.code_preview_dict["files"]["config.h"]["file_lines_list"]
            )
            for tab in range(2):
                text_widget = self.code_preview_dict["files"]["config.h"][
                    "text_widget"
                ][tab]
                text_widget.clear()
                text_widget.setPlainText(code_string)
                if place_cursor == True:
                    self.set_text_cursor(text_widget, tree_object)
        # end update_config_h

    def update_setup_h(self, tree_object, place_cursor=False):
        file_lines = self.generate_docstring_list_for_filename("setup.h")
        self.code_preview_dict["files"]["setup.h"]["file_lines_list"] = []
        # process output
        buffer_size = self.cliOpt["process output"]["var"]["buffer size"]
        buffer_char = "{'\\0'}"
        # process parameters
        pprm = self.cliOpt["process parameters"]["var"]
        object_name = "inputHandler"
        process_name = pprm["process name"]
        process_eol = str(repr(pprm["end of line characters"])).strip("'")
        process_ipcc = pprm["input control char sequence"]
        process_wcc = pprm["wildcard char"]
        delim_seq = pprm["data delimiter sequences"]
        ststp_seq = pprm["start stop data delimiter sequences"]
        setup_string = "Setting up InputHandler..."

        # this can be a function
        num_delim_seq = len(delim_seq)
        delim_seq_lens = []
        for key in delim_seq:
            delim_seq_lens.append(len(delim_seq[key]))

        delim_seq_lens_string = "{"
        for i in range(len(delim_seq_lens)):
            delim_seq_lens_string = delim_seq_lens_string + str(delim_seq_lens[i])
            if i != len(delim_seq_lens)-1:
                delim_seq_lens_string = delim_seq_lens_string + ", "
        delim_seq_lens_string = delim_seq_lens_string + "}"

        delim_seqs_string = "{"
        for i in range(len(delim_seq)):
            delim_seqs_string = delim_seqs_string + '"' + delim_seq[i] + '"'
            if i != len(delim_seq)-1:
                delim_seqs_string = delim_seqs_string + ", "
        delim_seqs_string = delim_seqs_string + "}"

        # this can be a function
        num_ststp_pairs = len(ststp_seq) / 2
        ststp_seq_lens = []
        for key in ststp_seq:
            ststp_seq_lens.append(len(ststp_seq[key]))

        ststp_seq_lens_string = "{"
        for i in range(len(ststp_seq_lens)):
            ststp_seq_lens_string = ststp_seq_lens_string + str(ststp_seq_lens[i])
            if i != len(ststp_seq_lens)-1:
                ststp_seq_lens_string = ststp_seq_lens_string + ", "
        ststp_seq_lens_string = ststp_seq_lens_string + "}"

        ststp_seqs_string = "{"
        for i in range(len(ststp_seq)):
            ststp_seqs_string = ststp_seqs_string + '"' + ststp_seq[i] + '"'
            if i != len(ststp_seq)-1:
                ststp_seqs_string = ststp_seqs_string + ", "
        ststp_seqs_string = ststp_seqs_string + "}"

        command_list_string = ""
        for key in self.cliOpt["commands"]:
            # iterate through list
            command_parameters_name = (
                str(self.cliOpt["commands"][key]["functionName"]) + "_"
            )
            command_list_string = setup_h_addcommand_string.format(
                objectname=object_name, commandparametersname=command_parameters_name
            )
            
        options_string = ""        

        setup_h = setup_h_filestring.format(
            objectname=object_name,
            buffersize=buffer_size,
            bufferchar=buffer_char,
            processname=process_name,
            processeol=process_eol,
            processinputcontrolchar=process_ipcc,
            processwildcardchar=process_wcc,
            numdelimseq=num_delim_seq,
            delimseqlens=delim_seq_lens_string,
            delimseqs=delim_seqs_string,
            numstartstoppairs=num_ststp_pairs,
            startstopseqlens=ststp_seq_lens_string,
            startstopseqs=ststp_seqs_string,
            setupstring=setup_string,
            commandlist=command_list_string,
            options=options_string
        )
        
        code_string = self.list_to_code_string(file_lines)
        code_string = code_string + setup_h
        self.code_preview_dict["files"]["setup.h"]["file_lines_list"] = code_string.split("\n")
        for tab in range(2):
            text_widget = self.code_preview_dict["files"]["setup.h"]["text_widget"][tab]
            text_widget.clear()
            text_widget.setPlainText(code_string)
            if place_cursor == True:
                self.set_text_cursor(text_widget, tree_object)

    # refreshes the text in the code preview trees
    def update_code_preview_tree(self, tree_object):
        print("update code preview")
        # update widgets
        for key in self.code_preview_dict["files"]:
            if key == "config.h":
                self.update_config_h(tree_object, True)
            if key == "setup.h":
                self.update_setup_h(tree_object, True)

    def display_initial_code_preview(self):
        self.update_config_h(None, False)
        self.update_setup_h(None, False)

    # end update_code_preview_tree()
