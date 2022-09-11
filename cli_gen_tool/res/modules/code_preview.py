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

# pyside imports
from PySide6.QtCore import QRect, QSize, Qt
from PySide6.QtGui import QMouseEvent, QTextCursor
from PySide6.QtWidgets import QHeaderView, QSizePolicy, QTreeWidgetItem, QTextBrowser

# external methods and resources
from res.modules.cli.clireadme import cliReadme
from res.modules.cli.config import cliConfig
from res.modules.cli.setup import cliSetup
from res.modules.cli.functions import cliFunctions
from res.modules.cli.parameters import cliParameters

# logging api
from res.modules.logging_setup import Logger

## each text browser in Code Preview is an instance of this class
class CodePreviewBrowser(QTextBrowser):
    # spawns a QTextBrowser with these settings
    def __init__(self, name):
        super(CodePreviewBrowser, self).__init__()
        self.setLineWrapMode(QTextBrowser.NoWrap)
        self.setReadOnly(True)
        self.setObjectName(str(name))
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.ensureCursorVisible()
        # let the user navigate to the hyperlinks provided in the readme
        if name == "README.md":
            self.setOpenExternalLinks(True)

    def resizeEvent(self, event):
        self.ensureCursorVisible()


# code preview methods
class CodePreview(cliReadme, cliConfig, cliSetup, cliFunctions, cliParameters, object):
    def __init__(self) -> None:
        super(CodePreview, self).__init__()
        CodePreview.logger = Logger.get_child_logger(self.logger, __name__)
        CodePreview.selected_text_widget = None
        cliReadme.__init__(self)
        cliConfig.__init__(self)
        cliSetup.__init__(self)
        cliFunctions.__init__(self)
        cliParameters.__init__(self)

    # refreshes the text in the code preview trees (also the text used to generate files)
    def update_code(self, file, item_string, place_cursor):
        CodePreview.logger.debug("update {filename}".format(filename=file))
        # update widgets
        if file == "README.md":
            self.readme_md(item_string, place_cursor)
        if file == "config.h":
            self.config_h(item_string, place_cursor)
        if file == "setup.h":
            self.setup_h(item_string, place_cursor)
        if file == "setup.cpp":
            self.setup_cpp(item_string, place_cursor)
        if file == "parameters.h":
            self.parameters_h(item_string, place_cursor)
        if file == "functions.h":
            self.functions_h(item_string, place_cursor)
        if file == "functions.cpp":
            self.functions_cpp(item_string, place_cursor)

    def display_initial_code_preview(self):
        self.readme_md(None, False)
        self.config_h(None, False)
        self.setup_h(None, False)
        self.setup_cpp(None, False)
        self.parameters_h(None, False)
        self.functions_h(None, False)
        self.functions_cpp(None, False)

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
            sb.setValue(sb.value() + (-(event.angleDelta().y() / 8)))

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

    # puts an invisible interaction hitbox around where someone would expect to be able to drag (vertical)
    def get_vertical_drag_icon_geometry(self, widget_qrect):
        return QRect(
            20,
            widget_qrect.y() + widget_qrect.height() - 4,
            widget_qrect.width() - 20,
            25,
        )

    # resizes code preview text browsers
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

    # highlights `item_string` in `text_widget`; centers the cursor on the highlighted text
    def set_text_cursor(self, text_widget, item_string):
        cursor = QTextCursor(text_widget.document().find(item_string))
        cursor.movePosition(cursor.EndOfLine)
        text_widget.setTextCursor(cursor)
        cursor.movePosition(cursor.StartOfLine, QTextCursor.KeepAnchor, 1)
        text_widget.setTextCursor(cursor)
        text_widget.ensureCursorVisible()

    # sets the text inside of code preview text browsers
    def set_code_string(self, filename, code_string, item_string, place_cursor=False):
        for tab in range(2):
            text_widget = self.code_preview_dict["files"][filename]["text_widget"][tab]
            text_widget.clear()
            if filename != "README.md":
                text_widget.setPlainText(code_string)
            else:
                text_widget.setMarkdown(code_string)
            if place_cursor == True:
                self.code_preview_dict["files"][filename]["tree_item"][tab].setExpanded(
                    True
                )
                self.set_text_cursor(text_widget, item_string)


# end of file
