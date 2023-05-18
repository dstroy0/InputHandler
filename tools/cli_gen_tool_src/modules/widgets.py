from __future__ import absolute_import

import copy
import json
from collections import OrderedDict

from PySide6.QtCore import (
    QRect,
    QSize,
    Qt,
    QEvent,
    QObject,
    QUrl,
    Slot,
    QPoint,
    QByteArray,
)
from PySide6.QtGui import (
    QMouseEvent,
    QTextCursor,
    QDesktopServices,
    QCursor,
    QPaintEvent,
    QPainter,
    QColor,
    QTextFormat,
    QAction,
    QKeySequence,
)
from PySide6.QtWidgets import (
    QSizePolicy,
    QTreeWidgetItem,
    QApplication,
    QWidget,
    QTextEdit,
    QPlainTextEdit,
    QTreeWidget,
    QAbstractItemView,
    QStyle,
    QHeaderView,
    QPushButton,
    QHBoxLayout,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QMenu,
    QDialogButtonBox,
    QDialog,
    QComboBox,
)

from modules.data_models import dataModels
from modules.display_models import displayModels
from modules.logging_setup import Logger


class TableButtonBox(QWidget):
    """up/down/remove row button widget for qtablewidget

    Args:
        QWidget (class): base class being specialized
    """

    def __init__(self, parent) -> None:
        super(TableButtonBox, self).__init__()
        self.setParent(parent)
        self.table = parent
        self.widget_layout = QHBoxLayout(parent)
        self.up_icn = self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowUp)
        self.dn_icn = self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowDown)
        self.del_row_icn = self.style().standardIcon(
            QStyle.StandardPixmap.SP_BrowserStop
        )
        self.up_btn = QPushButton()
        self.up_btn.setFixedSize(
            self.up_icn.actualSize(self.up_icn.availableSizes()[0])
        )
        self.up_btn.setText("")
        self.up_btn.setToolTip("Move argument up")
        self.up_btn.setIcon(self.up_icn)
        self.dn_btn = QPushButton()
        self.dn_btn.setFixedSize(
            self.dn_icn.actualSize(self.dn_icn.availableSizes()[0])
        )
        self.dn_btn.setText("")
        self.dn_btn.setToolTip("Move argument down")
        self.dn_btn.setIcon(self.dn_icn)
        self.del_row_btn = QPushButton()
        self.del_row_btn.setFixedSize(
            self.dn_icn.actualSize(self.dn_icn.availableSizes()[0])
        )
        self.del_row_btn.setText("")
        self.del_row_btn.setToolTip("Delete argument")
        self.del_row_btn.setIcon(self.del_row_icn)
        self.widget_layout.addWidget(self.up_btn)
        self.widget_layout.addWidget(self.dn_btn)
        self.widget_layout.addWidget(self.del_row_btn)
        self.setLayout(self.widget_layout)
        self.up_btn.clicked.connect(self.move_row_up)
        self.dn_btn.clicked.connect(self.move_row_down)
        self.del_row_btn.clicked.connect(self.remove_row)

    def row(self):
        return self.table.row(
            self.table.itemAt(
                self.table.viewport().mapFromGlobal(self.table._cursor.pos())
            )
        )

    def move_row_up(self):
        row = self.row()
        sourceItems = self.takeRow(row)
        destItems = self.takeRow(row - 1)
        self.setRow(row - 1, sourceItems)
        self.setRow(row, destItems)

    def move_row_down(self, row: int = None):
        row = self.row()
        sourceItems = self.takeRow(row)
        destItems = self.takeRow(row + 1)
        self.setRow(row + 1, sourceItems)
        self.setRow(row, destItems)

    def remove_row(self):
        row = self.row()
        self.table.removeRow(row)
        self.table.setCurrentCell(row - 1, 0)

    def takeRow(self, row: int) -> list:
        rowItems = []
        table = self.table
        for col in range(table.columnCount()):
            rowItems.append(table.takeItem(row, col))
        return rowItems

    def setRow(self, row: int, rowItems: list):
        table = self.table
        for col in range(table.columnCount()):
            table.setItem(row, col, rowItems[col])


