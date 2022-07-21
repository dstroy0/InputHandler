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
    QSizePolicy,
)
from PySide6.QtCore import Qt, QRect, QSize
from PySide6.QtGui import QTextCursor, QMouseEvent
from res.modules.dev_qol_var import (
    code_preview_text_line_offset,
    setup_h_filestring,
    setup_h_addcommand_string,
    setup_h_options_string_list,
    setup_h_output_buffer_string,
    setup_h_constructor_string,
    setup_h_class_output_string,
)


# code preview methods
class CodePreview(object):
    def code_preview_events(self, watched, event, event_type, mouse_button, mouse_pos):
        if watched == self.ui.codePreview_1.viewport():
            code_preview = self.ui.codePreview_1
        elif watched == self.ui.codePreview_2.viewport():
            code_preview = self.ui.codePreview_2

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
            8,
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
                ] = QPlainTextEdit()
                text_widget = self.code_preview_dict["files"][key]["text_widget"][tab]
                text_widget.setLineWrapMode(QPlainTextEdit.NoWrap)
                text_widget.setReadOnly(True)
                text_widget.setObjectName(str(key))
                text_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
                text_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
                text_widget.setSizePolicy(
                    QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding
                )
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

    def set_text_cursor(self, text_widget, tree_object):
        object_string = ""
        if tree_object == None:
            object_string = self.sender().objectName()
        else:
            try:
                # QTreeWidgetItem
                object_string = str(tree_object.data(4, 0))
            except:
                # QTableWidgetItem
                object_string = str(tree_object.tableWidget().objectName())
        object_list = object_string.strip("\n").split(",")
        line_num = 0
        if object_list[0] == "process output" or object_list[0] == "process name":
            code_list = self.code_preview_dict["files"]["setup.h"]["file_lines_list"]
            for i in range(len(code_list)):
                if object_list[2] in code_list[i]:
                    line_num = i
                    break
        elif object_list[0] == "process parameters":
            code_list = self.code_preview_dict["files"]["setup.h"]["file_lines_list"]
            for i in range(len(code_list)):
                if object_list[2] in code_list[i]:
                    line_num = i
                    break
        else:
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
                line = str(sub_dict[1]) + str(sub_dict[2]) + str(sub_dict[3]) + str(val)
                self.code_preview_dict["files"]["config.h"]["file_lines_list"][
                    int(sub_dict[0])
                ] = line
        code_string = self.list_to_code_string(
            self.code_preview_dict["files"]["config.h"]["file_lines_list"]
        )
        for tab in range(2):
            text_widget = self.code_preview_dict["files"]["config.h"]["text_widget"][
                tab
            ]
            text_widget.clear()
            text_widget.setPlainText(code_string)
            if place_cursor == True:
                self.set_text_cursor(text_widget, tree_object)
        # end update_config_h

    def update_setup_h_string_helper(self, seq):
        num_seq = len(seq)
        seq_lens_string = "{"
        seqs_string = "{"
        seq_lens = []
        seqs = []
        for key in seq:
            seq_lens.append(len(seq[key]))
            seqs.append(seq[key])
        for i in range(len(seq_lens)):
            seq_lens_string = seq_lens_string + str(seq_lens[i])
            seqs_string = (
                seqs_string + '"' + str(seqs[i]).strip("'").replace('"', '\\"') + '"'
            )
            if i != len(seq_lens) - 1:
                seq_lens_string = seq_lens_string + ", "
                seqs_string = seqs_string + ", "
        seq_lens_string = seq_lens_string + "}"
        seqs_string = seqs_string + "}"
        return [num_seq, seq_lens_string, seqs_string]

    def update_setup_h(self, tree_object, place_cursor=False):
        file_lines = self.generate_docstring_list_for_filename("setup.h")
        self.code_preview_dict["files"]["setup.h"]["file_lines_list"] = []
        # process output
        buffer_size = self.cliOpt["process output"]["var"]["buffer size"]
        buffer_char = "{'\\0'}"
        object_name = "inputHandler"
        output_buffer = setup_h_output_buffer_string.format(
            buffersize=buffer_size, bufferchar=buffer_char
        )
        class_constructor = setup_h_constructor_string.format(
            objectname=object_name, classoutput=setup_h_class_output_string
        )
        if int(buffer_size) == 0:
            output_buffer = ""
            class_constructor = setup_h_constructor_string.format(
                objectname=object_name, classoutput=""
            )
        # process parameters
        pprm = self.cliOpt["process parameters"]["var"]
        process_name = pprm["process name"]
        process_eol = str(repr(pprm["end of line characters"])).strip("'")
        process_ipcc = pprm["input control char sequence"]
        process_wcc = pprm["wildcard char"]
        delim_seq = pprm["data delimiter sequences"]
        ststp_seq = pprm["start stop data delimiter sequences"]
        setup_string = "Setting up InputHandler..."

        result = self.update_setup_h_string_helper(delim_seq)
        num_delim_seq = result[0]
        delim_seq_lens_string = result[1]
        delim_seqs_string = result[2]

        result = self.update_setup_h_string_helper(ststp_seq)
        num_ststp_pairs = result[0] / 2
        ststp_seq_lens_string = result[1]
        ststp_seqs_string = result[2]

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
            outputbuffer=output_buffer,
            constructor=class_constructor,
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
            options=options_string,
        )

        code_string = self.list_to_code_string(file_lines)
        code_string = code_string + setup_h
        self.code_preview_dict["files"]["setup.h"][
            "file_lines_list"
        ] = code_string.split("\n")
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
