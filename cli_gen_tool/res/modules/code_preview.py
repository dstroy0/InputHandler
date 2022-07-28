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

from PySide6.QtCore import QRect, QSize, Qt
from PySide6.QtGui import QMouseEvent, QTextCursor
from PySide6.QtWidgets import QHeaderView, QPlainTextEdit, QSizePolicy, QTreeWidgetItem
from res.modules.dev_qol_var import (
    filestring_db,
)

from res.modules.logging_setup import Logger


class CodePreviewBrowser(QPlainTextEdit):
    def __init__(self, name):
        super(CodePreviewBrowser, self).__init__()
        self.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.setReadOnly(True)
        self.setObjectName(str(name))
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.setCenterOnScroll(True)

    def resizeEvent(self, event):
        self.centerCursor()


# code preview methods
class CodePreview(object):
    def __init__(self) -> None:
        super(CodePreview, self).__init__()
        CodePreview.logger = Logger.get_child_logger(self.logger, __name__)
        CodePreview.selected_text_widget = None

    def code_preview_events(self, watched, event, event_type, mouse_button, mouse_pos):
        if watched == self.ui.codePreview_1.viewport():
            code_preview = self.ui.codePreview_1
        elif watched == self.ui.codePreview_2.viewport():
            code_preview = self.ui.codePreview_2
        else:
            return
        if (
            event_type == event.MouseButtonPress
            or event_type == event.MouseButtonRelease
        ):
            mouse_button = QMouseEvent(event).button()
            mouse_pos = QMouseEvent(event).position().toPoint()
        if event_type == event.MouseMove:
            mouse_pos = QMouseEvent(event).position().toPoint()

        if watched == code_preview.viewport():
            if (
                event_type == event.HoverEnter
                or event_type == event.HoverMove
                or event_type == event.HoverLeave
            ):
                viewportpos = code_preview.viewport().mapFromGlobal(mouse_pos)
                selected_item = code_preview.itemAt(viewportpos)

                if selected_item and selected_item.childCount() == 0:
                    CodePreview.selected_text_widget = (
                        selected_item.treeWidget().itemWidget(selected_item, 0)
                    )

                    drag_box_qrect = self.get_vertical_drag_icon_geometry(
                        code_preview.visualItemRect(selected_item)
                    )
                    if drag_box_qrect.contains(viewportpos):
                        self.setCursor(Qt.CursorShape.SizeVerCursor)
                    elif (
                        not drag_box_qrect.contains(viewportpos)
                        and self.user_resizing_code_preview_box == False
                    ):
                        self.setCursor(Qt.CursorShape.ArrowCursor)
                else:
                    # no item being hovered over
                    self.setCursor(Qt.CursorShape.ArrowCursor)

        if event_type == event.Wheel and CodePreview.selected_text_widget != None:
            sb = CodePreview.selected_text_widget.verticalScrollBar()
            sb.setValue(sb.value() + (-(event.angleDelta().y() / 8 / 15)))

        if event_type == event.MouseButtonPress and mouse_button == Qt.LeftButton:
            if watched is code_preview.viewport():
                selected_item = code_preview.itemAt(mouse_pos)
                self.qrect = code_preview.visualItemRect(selected_item)
                qrect = self.qrect

                drag_box_qrect = self.get_vertical_drag_icon_geometry(self.qrect)
                self.init_mouse_pos = mouse_pos
                self.init_height = qrect.height()
                if drag_box_qrect.contains(mouse_pos):
                    self.setCursor(Qt.CursorShape.SizeVerCursor)
                    self.user_resizing_code_preview_box = True
                    self.drag_resize_qsize = QSize(qrect.width(), qrect.height())
                    self.selected_drag_to_resize_item = selected_item

        if (
            event_type == event.MouseMove
            and self.user_resizing_code_preview_box == True
        ):
            self.resize_code_preview_tree_item(mouse_pos)

        if (
            event_type == event.MouseButtonRelease
            and self.user_resizing_code_preview_box == True
        ):
            self.user_resizing_code_preview_box = False
            self.resize_code_preview_tree_item(mouse_pos)
            self.setCursor(Qt.CursorShape.ArrowCursor)

    def get_vertical_drag_icon_geometry(self, widget_qrect):
        return QRect(
            20,
            widget_qrect.y() + widget_qrect.height() - 4,
            widget_qrect.width() - 20,
            25,
        )

    def resize_code_preview_tree_item(self, mouse_pos):
        y_axis = self.init_height + (mouse_pos.y() - self.init_mouse_pos.y())
        self.drag_resize_qsize.setHeight(y_axis)
        self.selected_drag_to_resize_item.setSizeHint(0, self.drag_resize_qsize)
        widget_size = (
            self.selected_drag_to_resize_item.treeWidget()
            .itemWidget(self.selected_drag_to_resize_item, 0)
            .sizeHint()
        )
        widget_size.setWidth(self.qrect.width() - 40)
        if y_axis >= 192:
            widget_size.setHeight(y_axis)
            self.selected_drag_to_resize_item.treeWidget().itemWidget(
                self.selected_drag_to_resize_item, 0
            ).resize(widget_size)
            self.selected_drag_to_resize_item.treeWidget().resize(widget_size)

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
                parent = self.code_preview_dict["files"][key]["tree_item"][tab]
                parent.setIcon(0, self.ui.fileIcon)
                self.code_preview_dict["files"][key]["text_widget"][
                    tab
                ] = CodePreviewBrowser(key)
                text_widget = self.code_preview_dict["files"][key]["text_widget"][tab]

                self.code_preview_dict["files"][key]["contents_item"][
                    tab
                ] = QTreeWidgetItem(parent)
                text_widget_container = self.code_preview_dict["files"][key][
                    "contents_item"
                ][tab]
                text_widget_container.setFirstColumnSpanned(True)
                text_widget_container.drag_box_qrect = tree.visualItemRect(
                    text_widget_container
                )
                tree.setItemWidget(text_widget_container, 0, text_widget)

    # end build_code_preview_tree()

    def set_text_cursor(self, text_widget, item_string):
        cursor = QTextCursor(text_widget.document().find(item_string))
        cursor.movePosition(cursor.EndOfLine)
        text_widget.setTextCursor(cursor)
        cursor.movePosition(cursor.StartOfLine, QTextCursor.KeepAnchor, 1)
        text_widget.setTextCursor(cursor)
        text_widget.centerCursor()

    def set_code_string(self, filename, code_string, item_string, place_cursor=False):
        for tab in range(2):
            text_widget = self.code_preview_dict["files"][filename]["text_widget"][tab]
            text_widget.clear()
            text_widget.setPlainText(code_string)
            if place_cursor == True:
                self.code_preview_dict["files"][filename]["tree_item"][tab].setExpanded(
                    True
                )
                self.set_text_cursor(text_widget, item_string)

    def update_config_h(self, item_string, place_cursor=False):
        self.code_preview_dict["files"]["config.h"]["file_lines_list"] = self.cliOpt[
            "config"
        ]["file_lines"]
        cfg_dict = self.cliOpt["config"]["tree"]["items"]
        for key in cfg_dict:
            for item in cfg_dict[key]:
                if "QComboBox" not in str(item) and "QTreeWidgetItem" not in str(item):
                    sub_dict = cfg_dict[key][item]["fields"]
                    if sub_dict[3] == True or sub_dict[3] == False:
                        val = ""
                    else:
                        val = sub_dict[3]
                    line = str(sub_dict[1]) + "#define " + str(sub_dict[2]) + str(val)
                    self.code_preview_dict["files"]["config.h"]["file_lines_list"][
                        int(sub_dict[0])
                    ] = line
        code_string = self.list_to_code_string(
            self.code_preview_dict["files"]["config.h"]["file_lines_list"]
        )
        self.set_code_string("config.h", code_string, item_string, place_cursor)
        # end update_config_h

    def update_setup_h(self, item_string, place_cursor=False):
        def sequence_string_helper(seq):
            num_seq = len(seq)
            seq_lens_string = "{"
            seqs_string = "{"
            seq_lens = []
            seqs = []
            for key in seq:
                delim_str = str(seq[key]).strip("'")
                delim_str_len = len(delim_str)

                seq_lens.append(delim_str_len)
                seqs.append(seq[key])
            for i in range(len(seq_lens)):
                seq_lens_string = seq_lens_string + str(seq_lens[i])
                seqs_string = (
                    seqs_string
                    + '"'
                    + str(repr(seqs[i])).strip("'").replace("\\\\", "\\")
                    + '"'
                )
                if i != len(seq_lens) - 1:
                    seq_lens_string = seq_lens_string + ", "
                    seqs_string = seqs_string + ", "
            seq_lens_string = seq_lens_string + "}"
            seqs_string = seqs_string + "}"
            return [num_seq, seq_lens_string, seqs_string]

        file_lines = self.generate_docstring_list_for_filename(
            "setup.h", "InputHandler autogenerated setup.h"
        )
        self.code_preview_dict["files"]["setup.h"]["file_lines_list"] = []
        # process output
        output_buffer_name = "InputHandler_output_buffer"
        buffer_size = self.cliOpt["process output"]["var"]["buffer size"]
        buffer_char = "{'\\0'}"
        object_name = "inputHandler"
        output_buffer = filestring_db["setup"]["h"]["filestring components"][
            "outputbuffer"
        ].format(
            outputbuffername=output_buffer_name,
            buffersize=buffer_size,
            bufferchar=buffer_char,
        )
        class_output = filestring_db["setup"]["h"]["filestring components"][
            "classoutput"
        ].format(input_prm="input_prm", outputbuffer="InputHandler_output_buffer")

        setup_function_entry_string = "Setting up InputHandler..."

        class_constructor = filestring_db["setup"]["h"]["filestring components"][
            "constructor"
        ].format(objectname=object_name, classoutput=class_output)
        if int(buffer_size) == 0:
            output_buffer = ""
            class_constructor = filestring_db["setup"]["h"]["filestring components"][
                "constructor"
            ].format(objectname=object_name, classoutput="")

        # process parameters
        pprm = self.cliOpt["process parameters"]["var"]
        process_name = pprm["process name"]
        process_eol = (
            str(repr(pprm["end of line characters"])).strip("'").replace("\\\\", "\\")
        )
        process_ipcc = (
            str(repr(pprm["input control char sequence"]))
            .strip("'")
            .replace("\\\\", "\\")
        )
        process_wcc = str(repr(pprm["wildcard char"])).strip("'").replace("\\\\", "\\")
        delim_seq = pprm["data delimiter sequences"]
        ststp_seq = pprm["start stop data delimiter sequences"]

        setup_function_entry = ""
        stream_string = self.cliOpt["process output"]["var"]["output stream"]
        if stream_string != "" and stream_string != None and int(buffer_size) != 0:
            setup_function_entry = filestring_db["setup"]["h"]["filestring components"][
                "setup function output"
            ]["stream"].format(
                stream=self.cliOpt["process output"]["var"]["output stream"],
                setupstring=setup_function_entry_string,
            )
        elif stream_string == "" or stream_string == None and int(buffer_size) != 0:
            setup_function_entry = filestring_db["setup"]["h"]["filestring components"][
                "setup function output"
            ]["buffer"].format(
                outputbuffer=output_buffer_name,
                setupstring=setup_function_entry_string,
            )

        default_function_string = ""
        if self.cliOpt["builtin methods"]["var"]["defaultFunction"] == True:
            default_function_string = filestring_db["setup"]["h"][
                "filestring components"
            ]["defaultFunction"]["call"].format(
                objectname=object_name, defaultfunctionname="unrecognized"
            )

        result = sequence_string_helper(delim_seq)
        num_delim_seq = result[0]
        delim_seq_lens_string = result[1]
        delim_seqs_string = result[2]

        result = sequence_string_helper(ststp_seq)
        num_ststp_pairs = int(result[0] / 2)
        ststp_seq_lens_string = result[1]
        ststp_seqs_string = result[2]

        command_list_string = ""
        for key in self.cliOpt["commands"]:
            # iterate through list
            command_parameters_name = (
                str(self.cliOpt["commands"][key]["functionName"]) + "_"
            )
            command_list_string = filestring_db["setup"]["h"]["filestring components"][
                "addCommand"
            ]["call"].format(
                objectname=object_name, commandparametersname=command_parameters_name
            )

        begin_string = filestring_db["setup"]["h"]["filestring components"]["begin"][
            "call"
        ].format(objectname=object_name)

        options_string = ""

        setup_h = filestring_db["setup"]["h"]["filestring"].format(
            objectname=object_name,
            outputbuffer=output_buffer,
            constructor=class_constructor,
            defaultfunction=default_function_string,
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
            setupfunctionentry=setup_function_entry,
            commandlist=command_list_string,
            begin=begin_string,
            options=options_string,
        )

        code_string = self.list_to_code_string(file_lines)
        code_string = code_string + setup_h
        self.code_preview_dict["files"]["setup.h"][
            "file_lines_list"
        ] = code_string.split("\n")
        self.set_code_string("setup.h", code_string, item_string, place_cursor)

    # refreshes the text in the code preview trees
    def update_code_preview(self, file, item_string, place_cursor):
        CodePreview.logger.info("update {filename} preview".format(filename=file))
        # update widgets
        if file == "config.h":
            self.update_config_h(item_string, place_cursor)
        if file == "setup.h":
            self.update_setup_h(item_string, place_cursor)

    def display_initial_code_preview(self):
        self.update_config_h(None, False)
        self.update_setup_h(None, False)

    # end update_code_preview_tree()