class CodePreviewWidget(
    QTreeWidget,
    QTreeWidgetItem,
):
    """This is a tree that contains the code preview widgets

    Args:
        QTreeWidget (QWidget): A convenience class
        QTreeWidgetItem (QWidget): children of QTreeWidget
    """

    ## QCursor
    _cursor = ""

    def __init__(self, parent, container, code_preview_dict, cliopt) -> None:
        """the constructor

        Args:
            parent (QWidget): parent widget
            container (QPane): tree container
            code_preview_dict (dict): dict of filestrings
            cliopt (dict): CLI options dict
        """
        super(CodePreviewWidget, self).__init__()

        self.setParent(container)
        self.collapse_button = container.collapse_button
        self.logger = parent.codegen_logger
        self._cursor = parent.qcursor
        self.readme_md = parent.readme_md
        self.config_h = parent.config_h
        self.cli_h = parent.cli_h

        self.parameters_h = parent.parameters_h
        self.functions_h = parent.functions_h

        self.cli_options = parent.cli_options
        self.input_config_file_lines = parent.input_config_file_lines
        self.minimum_file_len = parent.minimum_file_len

        self.fileicon = (
            QWidget().style().standardIcon(QStyle.StandardPixmap.SP_FileIcon)
        )
        self.text_widgets = {}
        self.selected_text_widget = None

        self._parent = parent
        self.app = parent.app

        self.code_preview_dict = code_preview_dict
        self.active_item = self.invisibleRootItem()

        self.user_resizing_code_preview_box = False
        self.selected_drag_to_resize_item = None
        self.init_mouse_pos = QPoint()
        self.init_height = 0

        self.setHeaderLabel("Code Preview")
        self.setColumnCount(2)
        self.setColumnHidden(1, True)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.header().setSectionResizeMode(QHeaderView.Stretch)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumHeight(100)
        self.setMinimumWidth(100)
        for i in range(self.columnCount() - 1):
            self.header().setSectionResizeMode(i, QHeaderView.ResizeToContents)
            self.header().setSectionResizeMode(i, QHeaderView.Stretch)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setSelectionMode(QAbstractItemView.NoSelection)
        self.setFocusPolicy(Qt.NoFocus)

        self.build_tree()

        self.clicked.connect(self.which_clicked)
        self.pressed.connect(self.which_pressed)
        self.itemChanged.connect(self.item_changed)
        self.currentItemChanged.connect(self.item_changed)

        self.itemSelectionChanged.connect(self.button_toggles)
        self.itemClicked.connect(self.button_toggles)
        self.itemCollapsed.connect(self.button_toggles)
        self.itemExpanded.connect(self.button_toggles)
        self.itemExpanded.connect(self.item_expanded)
        self.collapse_button.clicked.connect(self.tree_expander)
        self.button_toggles()

    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key_Escape:
            self.selectionModel().clearSelection()
        return super().keyPressEvent(event)

    def item_expanded(self, item: QTreeWidgetItem) -> None:
        """expand only QTreeWidgetItems that are expandable

        Args:
            item (QTreeWidgetItem): the item highlighted at the time of the collapse button interaction
        """
        self.active_item = item
        if self.active_item == self.invisibleRootItem():
            self.selected_text_widget = None
            return
        if item.data(0, 0) == None:
            self.selected_text_widget = self.text_widgets[
                self.active_item.parent().data(0, 0)
            ]["widget"]
        else:
            self.selected_text_widget = self.text_widgets[self.active_item.data(0, 0)][
                "widget"
            ]

    def tree_expander(self):
        """collapse button interaction"""
        text = self.collapse_button.text()
        if text == "Collapse All":
            self.collapseAll()
        elif text == "Expand All":
            self.expandAll()
        elif text == "Collapse":
            item = self.active_item
            if item.data(0, 0) == None:
                item = item.parent()
            item.setExpanded(False)
        elif text == "Expand":
            item = self.active_item
            if item.data(0, 0) == None:
                item = item.parent()
            self.active_item.setExpanded(True)

    def button_toggles(self):
        """tree button toggles"""
        if self.active_item == self.invisibleRootItem():
            if self.active_item.isExpanded():
                self.collapse_button.setText("Collapse All")
            else:
                self.collapse_button.setText("Expand All")
        else:
            item = self.active_item
            if item.data(0, 0) == None:
                item = self.active_item.parent()
            if item.isExpanded():
                self.collapse_button.setText("Collapse")
            else:
                self.collapse_button.setText("Expand")

    def initial_code_preview(self):
        """make initial code preview available to user"""
        code_string = self.readme_md()
        self.code_preview_dict["files"]["README.md"]["file_string"] = code_string
        self.set_code_string("README.md", code_string, None, False)
        self.code_preview_dict["files"]["README.md"]["file_lines_list"] = []
        self.code_preview_dict["files"]["README.md"][
            "file_lines_list"
        ] = code_string.split("\n")

        code_string = self.config_h()
        self.code_preview_dict["files"]["config.h"]["file_string"] = code_string
        self.set_code_string("config.h", code_string, None, False)
        self.code_preview_dict["files"]["config.h"]["file_lines_list"] = []
        self.code_preview_dict["files"]["config.h"][
            "file_lines_list"
        ] = code_string.split("\n")

        code_string = self.cli_h()
        self.code_preview_dict["files"]["CLI.h"]["file_string"] = code_string
        self.set_code_string("CLI.h", code_string, None, False)
        self.code_preview_dict["files"]["CLI.h"]["file_lines_list"] = []
        self.code_preview_dict["files"]["CLI.h"]["file_lines_list"] = code_string.split(
            "\n"
        )

        code_string = self.parameters_h()
        self.code_preview_dict["files"]["parameters.h"]["file_string"] = code_string
        self.set_code_string("parameters.h", code_string, None, False)
        self.code_preview_dict["files"]["parameters.h"]["file_lines_list"] = []
        self.code_preview_dict["files"]["parameters.h"][
            "file_lines_list"
        ] = code_string.split("\n")

        code_string = self.functions_h()
        self.code_preview_dict["files"]["functions.h"]["file_string"] = code_string
        self.set_code_string("functions.h", code_string, None, False)
        self.code_preview_dict["files"]["functions.h"]["file_lines_list"] = []
        self.code_preview_dict["files"]["functions.h"][
            "file_lines_list"
        ] = code_string.split("\n")

    def item_changed(self, item, column):
        """tree item iteraction sentinel

        Args:
            item (QTreeWidgetItem): the item interacted with
            column (int): column of item interacted with
        """
        self.active_item = item
        if item.data(0, 0) == None:
            self.selected_text_widget = self.text_widgets[
                self.active_item.parent().data(0, 0)
            ]["widget"]
        else:
            self.selected_text_widget = self.text_widgets[self.active_item.data(0, 0)][
                "widget"
            ]

    def which_pressed(self):
        """item interaction detection"""
        self.active_item = self.itemFromIndex(self.currentIndex())
        if self.active_item.data(0, 0) == None:
            self.selected_text_widget = self.text_widgets[
                self.active_item.parent().data(0, 0)
            ]["widget"]
        else:
            self.selected_text_widget = self.text_widgets[self.active_item.data(0, 0)][
                "widget"
            ]

    def which_clicked(self):
        """item interaction detection"""
        self.active_item = self.itemFromIndex(self.currentIndex())
        if self.active_item.data(0, 0) == None:
            self.selected_text_widget = self.text_widgets[
                self.active_item.parent().data(0, 0)
            ]["widget"]
        else:
            self.selected_text_widget = self.text_widgets[self.active_item.data(0, 0)][
                "widget"
            ]

    def update_code(self, filename: str, item_string: str, place_cursor: bool) -> None:
        """updates code in text_widget.objectName(`file`);
           highlights `item_string` if exists;
           places the cursor on `item_string` if `place_cursor` True.

        Args:
            file (str): filename.extension
            item_string (str): item within `file` that changed, if any.
            place_cursor (bool): place the text cursor on `item_string` if True and `item_string` exists.
        """
        self.logger.debug("update {filename}".format(filename=filename))

        # update widgets
        if filename == "README.md":
            code_string = self.readme_md()
            self.code_preview_dict["files"]["README.md"]["file_string"] = code_string
            self.set_code_string("README.md", code_string, item_string, place_cursor)
            self.code_preview_dict["files"]["README.md"]["file_lines_list"] = []
            self.code_preview_dict["files"]["README.md"][
                "file_lines_list"
            ] = code_string.split("\n")

        elif filename == "config.h":
            code_string = self.config_h()
            self.code_preview_dict["files"]["config.h"]["file_string"] = code_string
            self.set_code_string("config.h", code_string, item_string, place_cursor)
            self.code_preview_dict["files"]["config.h"]["file_lines_list"] = []
            self.code_preview_dict["files"]["config.h"][
                "file_lines_list"
            ] = code_string.split("\n")

        elif filename == "CLI.h":
            code_string = self.cli_h()
            self.code_preview_dict["files"]["CLI.h"]["file_string"] = code_string
            self.set_code_string("CLI.h", code_string, item_string, place_cursor)
            self.code_preview_dict["files"]["CLI.h"]["file_lines_list"] = []
            self.code_preview_dict["files"]["CLI.h"][
                "file_lines_list"
            ] = code_string.split("\n")
        elif filename == "parameters.h":
            code_string = self.parameters_h()
            self.code_preview_dict["files"]["parameters.h"]["file_string"] = code_string
            self.set_code_string("parameters.h", code_string, item_string, place_cursor)
            self.code_preview_dict["files"]["parameters.h"]["file_lines_list"] = []
            self.code_preview_dict["files"]["parameters.h"][
                "file_lines_list"
            ] = code_string.split("\n")

        elif filename == "functions.h":
            code_string = self.functions_h()
            self.code_preview_dict["files"]["functions.h"]["file_string"] = code_string
            self.set_code_string("functions.h", code_string, item_string, place_cursor)
            self.code_preview_dict["files"]["functions.h"]["file_lines_list"] = []
            self.code_preview_dict["files"]["functions.h"][
                "file_lines_list"
            ] = code_string.split("\n")

    def build_tree(self) -> None:
        """builds codepreviewwidgets"""
        for key in self.code_preview_dict["files"]:
            label = QTreeWidgetItem(self.invisibleRootItem(), [key, ""])
            label.setIcon(0, self.fileicon)
            if key != "README.md":
                text_widget = CodePreviewBrowser(key, self.app)
                self.text_widgets.update(
                    {key: {"widget": text_widget, "parent": label}}
                )
            else:
                text_widget = MarkDownBrowser(key, self.app)
                self.text_widgets.update(
                    {key: {"widget": text_widget, "parent": label}}
                )

            text_widget_container = QTreeWidgetItem(label)
            text_widget_container.setFirstColumnSpanned(True)
            text_widget_container.drag_box_qrect = self.visualItemRect(
                text_widget_container
            )
            self.setItemWidget(text_widget_container, 0, text_widget)

    def set_code_string(
        self,
        filename: str,
        code_string: str,
        item_string: str,
        place_cursor: bool = False,
    ) -> None:
        """sets the code string in `filename` widget

        Args:
            filename (str): the filename
            code_string (str): the code
            item_string (str): code to highlight
            place_cursor (bool, optional): place cursor on highlighted code if True. Defaults to False.
        """
        text_widget = self.text_widgets[filename]["widget"]

        if (
            len(self.code_preview_dict["files"][filename]["file_string"].split("\n"))
            <= self.minimum_file_len[filename]
        ):
            text_widget.clear()
            return

        if filename != "README.md":
            text_widget.setPlainText(code_string)
        else:
            # text_widget.setHtml(code_string)
            text_widget.setMarkdown(code_string)

        if place_cursor == True and code_string != "":
            self.text_widgets[filename]["parent"].setExpanded(True)
            self.set_text_cursor(text_widget, item_string)

    def set_text_cursor(self, text_widget, item_string: str) -> None:
        """sets the cursor on `item_string` in `text_widget`

        Args:
            text_widget (CodePreviewBrowser or MarkdownBrowser): the widget to search
            item_string (str): the text to search for
        """
        cursor = QTextCursor(text_widget.document().find(item_string))
        cursor.movePosition(cursor.EndOfLine)
        text_widget.setTextCursor(cursor)
        cursor.movePosition(cursor.StartOfLine, QTextCursor.KeepAnchor, 1)
        text_widget.setTextCursor(cursor)
        text_widget.ensureCursorVisible()

    def get_vertical_drag_icon_geometry(self, widget_qrect: QRect) -> QRect:
        """makes the interactive box to resize code preview widgets

        Args:
            widget_qrect (QRect): size of individual widgets in the tree

        Returns:
            QRect: size and position descriptor
        """
        return QRect(
            20,
            widget_qrect.y() + widget_qrect.height() - 4,
            widget_qrect.width() - 20,
            25,
        )

    def resize_code_preview_tree_item(self, mouse_pos: QCursor) -> None:
        """resizes code preview tree items

        Args:
            mouse_pos (QCursor): position of the mouse
        """
        y_axis = self.init_height + (mouse_pos.y() - self.init_mouse_pos.y())
        self.drag_resize_qsize.setHeight(y_axis)
        self.selected_drag_to_resize_item.setSizeHint(0, self.drag_resize_qsize)
        widget_size = (
            self.selected_drag_to_resize_item.treeWidget()
            .itemWidget(self.selected_drag_to_resize_item, 0)
            .sizeHint()
        )
        widget_size.setWidth(self.qrect.width())
        if y_axis >= 192:
            widget_size.setHeight(y_axis)
            self.selected_drag_to_resize_item.treeWidget().itemWidget(
                self.selected_drag_to_resize_item, 0
            ).resize(widget_size)
        self.doItemsLayout()

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if not self._cursor:
            return super().eventFilter(watched, event)
        event_type = event.type()
        mouse_button = False
        mouse_pos = self._cursor.pos()

        if (
            event_type == event.MouseButtonPress
            or event_type == event.MouseButtonRelease
        ):
            mouse_button = QMouseEvent(event).button()
            mouse_pos = QMouseEvent(event).position().toPoint()
        if event_type == event.MouseMove:
            mouse_pos = QMouseEvent(event).position().toPoint()

        if watched == self.viewport():
            if (
                event_type == event.HoverEnter
                or event_type == event.HoverMove
                or event_type == event.HoverLeave
            ):
                viewportpos = self.viewport().mapFromGlobal(mouse_pos)
                selected_item = self.itemAt(viewportpos)

                if selected_item and selected_item.childCount() == 0:
                    self.selected_text_widget = selected_item.treeWidget().itemWidget(
                        selected_item, 0
                    )

                    drag_box_qrect = self.get_vertical_drag_icon_geometry(
                        self.visualItemRect(selected_item)
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

        if event_type == event.Wheel and self.selected_text_widget != None:
            sb = self.selected_text_widget.verticalScrollBar()
            sb.setValue(sb.value() + (-(event.angleDelta().y() / 8)))

        if event_type == event.MouseButtonPress and mouse_button == Qt.LeftButton:
            selected_item = self.itemAt(mouse_pos)
            self.qrect = self.visualItemRect(selected_item)
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
        return super().eventFilter(watched, event)


class LineNumberArea(QWidget):
    """Widget specialization to paint linenos

    Args:
        QWidget (QWidget): widget type to specialize
    """

    def __init__(self, editor) -> None:
        """the constructor

        Args:
            editor (CodePreviewBrowser or MarkdownBrowser): the text editor adopting this widget
        """
        QWidget.__init__(self, editor)
        self._code_editor = editor

    def sizeHint(self) -> QSize:
        return QSize(self._code_editor.line_number_area_width(), 0)

    def paintEvent(self, event: QPaintEvent) -> None:
        return self._code_editor.lineNumberAreaPaintEvent(event)


## every code preview text widget is this except the readme
class CodePreviewBrowser(QPlainTextEdit):
    """specializes QPlainTextEdit to view generated code

    Args:
        QPlainTextEdit (QWidget): base class
    """

    # spawns a QTextBrowser with these settings
    def __init__(self, name: str, app: QApplication):
        """Constructor method, each widget must have a unique name
           Only widgets named README.md will allow external links

        Args:
            name (str): human readable object ID (a filename)
        """
        super(CodePreviewBrowser, self).__init__()
        self.app = app
        self.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.setReadOnly(True)
        self.setObjectName(str(name))
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumHeight(25)
        self.setMinimumWidth(100)
        self.centerCursor()
        self.line_number_area = LineNumberArea(self)
        self.blockCountChanged[int].connect(self.update_line_number_area_width)
        self.updateRequest[QRect, int].connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)
        self.update_line_number_area_width(0)
        self.setTextInteractionFlags(
            Qt.TextSelectableByKeyboard | Qt.TextSelectableByMouse
        )

    def resizeEvent(self, event: QEvent) -> None:
        """Keeps the text cursor visible while resizing `this` text widget

        Args:
            event (QEvent): always a resize
        """
        super().resizeEvent(event)
        cr = self.contentsRect()
        width = self.line_number_area_width()
        rect = QRect(cr.left(), cr.top(), width, cr.height())
        self.line_number_area.setGeometry(rect)
        self.centerCursor()

    def mousePressEvent(self, e):
        """changes cursor over external link

        Args:
            e (QEvent): Event
        """
        self.anchor = self.anchorAt(e.pos())
        if self.anchor:
            self.app.setOverrideCursor(Qt.PointingHandCursor)

    def mouseReleaseEvent(self, e) -> None:
        """changes cursor back to arrow after releasing mouse button

        Args:
            e (QEvent): Event
        """
        if self.anchor:
            QDesktopServices.openUrl(QUrl(self.anchor))
            self.app.setOverrideCursor(Qt.ArrowCursor)
            self.anchor = None

    def line_number_area_width(self) -> int:
        digits = 1
        max_num = max(1, self.blockCount())
        while max_num >= 10:
            max_num *= 0.1
            digits += 1

        space = 3 + self.fontMetrics().horizontalAdvance("9") * digits
        return space

    def lineNumberAreaPaintEvent(self, event: QPaintEvent):
        """paints the line number rectangle and the line numbers

        Args:
            event (QPaintEvent): Time to draw now!
        """
        with QPainter(self.line_number_area) as painter:
            painter.fillRect(event.rect(), Qt.lightGray)
            block = self.firstVisibleBlock()
            block_number = block.blockNumber()
            _contentOffset = self.contentOffset()
            top = self.blockBoundingGeometry(block).translated(_contentOffset).top()
            bottom = top + self.blockBoundingRect(block).height()

            while block.isValid() and top <= event.rect().bottom():
                if block.isVisible() and bottom >= event.rect().top():
                    number = str(block_number + 1)
                    painter.setPen(Qt.black)
                    width = self.line_number_area_width()
                    height = self.fontMetrics().height()
                    painter.drawText(0, top, width, height, Qt.AlignLeft, number)

                block = block.next()
                top = bottom
                bottom = top + self.blockBoundingRect(block).height()
                block_number += 1

    @Slot(int)
    def update_line_number_area_width(self, newBlockCount):
        """resize lineno width

        Args:
            newBlockCount (int): The new number of text blocks.
        """
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    @Slot(QRect, int)
    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            width = self.line_number_area.width()
            self.line_number_area.update(0, rect.y(), width, rect.height())

        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    @Slot()
    def highlight_current_line(self):
        extra_selections = []

        selection = QTextEdit.ExtraSelection()

        line_color = QColor(Qt.blue).lighter(160)
        selection.format.setBackground(line_color)

        selection.format.setProperty(QTextFormat.FullWidthSelection, True)

        selection.cursor = self.textCursor()
        selection.cursor.clearSelection()

        extra_selections.append(selection)

        self.setExtraSelections(extra_selections)


## the only code preview text widget that uses this class is readme.md
class MarkDownBrowser(QTextEdit):
    """specializes QTextEdit to view .md

    Args:
        QTextEdit (QWidget): base class specialization
    """

    # spawns a QTextBrowser with these settings
    def __init__(self, name: str, app: QApplication):
        """Constructor method, each widget must have a unique name
           Only widgets named README.md will allow external links

        Args:
            name (str): human readable object ID (a filename)
        """
        super(MarkDownBrowser, self).__init__()
        self.app = app
        self.setLineWrapMode(QTextEdit.NoWrap)
        self.setReadOnly(True)
        self.setObjectName(str(name))
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumHeight(25)
        self.setMinimumWidth(100)
        self.ensureCursorVisible()
        # let the user navigate to the hyperlinks provided in the readme
        self.setTextInteractionFlags(
            Qt.TextSelectableByKeyboard
            | Qt.TextSelectableByMouse
            | Qt.LinksAccessibleByKeyboard
            | Qt.LinksAccessibleByMouse
        )

    def resizeEvent(self, event: QEvent) -> None:
        """Keeps the text cursor visible while resizing `this` text widget

        Args:
            event (QEvent): always a resize
        """
        self.ensureCursorVisible()

    def mouseMoveEvent(self, e):
        """changes cursor over external link

        Args:
            e (QEvent): Event
        """
        self.anchor = self.anchorAt(e.pos())
        if self.anchor:
            self.app.setOverrideCursor(Qt.PointingHandCursor)

    def mousePressEvent(self, e):
        """changes cursor over external link

        Args:
            e (QEvent): Event
        """
        self.anchor = self.anchorAt(e.pos())
        if self.anchor:
            self.app.setOverrideCursor(Qt.PointingHandCursor)

    def mouseReleaseEvent(self, e) -> None:
        """changes cursor back to arrow after releasing mouse button

        Args:
            e (QEvent): Event
        """
        if self.anchor:
            QDesktopServices.openUrl(QUrl(self.anchor))
            self.app.setOverrideCursor(Qt.ArrowCursor)
            self.anchor = None


class CommandParametersPTableWidget(QTableWidget, object):
    def __init_subclass__(cls) -> None:
        return super(CommandParametersPTableWidget, cls).__init_subclass__()

    def mouseDoubleClickEvent(cls, event) -> None:
        if cls.tree.active_item:
            cls.tree.clicked_edit_tab_two()
        return super().mouseDoubleClickEvent(event)

    def build_table(cls, command_parameters, tree):
        cls.tree = tree
        cls.prm = copy.deepcopy(command_parameters)
        cls.prm.pop("commandArguments")
        rows = int((len(cls.prm) * 2) / 6)
        cls.setColumnCount(6)
        cls.setRowCount(rows)
        cls.setHorizontalHeaderLabels(
            [
                "Setting",
                "Value",
                "Setting",
                "Value",
                "Setting",
                "Value",
            ]
        )
        cls.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        cls.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        r = 0
        c = 0
        for key in cls.prm:
            setting_item = QTableWidgetItem()
            setting_item.setData(0, key)
            setting_item.setToolTip(displayModels.command_table_tooltip_dict[key])
            setting_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            setting_item.setFlags(setting_item.flags() & ~Qt.ItemIsEditable)
            cls.setItem(r, c, setting_item)
            c += 1
            value_item = QTableWidgetItem()
            value_item.setData(0, cls.prm[key])
            value_item.setToolTip(displayModels.command_table_tooltip_dict[key])
            value_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            value_item.setFlags(value_item.flags() & ~Qt.ItemIsEditable)
            cls.setItem(r, c, value_item)
            c += 1
            if c > cls.columnCount():
                r += 1
                c = 0


class CommandParametersArgumentsTableWidget(QTableWidget, object):
    def __init_subclass__(cls) -> None:
        return super(CommandParametersArgumentsTableWidget, cls).__init_subclass__()

    def build_table(cls, command_parameters, tree):
        cls.tree = tree
        cls.args_list = cls.parse_commandarguments_string(
            command_parameters["commandArguments"]
        )
        table = cls
        table.clear()
        table.setColumnCount(1)
        table.setHorizontalHeaderLabels(["type"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setRowCount(len(cls.args_list))
        table.setMinimumWidth(150)
        table.setMaximumWidth(175)
        for r in range(len(cls.args_list)):
            type_item = QTableWidgetItem()
            type_item.setData(0, cls.args_list[r])
            type_item.setToolTip(
                displayModels.argument_table_tooltip_dict[cls.args_list[r]]
            )
            type_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            table.setItem(r, 0, type_item)

    def parse_commandarguments_string(cls, args: str) -> list:
        args_list = copy.deepcopy(args)
        args_list = args_list.replace("UITYPE::", "")
        args_list = args_list.replace("{", "")
        args_list = args_list.replace("}", "")
        args_list = args_list.replace(" ", "")
        args_list = args_list.replace("\n", "")
        args_list = args_list.split(",")
        return args_list

    def mouseDoubleClickEvent(cls, event) -> None:
        if cls.tree.active_item:
            cls.tree.clicked_edit_tab_two()
        return super().mouseDoubleClickEvent(event)


class CommandParametersTableWidget(QWidget):
    """Command parameters table container

    Args:
        QWidget (object): Base class that is specialized
    """

    def __init__(self, command_parameters, tree_item, tree) -> None:
        """constructor method

        Args:
            command_parameters (dict): command parameters dictionary
            tree_item (QTreeWidgetItem): parent container
            logger (logger): method logger
            cursor (QCursor): mouse cursor
        """
        super(CommandParametersTableWidget, self).__init__()
        self.parameters = command_parameters
        self.tree = tree
        self.tree_item = tree_item
        self.widget_layout = QHBoxLayout(self)
        self.splitter = QSplitter(self)

        self.parameters_view = CommandParametersPTableWidget()
        self.parameters_view.build_table(self.parameters, self.tree)

        self.arguments_view = CommandParametersArgumentsTableWidget()
        self.arguments_view.build_table(self.parameters, self.tree)

        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        self.splitter.addWidget(self.parameters_view)
        self.splitter.addWidget(self.arguments_view)
        self.widget_layout.addWidget(self.splitter)
        self.splitter.setSizes(
            [
                self.parameters_view.sizeHint().width(),
                self.arguments_view.sizeHint().width(),
            ]
        )
        self.setLayout(self.widget_layout)


class CommandTreeWidget(QTreeWidget, QTreeWidgetItem):
    def __init__(self, parent, cliopt, logger) -> None:
        super(CommandTreeWidget, self).__init__()
        self.setParent(parent.ui.command_tree_container)
        self.active_builtins = []
        self._settings_tree = None
        self._parent = parent
        self.ih_builtins = self._parent.ih_builtins
        self.cliopt = cliopt
        self.active_item = self.invisibleRootItem()
        self._cursor = self._parent.qcursor
        self.create_qdialog = self._parent.create_qdialog
        self.clicked_edit_tab_two = self._parent.clicked_edit_tab_two
        self.logger = logger
        self.command_index = cliopt["commands"]["index"]
        self.loading_index = 0
        self.setColumnCount(2)
        self.setColumnHidden(1, 1)
        self.setHeaderLabel("Command Tree")
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_customContextMenuRequested)
        self.build_tree()
        self.clicked.connect(self.which_clicked)
        self.pressed.connect(self.which_pressed)
        self.itemChanged.connect(self.item_changed)
        self.currentItemChanged.connect(self.item_changed)
        self.itemSelectionChanged.connect(self._parent.command_tree_button_toggles)
        self.itemClicked.connect(self._parent.command_tree_button_toggles)
        self.itemCollapsed.connect(self._parent.command_tree_button_toggles)
        self.itemExpanded.connect(self._parent.command_tree_button_toggles)

    def on_customContextMenuRequested(self, pos):
        self._pos = pos
        menu = QMenu(self)
        item_title = self.get_parent_item(self.itemAt(pos)).data(0, 0)
        collapseAction = QAction(f"collapse {item_title}", self)
        collapseAction.triggered.connect(self.collapseAt)
        deleteAction = QAction(f"delete {item_title}")
        deleteAction.setShortcut(Qt.Key_Delete)
        deleteAction.triggered.connect(self.deleteAt)
        editAction = QAction(f"edit {item_title}")
        editAction.setShortcuts(QKeySequence(Qt.Key_Return, Qt.Key_Enter))
        editAction.triggered.connect(self.editAt)
        menu.addAction(collapseAction)
        menu.addAction(editAction)
        menu.addAction(deleteAction)
        menu.exec(self.mapToGlobal(pos))
        return super().customContextMenuRequested

    def collapseAt(self):
        index = self.indexFromItem(self.get_parent_item(self.itemAt(self._pos)))
        self.collapse(index)

    def deleteAt(self):
        item = self.itemAt(self._pos)
        item_title = self.get_parent_item(item).data(0, 0)
        self.active_item = item
        b = QDialogButtonBox.StandardButton
        buttons = [b.Ok, b.Close]
        button_text = ["Yes", "No"]
        result = self.create_qdialog(
            f"remove {item_title} from tree?",
            Qt.AlignCenter,
            Qt.NoTextInteraction,
            "Deleting command",
            buttons,
            button_text,
            QStyle.StandardPixmap.SP_MessageBoxCritical,
            self._parent.qscreen,
        )
        if result == QDialog.Accepted:
            self.remove_command_from_tree()

    def editAt(self):
        item = self.itemAt(self._pos)
        item_title = self.get_parent_item(item).data(0, 0)
        self.active_item = item
        self._parent.clicked_edit_tab_two()

    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key_Escape:
            self.selectionModel().clearSelection()
        if event.key() == Qt.Key_Delete:
            if self.active_item:
                item_title = self.get_parent_item(self.active_item).data(0, 0)
                b = QDialogButtonBox.StandardButton
                buttons = [b.Ok, b.Close]
                button_text = ["Yes", "No"]
                result = self.create_qdialog(
                    f"remove {item_title} from tree?",
                    Qt.AlignCenter,
                    Qt.NoTextInteraction,
                    "Deleting command",
                    buttons,
                    button_text,
                    QStyle.StandardPixmap.SP_MessageBoxCritical,
                    self._parent.qscreen,
                )
                if result == QDialog.Accepted:
                    self.remove_command_from_tree()
        if event.key() in (Qt.Key_Enter, Qt.Key_Return):
            if self.active_item:
                self._parent.clicked_edit_tab_two()
        return super().keyPressEvent(event)

    def mouseDoubleClickEvent(self, event) -> None:
        if self.active_item:
            self.clicked_edit_tab_two()
        return super().mouseDoubleClickEvent(event)

    def make_builtin_parameters(self, builtin: str = None) -> dict:
        if builtin == "listCommands":
            list_commands = OrderedDict()
            list_commands = dict(
                zip(
                    dataModels.command_parameters_dict_keys_list,
                    dataModels.LCcmdParam,
                )
            )
            return list_commands
        if builtin == "listSettings":
            list_settings = OrderedDict()
            list_settings = dict(
                zip(
                    dataModels.command_parameters_dict_keys_list,
                    dataModels.LScmdParam,
                )
            )
            return list_settings
        return {}

    def saveState(self):
        items = self.findItems("*", Qt.MatchWrap | Qt.MatchWildcard | Qt.MatchRecursive)
        current_selected = ""
        expanded_state = []
        state = {"selected item": current_selected, "expanded": expanded_state}
        state_index = 0
        for item in items:
            if item.isSelected():
                state["selected item"] = state_index
            if item.isExpanded():
                state["expanded"].append(True)
            else:
                state["expanded"].append(False)
            state_index += 1
        b = json.dumps(state, indent=2).encode("utf-8")
        return QByteArray(b)

    def restoreState(self, b: QByteArray):
        items = self.findItems("*", Qt.MatchWrap | Qt.MatchWildcard | Qt.MatchRecursive)
        state = json.loads(b.data())
        state_index = 0
        for item in items:
            if state_index == state["selected item"]:
                self.setCurrentItem(item)
                self.active_item = item
            if state_index < len(state["expanded"]):
                if state["expanded"][state_index] == True:
                    item.setExpanded(True)
                else:
                    item.setExpanded(False)
            else:
                break
            state_index += 1

    def get_settings_tree(self):
        self._settings_tree = self._parent.settings_tree

    def build_tree(self):
        self.logger.info("Building command tree.")

        def populate_children(parent, index):
            if bool(self.command_index[index]["child index key list"]):
                for child_index in self.command_index[index]["child index key list"]:
                    child_command = self.add_command_to_tree(parent)
                    if bool(self.command_index[child_index]["child index key list"]):
                        populate_children(child_command, child_index)

        for root_command_index in self.command_index:
            # only populates root commands with their children, because
            # self.command_index is flat, not a matrix
            if int(self.command_index[root_command_index]["root index key"]) == int(
                self.command_index[root_command_index]["parameters key"]
            ):
                root_command = self.add_command_to_tree(self.invisibleRootItem())
                populate_children(root_command, root_command_index)

    def update_command(self, item: QTreeWidgetItem):
        command_container = self.get_child_item(item)
        command_parameters = self.cliopt["commands"]["parameters"][
            self.command_index[command_container.data(1, 0)]["parameters key"]
        ]
        command_table = CommandParametersTableWidget(
            command_parameters, command_container, self
        )
        self.removeItemWidget(command_container, 0)
        self.setItemWidget(command_container, 0, command_table)
        self._parent.prompt_to_save = True
        self._parent.windowtitle_set = False
        self._parent.set_main_window_title()

    def add_command_to_tree(
        self, parent_item: QTreeWidgetItem, builtin: str = None
    ) -> QTreeWidgetItem:
        item = self.build_command(parent_item, builtin)
        self.active_item = item

        if self._parent.loading == False and self._parent.prompt_to_save == False:
            item.setExpanded(True)
            self.setCurrentItem(item)
            self._parent.prompt_to_save = True
            self._parent.windowtitle_set = False
            self._parent.set_main_window_title()
        return item

    def build_command(self, parent_item, builtin: str = None):
        if builtin != None:
            if builtin in self.active_builtins:
                return None

        if self._parent.loading:
            if len(self.command_index) - 1 >= int(self.loading_index):
                command_index = str(
                    list(self.command_index.keys())[int(self.loading_index)]
                )
            else:
                self.make_command_index(parent_item)
                command_index = str(
                    list(self.command_index.keys())[int(self.loading_index)]
                )
            self.cliopt["commands"]["primary id key"] = command_index
            primary_id_key = command_index
            if int(self.loading_index) < len(list(self.command_index.keys())):
                self.loading_index = str(int(self.loading_index) + 1)
        else:
            command_index = str(self.cliopt["commands"]["primary id key"])
            primary_id_key = command_index
            if primary_id_key not in self.cliopt["commands"]["index"]:
                self.make_command_index(parent_item)

        if builtin != None:
            self.active_builtins.append(builtin)
            self.cliopt["commands"]["parameters"].update(
                {
                    self.cliopt["commands"][
                        "primary id key"
                    ]: self.make_builtin_parameters(builtin)
                }
            )

        if parent_item == None:
            parent_item = self.active_item
            if parent_item == None:
                parent_item = self.invisibleRootItem()

        command_parameters = self.cliopt["commands"]["parameters"][
            self.command_index[command_index]["parameters key"]
        ]
        command_string = command_parameters["commandString"]

        command_label = QTreeWidgetItem(parent_item, [command_string, ""])
        command_label.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        command_label.setData(1, 0, str(primary_id_key))
        command_container = QTreeWidgetItem(command_label, "")
        command_container.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        command_container.setData(1, 0, str(primary_id_key))
        command_label.addChild(command_container)

        command_table = CommandParametersTableWidget(
            command_parameters, command_container, self
        )

        self.setItemWidget(command_container, 0, command_table)

        if parent_item == self.invisibleRootItem():
            self.addTopLevelItem(command_label)
            command_label.setExpanded(True)
            parent_string = "Root"
        else:
            item = self.active_item
            item.addChild(command_label)
            command_label.setExpanded(True)
            parent_string = parent_item.data(0, 0)

        self.cliopt["commands"]["primary id key"] = str(int(int(primary_id_key) + 1))

        if not self._parent.loading:
            number_of_commands = self.cliopt["commands"]["number of commands"]
            self.cliopt["commands"]["number of commands"] = str(
                int(int(number_of_commands) + 1)
            )

        self.logger.info(f"added {command_string} to CommandTreeWidget {parent_string}")

        self._parent.update_code("README.md", command_string, True)
        self._parent.update_code("CLI.h", command_string, True)
        self._parent.update_code("functions.h", command_string, True)
        self._parent.update_code("parameters.h", command_string, True)
        return command_label

    def item_changed(self, item, column):
        self.active_item = item

    def make_command_index(self, parent_item):
        primary_id_key = self.cliopt["commands"]["primary id key"]
        self.cliopt["commands"]["index"].update(
            {primary_id_key: copy.deepcopy(dataModels.parameters_index_struct)}
        )

        if parent_item == self.invisibleRootItem() or parent_item == None:
            self.cliopt["commands"]["index"][primary_id_key]["parameters key"] = str(
                primary_id_key
            )
            self.cliopt["commands"]["index"][primary_id_key]["root index key"] = str(
                primary_id_key
            )
            self.cliopt["commands"]["index"][primary_id_key]["parent index key"] = str(
                primary_id_key
            )
        else:
            parent_index = self.get_command_index(parent_item)
            self.cliopt["commands"]["index"][primary_id_key]["parameters key"] = str(
                primary_id_key
            )
            self.cliopt["commands"]["index"][primary_id_key]["root index key"] = str(
                parent_index["root index key"]
            )
            self.cliopt["commands"]["index"][primary_id_key]["parent index key"] = str(
                parent_item.data(1, 0)
            )
            parent_index["child index key list"].append(primary_id_key)

    def remove_command_from_tree(self, search_string=None):
        if (
            search_string in self.ih_builtins
            and search_string not in self.active_builtins
        ):
            self.logger.info(f"{search_string} not in command tree")
            return -1

        if search_string != None:
            item_list = self.findItems(search_string, Qt.MatchExactly, 0)
            if bool(item_list):
                item = item_list[0]
            else:
                self.logger.info(
                    f"couldnt find {search_string} to remove it from the tree"
                )
                return -1
        else:
            item = self.get_parent_item(self.active_item)

        number_of_commands = int(self.cliopt["commands"]["number of commands"])

        if item == self.invisibleRootItem():
            self.logger.warning(f"cannot delete self.invisibleRootItem()!")
            return -1

        def remove_children(item: QTreeWidgetItem, number_of_commands):
            if item.childCount() > 0:
                child_list = []
                list_len = item.childCount()
                for i in range(list_len):
                    child_list.append(item.child(i))
                for i in reversed(range(list_len)):
                    if item.child(i).childCount() > 0:
                        remove_children(item.child(i), number_of_commands)
                    number_of_commands = clean_up(child_list[i], number_of_commands)
            else:
                number_of_commands = clean_up(item, number_of_commands)
            return number_of_commands

        def clean_up(item: QTreeWidgetItem, number_of_commands):
            command_index = self.get_command_index(item)
            if command_index == -1:
                return number_of_commands
            if (
                command_index["parameters key"]
                in self.command_index[command_index["parent index key"]][
                    "child index key list"
                ]
            ):
                self.command_index[command_index["parent index key"]][
                    "child index key list"
                ].remove(command_index["parameters key"])
            command_string = self.cliopt["commands"]["parameters"][
                command_index["parameters key"]
            ]["commandString"]
            self.logger.info(f"removing {command_string} from command tree")
            if item != self.invisibleRootItem():
                del item
            if command_index["parameters key"] in self.cliopt["commands"]["parameters"]:
                del self.cliopt["commands"]["parameters"][
                    command_index["parameters key"]
                ]
            if command_index["parameters key"] in self.cliopt["commands"]["index"]:
                del self.cliopt["commands"]["index"][command_index["parameters key"]]
            number_of_commands -= 1
            return number_of_commands

        if item.parent() == self.invisibleRootItem():
            index = self.indexFromItem(item)
            item = self.takeTopLevelItem(index)
            number_of_commands = remove_children(item, number_of_commands)
        else:
            parent = item.parent()
            if parent == None:
                parent = self.invisibleRootItem()
            number_of_commands = remove_children(item, number_of_commands)
            parent.removeChild(item)
        if self._parent.loading == False and self._parent.prompt_to_save == False:
            self._parent.prompt_to_save = True
            self._parent.windowtitle_set = False

        # switch off builtin
        if item.data(0, 0) in self.active_builtins:
            self.active_builtins.remove(item.data(0, 0))
            item_list = self._settings_tree.findItems(
                str(item.data(0, 0)), Qt.MatchRecursive | Qt.MatchExactly, 1
            )
            cmb_item = item_list[0]
            self._settings_tree.setCurrentItem(cmb_item)
            cmb = self._settings_tree.itemWidget(cmb_item, 3)
            self._settings_tree.setCurrentItem(item)
            cmb.setCurrentIndex(cmb.findText("Disabled"))
            self.cliopt["builtin methods"]["var"][item.data(0, 0)] = False

        self._parent.update_code("README.md", item.data(0, 0), True)
        self._parent.update_code("CLI.h", item.data(0, 0), True)
        self._parent.update_code("functions.h", item.data(0, 0), True)
        self._parent.update_code("parameters.h", item.data(0, 0), True)
        self.cliopt["commands"]["number of commands"] = str(int(number_of_commands) - 1)
        self._parent.prompt_to_save = True
        self._parent.windowtitle_set = False
        self._parent.set_main_window_title()

    def get_parent_item(self, item: QTreeWidgetItem):
        if item:
            if item.data(0, 0) != None and item.data(1, 0) != None:
                return item
            else:
                return item.parent()

    def get_child_item(self, item: QTreeWidgetItem):
        if item:
            if item.data(0, 0) == None and item.data(1, 0) != None:
                return item
            elif (
                item.data(1, 0) != None
                and item.data(1, 0) != None
                and item.childCount() > 0
            ):
                return item.child(0)

    def get_command_index(self, item):
        item_data = str(item.data(1, 0))
        if len(item_data) < 1:
            return -1
        elif item_data not in self.cliopt["commands"]["index"]:
            return -1
        else:
            return self.cliopt["commands"]["index"][item_data]

    def which_pressed(self):
        self.active_item = self.itemFromIndex(self.currentIndex())

    def which_clicked(self):
        self.active_item = self.itemFromIndex(self.currentIndex())


# TODO update underlying data
class DelimiterTableWidget(QTableWidget):
    def __init_subclass__(cls) -> None:
        return super(DelimiterTableWidget, cls).__init_subclass__()

    def build_table(cls, container, cliopt):
        cls.ddtt = displayModels._settings_tree_display["process parameters"][
            "data delimiter sequences"
        ]["tooltip"]
        cls.sstt = displayModels._settings_tree_display["process parameters"][
            "start stop data delimiter sequences"
        ]["tooltip"]
        cls._cursor = QCursor()
        cls.dict_pos = container.data(4, 0).split(",")
        cls.setObjectName(str(container.data(4, 0)))
        cls.cliopt = cliopt
        cls.delimiters = cls.cliopt[cls.dict_pos[0]]["var"][cls.dict_pos[2]]
        cls.tt = True
        if cls.dict_pos[2] == "start stop data delimiter sequences":
            cls.tt = False
        cls.setColumnCount(2)
        cls.setRowCount(len(cls.delimiters))
        cls.setMaximumWidth(300)
        cls.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        cls.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        cls.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        cls.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        r = 0
        for key in cls.delimiters:
            delimiter_item = QTableWidgetItem()
            delimiter_item.setData(0, cls.delimiters[key])
            if cls.tt:
                delimiter_item.setToolTip(cls.ddtt)
            else:
                delimiter_item.setToolTip(cls.sstt)
            cls.setItem(r, 0, delimiter_item)
            control_item = QTableWidgetItem()
            cls.setItem(r, 1, control_item)
            cls.setCellWidget(r, 1, TableButtonBox(cls))
            r += 1


class SettingsTreeWidget(Logger, QTreeWidget):
    def __init__(self, parent, cliopt, session, logger) -> None:
        super(SettingsTreeWidget, self).__init__()
        self.command_tree = parent.command_tree
        self.update_code = parent.update_code
        self.loading = parent.loading
        self.setParent(parent.ui.settings_tree_container)
        self.items = []
        self.tables = []
        self.default_settings_tree_values = parent.default_settings_tree_values
        self._parent = parent
        self.cliopt = cliopt
        self.session = session
        self.item_clicked = None
        self._cursor = parent.qcursor
        SettingsTreeWidget.logger = self.get_child_logger(__name__)
        self._tree = parent._tree
        self.setHeaderLabel("Settings Tree")
        self.setColumnCount(5)
        self.setColumnHidden(4, True)
        self.setHeaderLabels(("Section", "Macro Name", "Type", "Value"))
        self.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        for i in range(self.columnCount() - 1):
            self.header().setSectionResizeMode(i, QHeaderView.ResizeToContents)
            self.header().setSectionResizeMode(i, QHeaderView.Stretch)
        self.setMinimumWidth(400)
        # self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setSelectionMode(QAbstractItemView.NoSelection)
        self.setFocusPolicy(Qt.NoFocus)
        # use the text in _tree for self.ui.settings_tree field labels, build the tree
        for parent in self._tree:
            index_of_child = 0
            dict_key = parent

            is_config = True if dict_key == "config" else False
            # add parents to self.ui.settings_treeS

            if is_config:
                # make these parents children of root using the keys from 'cfg_dict'
                cfg_path = session["opt"]["inputhandler_config_file_path"]
                setting_container = QTreeWidgetItem(
                    self.invisibleRootItem(), [str("Input config: " + cfg_path), ""]
                )
                setting_container.setIcon(0, self._parent.ui.fileDialogContentsViewIcon)
                setting_container.setToolTip(0, "Input config: " + cfg_path)
                setting_label.setFlags(setting_label.flags() | Qt.ItemIsSelectable)

                for subsection in self._tree["config"]:
                    # index_of_child = 0
                    setting_label = QTreeWidgetItem(
                        setting_container, [subsection, "", "", ""]
                    )
                    # make the treewidgetitem editable
                    setting_label.setFlags(setting_label.flags() | Qt.ItemIsSelectable)
                    # make the treewidgetitem span columns

                    for item in self._tree["config"][subsection]:
                        # dict_pos = subsection + "," + str(index_of_child) + "," + item
                        var_initial_val = self.cliopt["config"]["var"][subsection][
                            item
                        ]["value"]
                        has_combobox = False
                        tooltip = self._tree[dict_key][subsection][item]["tooltip"]
                        combobox_tooltip = self._tree[dict_key][subsection][item][
                            "tooltip"
                        ]
                        if (
                            self._tree[dict_key][subsection][item]["type"]
                            == "Enable/Disable"
                        ):
                            has_combobox = True
                            tooltip = ""
                        index_of_child = self.set_up_child(
                            subsection,
                            setting_label,
                            index_of_child,
                            item,
                            self._tree[dict_key][subsection][item]["type"],
                            tooltip,
                            var_initial_val,
                            has_combobox,
                            combobox_tooltip,
                        )
            elif not is_config:
                setting_container = QTreeWidgetItem(
                    self.invisibleRootItem(), [dict_key, ""]
                )
                setting_container.setIcon(0, self._parent.ui.commandLinkIcon)

                for child in self._tree[parent]:
                    dict_pos = dict_key + "," + str(index_of_child) + "," + child

                    var_initial_val = self.cliopt[dict_key]["var"][child]
                    if (
                        child == "data delimiter sequences"
                        or child == "start stop data delimiter sequences"
                    ):
                        setting_label = QTreeWidgetItem(
                            setting_container, [child, "", "", ""]
                        )
                        setting_label.setData(4, 0, dict_pos)
                        setting_label.setFlags(
                            setting_label.flags() | Qt.ItemIsSelectable
                        )
                        index_of_child = self.build_tree_table_widget(
                            setting_label, index_of_child, dict_pos
                        )
                    else:
                        has_combobox = False
                        tooltip = self._tree[dict_key][child]["tooltip"]
                        combobox_tooltip = self._tree[dict_key][child]["tooltip"]
                        if self._tree[dict_key][child]["type"] == "Enable/Disable":
                            has_combobox = True
                            tooltip = ""
                        index_of_child = self.set_up_child(
                            dict_key,
                            setting_container,
                            index_of_child,
                            child,
                            self._tree[dict_key][child]["type"],
                            tooltip,
                            var_initial_val,
                            has_combobox,
                            combobox_tooltip,
                        )

                    self.default_settings_tree_values.update(
                        {str(child).strip(): var_initial_val}
                    )

        self.setEditTriggers(self.NoEditTriggers)
        # update cliopt with new value when editing is complete
        self.itemChanged.connect(self.settings_tree_edit_complete)
        # check if user clicked on the column we want them to edit
        self.itemDoubleClicked.connect(self.check_if_settings_tree_col_editable)
        # check if user hit enter on an item
        self.itemActivated.connect(self.settings_tree_item_activated)
        # self._parent.settings_tree_button_toggles()
        # self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.itemSelectionChanged.connect(self._parent.settings_tree_button_toggles)
        self.itemClicked.connect(self._parent.settings_tree_button_toggles)
        self.itemCollapsed.connect(self._parent.settings_tree_button_toggles)
        self.itemExpanded.connect(self._parent.settings_tree_button_toggles)
        self.itemExpanded.connect(self.item_expanded)

    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key_Escape:
            self.selectionModel().clearSelection()
        return super().keyPressEvent(event)

    def item_expanded(self, item: QTreeWidgetItem):
        self.active_item = item

    def saveState(self):
        items = self.findItems("*", Qt.MatchWrap | Qt.MatchWildcard | Qt.MatchRecursive)
        current_selected = ""
        expanded_state = []
        state = {"selected item": current_selected, "expanded": expanded_state}
        state_index = 0
        for item in items:
            if item.isSelected():
                state["selected item"] = state_index
            if item.isExpanded():
                state["expanded"].append(True)
            else:
                state["expanded"].append(False)
            state_index += 1
        b = json.dumps(state, indent=2).encode("utf-8")
        return QByteArray(b)

    def restoreState(self, b: QByteArray):
        items = self.findItems("*", Qt.MatchWrap | Qt.MatchWildcard | Qt.MatchRecursive)
        state = json.loads(b.data())
        state_index = 0
        for item in items:
            if state_index == state["selected item"]:
                self.setCurrentItem(item)
                self.active_item = item

            if state["expanded"][state_index] == True:
                item.setExpanded(True)
            else:
                item.setExpanded(False)
            state_index += 1

    def update_delimiters(self, row, column, table):
        dict_pos = table.dict_pos.split(",")
        self.cliopt[dict_pos[0]]["var"][dict_pos[2]] = {}
        for row in range(table.rowCount()):
            self.cliopt[dict_pos[0]]["var"][dict_pos[2]].update(
                {str(row): str(table.item(row, 0).data(0))}
            )
        self.prompt_to_save = True

    ## builds a table onto a tree widget item
    def build_tree_table_widget(self, label: QTreeWidgetItem, index_of_child, dict_pos):
        container = QTreeWidgetItem(label)
        container.setFirstColumnSpanned(True)
        container.setData(4, 0, dict_pos)
        # table = DelimitersTableView(self, logger, cursor, container, self.cliopt)
        table = DelimiterTableWidget(self)
        table.build_table(container, self.cliopt)
        table.dict_pos = dict_pos
        table.cellChanged.connect(lambda r, c, t=table: self.update_delimiters(r, c, t))
        self.setItemWidget(container, 0, table)
        self.tables.append(table)
        index_of_child += 1
        return index_of_child

    ## helper method to add children to container items
    def set_up_child(
        self,
        dict_key,
        parent,
        index_of_child,
        var_name,
        var_type,
        var_tooltip,
        var_initial_val,
        combobox=False,
        combobox_item_tooltips=[],
    ):
        column_label_list = ["", var_name, var_type, str(repr(var_initial_val))]
        child_container = QTreeWidgetItem(parent, column_label_list)
        _twi = child_container
        dict_pos = dict_key + "," + str(index_of_child) + "," + var_name
        _twi.setData(4, 0, dict_pos)
        _twi.setFlags(_twi.flags() | Qt.ItemIsEditable)
        if var_tooltip != "" and var_tooltip != None:
            for col in range(self.columnCount()):
                _twi.setToolTip(col, var_tooltip)
        if combobox == True:
            for col in range(self.columnCount()):
                _twi.setToolTip(col, combobox_item_tooltips[0])
            _cmb = QComboBox()
            _cmb.addItem("Disabled", False)
            _cmb.addItem("Enabled", True)

            if (
                combobox_item_tooltips
                and combobox_item_tooltips[0] != None
                and combobox_item_tooltips[0] != ""
            ):
                _cmb.setItemData(0, combobox_item_tooltips[0], Qt.ToolTipRole)
            if (
                combobox_item_tooltips
                and combobox_item_tooltips[1] != None
                and combobox_item_tooltips[1] != ""
            ):
                _cmb.setItemData(1, combobox_item_tooltips[1], Qt.ToolTipRole)
            _cmb.setObjectName(dict_pos)
            if var_initial_val == False:
                _cmb.setCurrentIndex(_cmb.findText("Disabled"))
            elif var_initial_val == True:
                _cmb.setCurrentIndex(_cmb.findText("Enabled"))
            _cmb.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLengthWithIcon)
            # either or, dont trigger twice
            # _cmb.currentIndexChanged.connect(self.settings_tree_combo_box_index_changed)
            _cmb.currentTextChanged.connect(
                lambda text, combobox=_cmb, item=_twi: self.settings_tree_combo_box_index_changed(
                    text, combobox, item
                )
            )
            self.setItemWidget(
                _twi,
                3,
                _cmb,
            )
        index_of_child += 1
        return index_of_child

    ## updates the type field to reflect the value
    def update_settings_tree_type_field_text(self, item):
        object_string = str(item.data(4, 0))
        object_list = object_string.strip("\n").split(",")
        sub_dict = self.cliopt["config"]["var"][object_list[0]][object_list[2]]
        number_field = sub_dict["value"]

        if str(number_field) == "True" or str(number_field) == "False":
            return

        if number_field <= 255:
            type_field = "uint8_t"
            item.setToolTip(2, "")
        elif number_field > 255 and number_field <= 65535:
            type_field = "uint16_t*"
            item.setToolTip(2, "The compiler will warn you about this type change")
        elif number_field > 65535:
            type_field = "uint32_t*"
            item.setToolTip(2, "The compiler will warn you about this type change")
        item.setText(2, type_field)

    ## called on combobox change
    def settings_tree_combo_box_index_changed(self, text, combobox, item):
        self.prompt_to_save = True
        self.windowtitle_set = False
        _twi = item
        self.setCurrentItem(_twi)
        object_string = str(_twi.data(4, 0))
        object_list = object_string.strip("\n").split(",")
        object_list[1] = int(object_list[1])

        if object_list[0] in displayModels._settings_tree_display["config"]:
            _tt = displayModels._settings_tree_display["config"][object_list[0]][
                object_list[2]
            ]["tooltip"]
        else:
            _tt = displayModels._settings_tree_display[object_list[0]][object_list[2]][
                "tooltip"
            ]

        if object_list[0] == "builtin methods":
            if combobox.currentText() == "Enabled":
                if object_list[0] in self.cliopt:
                    self.cliopt[object_list[0]]["var"][object_list[2]] = "True"
                else:
                    self.cliopt["config"]["var"][object_list[0]][object_list[2]][
                        "value"
                    ] = "True"
                SettingsTreeWidget.logger.info(
                    object_list[0] + " " + object_list[2] + " enabled"
                )
                for col in range(self.columnCount()):
                    _twi.setToolTip(col, _tt[1])
            else:
                if object_list[0] in self.cliopt:
                    self.cliopt[object_list[0]]["var"][object_list[2]] = "False"
                else:
                    self.cliopt["config"]["var"][object_list[0]][object_list[2]][
                        "value"
                    ] = "False"
                SettingsTreeWidget.logger.info(
                    object_list[0] + " " + object_list[2] + " disabled"
                )
                for col in range(self.columnCount()):
                    _twi.setToolTip(col, _tt[0])

            self.update_code("CLI.h", object_list[2], True)

            if object_list[2] == "outputToStream":
                self.update_code("CLI.h", object_list[2], True)

            elif object_list[2] == "defaultFunction":
                if combobox.currentText() == "Enabled":
                    self.cliopt["builtin methods"]["var"]["defaultFunction"] = True
                else:
                    self.cliopt["builtin methods"]["var"]["defaultFunction"] = False
            elif object_list[2] == "listCommands":
                if combobox.currentText() == "Enabled":
                    self.command_tree.add_command_to_tree(
                        self.command_tree.invisibleRootItem(), "listCommands"
                    )
                else:
                    if self.cliopt["builtin methods"]["var"]["listCommands"] == True:
                        self.command_tree.remove_command_from_tree("listCommands")
            elif object_list[2] == "listSettings":
                if combobox.currentText() == "Enabled":
                    self.command_tree.add_command_to_tree(
                        self.command_tree.invisibleRootItem(), "listSettings"
                    )
                else:
                    if self.cliopt["builtin methods"]["var"]["listSettings"] == True:
                        self.command_tree.remove_command_from_tree("listSettings")
            self.update_code("functions.h", object_list[2], True)
            self.update_code("parameters.h", object_list[2], True)
            self.update_code("CLI.h", object_list[2], True)

        # if object_list[0] != "builtin methods":
        else:
            _twi = self.currentItem()
            object_data = self.get_object_data(_twi)
            info = self.cliopt["config"]["var"][object_data["pos"][0]][
                object_data["pos"][2]
            ]
            if combobox.currentText() == "Enabled":
                info["value"] = "True"
                # self.log_settings_tree_edit(_twi)
                for col in range(self.columnCount()):
                    _twi.setToolTip(col, _tt[1])
            elif combobox.currentText() == "Disabled":
                info["value"] = "False"
                # self.log_settings_tree_edit(_twi)
                for col in range(self.columnCount()):
                    _twi.setToolTip(col, _tt[0])
            self.update_code("config.h", object_data["pos"][2], True)

    ## this is called after determining if an item is editable
    def edit_settings_tree_item(self, item):
        widget_present = self.itemWidget(item, 0)
        if widget_present != None:
            # self.edit_table_widget_item(widget_present)
            widget_present.edit(widget_present.currentIndex())
            return
        self.log_settings_tree_edit(item)
        self.editItem(item, 3)

    ## called when a user "activates" a tree item (by pressing enter)
    def settings_tree_item_activated(self, item):
        # expand/collapse QTreeWidgetItem that has children, if it has them
        if item.childCount() > 0:
            if item.isExpanded():
                item.setExpanded(False)
            else:
                item.setExpanded(True)
            return
        object_list = str(item.data(4, 0)).split(",")
        SettingsTreeWidget.logger.info(object_list[2] + " selected")
        self.edit_settings_tree_item(item)

    ## if the user double clicks on something, see if it is editable
    def check_if_settings_tree_col_editable(self, item, column):
        # allow the third column to be editable with mouse clicks
        if column == 3:
            self.edit_settings_tree_item(item)

    def log_settings_tree_edit(self, item, object_data=None):
        if object_data == None:
            object_data = self.get_object_data(item)
        if object_data["pos"][0] in self.cliopt:
            info = self.cliopt[object_data["pos"][0]]["var"][object_data["pos"][2]]
        else:
            info = self.cliopt["config"]["var"][object_data["pos"][0]][
                object_data["pos"][2]
            ]
        val_type = object_data["type"]
        val = object_data["value"]
        if self._parent.loading:
            SettingsTreeWidget.logger.info(
                "Preference set "
                + object_data["pos"][2]
                + " to "
                + "'"
                + str(val)
                + "' "
                + str(val_type)
            )
        else:
            SettingsTreeWidget.logger.info(
                "User set "
                + object_data["pos"][2]
                + " to "
                + "'"
                + str(val)
                + "' "
                + str(val_type)
            )
        SettingsTreeWidget.logger.debug(
            str(
                "self.cli_options['config']['var']['{}']:".format(object_data["pos"][2])
            )
            + "\n"
            + str(
                json.dumps(info, indent=2, sort_keys=False, default=lambda o: "object")
            )
        )

    def get_object_data(self, item):
        retval = {"type": "", "value": "", "pos": []}
        object_data_pos_string = str(item.data(4, 0))
        object_data_pos_list = object_data_pos_string.strip("\n").split(",")
        if len(object_data_pos_list) < 2:
            return -1
        else:
            retval["type"] = str(item.data(2, 0))
            item_widget = self._parent.settings_tree.itemWidget(item, 3)
            if isinstance(item_widget, QComboBox):
                string = item_widget.currentText()
                if string == "Enabled":
                    retval["value"] = "True"
                else:
                    retval["value"] = "False"
            else:
                retval["value"] = str(item.data(3, 0))
            retval["pos"] = object_data_pos_list
            return retval

    ## this is called any time an item changes; any time any column edits take place on settings tree, user or otherwise
    def settings_tree_edit_complete(self, item, col):
        self.prompt_to_save = True
        self.windowtitle_set = False
        if col != 3:
            return
        object_data = self.get_object_data(item)

        val = object_data["value"]
        if "'" in str(val):
            return  # already repr

        if object_data["pos"][0] == "builtin methods":
            return
        object_data["pos"][1] = int(str(object_data["pos"][1]))

        # process output
        if object_data["pos"][0] == "process output":
            item.setText(3, str(repr(val)))
            self.cliopt["process output"]["var"][object_data["pos"][2]] = val
            self.log_settings_tree_edit(item, object_data)
            self.update_code("CLI.h", object_data["pos"][2], True)
            if object_data["pos"][2] == "defaultFunction":
                self.update_code("functions.h", object_data["pos"][2], True)
            return

        # process parameters (CLI.h)
        if object_data["pos"][0] == "process parameters":
            item.setText(3, "'" + str(val) + "'")
            self.log_settings_tree_edit(item, object_data)
            self.cliopt["process parameters"]["var"][item.text(1)] = val
            self.update_code("CLI.h", val, True)
            return

        # config.h
        info = self.cliopt["config"]["var"][object_data["pos"][0]][
            object_data["pos"][2]
        ]
        tmp = ""
        if val == "True":
            tmp = True
        elif val == "False":
            tmp = False
        else:
            if val == "":
                tmp = 0
                item.setText(3, "'" + str(repr(tmp)) + "'")
            else:
                try:
                    tmp = str(int(val)).strip("'")
                except:
                    tmp = str(val).strip("'")
                item.setText(3, "'" + str(repr(tmp)) + "'")
        if tmp == info["value"]:
            return
        # update the config dict
        info["value"] = tmp
        self.update_settings_tree_type_field_text(item)
        self.update_code("config.h", object_data["pos"][2], True)
        self.log_settings_tree_edit(item, object_data)

    ## this is called after determining if an item is editable
    def edit_item(self, item):
        widget_present = self.itemWidget(item, 0)
        if widget_present != None:
            # self.edit_table_widget_item(widget_present)
            widget_present.edit(widget_present.currentIndex())
            return
        self.log_settings_tree_edit(item)
        self.editItem(item, 3)


## mainwindow runs on top of "RootWidget"
class RootWidget(QWidget, object):
    def __init__(self, parent) -> None:
        super(RootWidget, self).__init__()
        self._parent = parent
        self.setObjectName("root")

    # shim
    def import_methods(self):
        self.app = self._parent.app
        self.mainwindow_screen = self._parent.mainwindow_screen
        self.create_qdialog = self._parent.create_qdialog
        self.write_cli_gen_tool_json = self._parent.write_cli_gen_tool_json
        self.write_json = self._parent.write_json
        self.read_json = self._parent.read_json
        self.create_file_error_qdialog = self._parent.create_file_error_qdialog
        self.get_project_dir = self._parent.get_project_dir
        self.open_file = self._parent.open_file

        self.root_log_handler = self._parent.root_log_handler
        self.setup_file_handler = self._parent.setup_file_handler
        self.get_child_logger = self._parent.get_child_logger
        self.set_up_window_history_logger = self._parent.set_up_window_history_logger
        self.logger = self.root_log_handler

        self.lib_root_path = self._parent.lib_root_path

        self.lib_version = self._parent.lib_version

        self.inputhandler_save_path = self._parent.inputhandler_save_path
        self.user_home_dir = self._parent.user_home_dir
        self.set_up_session = self._parent.set_up_session

        self.version = self._parent.version
        self.splashscreen_duration = self._parent.splashscreen_duration
