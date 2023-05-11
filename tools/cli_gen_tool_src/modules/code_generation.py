##
# @file code_generation.py
# @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
# @brief MainWindow external methods
# @version 1.0
# @date 2022-12-13
# @copyright Copyright (c) 2022
# Copyright (C) 2022 Douglas Quigg (dstroy0) <dquigg123@gmail.com>
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 3 as published by the Free Software Foundation.

from __future__ import absolute_import

import os
import glob
import shutil
import datetime

# pyside imports
from PySide6.QtCore import (
    QRect,
    QSize,
    Qt,
    QEvent,
    QObject,
    QUrl,
    Slot,
    QPoint,
    QDir,
    QIODevice,
    QByteArray,
    QFile,
    Signal,
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
    QVBoxLayout,
    QPushButton,
    QDialog,
    QDialogButtonBox,
)

# external methods and resources
from modules.cli.clireadme import cliReadme
from modules.cli.config import cliConfig
from modules.cli.CLI import cliH
from modules.cli.functions import cliFunctions
from modules.cli.parameters import cliParameters
from modules.cli.filestrings import cliFileStrings
from modules.cli.parse_config import ParseInputHandlerConfig
from modules.data_models import dataModels


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


# code generation and preview
class CodeGeneration(
    ParseInputHandlerConfig,
    cliFileStrings,
    cliReadme,
    cliConfig,
    cliH,
    cliFunctions,
    cliParameters,
    object,
):
    """Generates code for display and writing to disk

    Args:
        ParseInputHandlerConfig (CodeGeneration): config.h parser
        cliFileStrings (CodeGeneration): cli filestrings
        cliReadme (CodeGeneration): generates README.md
        cliConfig (CodeGeneration): generates config.h
        cliH (CodeGeneration): generates CLI.h
        cliFunctions (CodeGeneration): generates functions.h
        cliParameters (CodeGeneration): generates parameters.h
        object (object): base object specialization
    """

    def __init__(self) -> None:
        """Constructor method"""
        super(CodeGeneration, self).__init__()
        self.codegen_logger = self.get_child_logger(__name__)
        self._parent = self
        self.session = self._parent.session
        self.minimum_file_len = self.minimum_file_len
        self.input_config_file_lines = self.input_config_file_lines
        self.cliOpt = self.cliOpt
        self.qcursor = self.qcursor
        self.tab_1 = ""
        self.tab_2 = ""

        ParseInputHandlerConfig.__init__(self)
        cliFileStrings.__init__(self)
        cliReadme.__init__(self)
        cliConfig.__init__(self)
        cliH.__init__(self)
        cliFunctions.__init__(self)
        cliParameters.__init__(self)

    def generatedialog_set_output_dir(self):
        project_path = self._parent.get_project_dir()
        if project_path:
            self.session["opt"]["cli_output_dir"] = project_path
            CodeGeneration.logger.info(
                "set session output_dir to:\n" + str(project_path)
            )
            self.ui.generateDialog.dlg.outputPathLineEdit.setText(
                self.session["opt"]["cli_output_dir"]
            )
            arduino_compatibility = self.detect_output_type(project_path)
            print(arduino_compatibility)
            if arduino_compatibility:
                self._parent.ui.generateDialog.dlg.arduinoRadioButton.setChecked(True)
            else:
                self._parent.ui.generateDialog.dlg.platformioRadioButton.setChecked(
                    True
                )
            self._parent.ui.generateDialog.dlg.buttonBox.button(
                QDialogButtonBox.StandardButton.Ok
            ).setEnabled(True)
        else:
            self._parent.ui.generateDialog.dlg.buttonBox.button(
                QDialogButtonBox.StandardButton.Ok
            ).setEnabled(False)

    def generatedialog_clicked_platformio_file_output_structure(self):
        CodeGeneration.logger.info("platformio file output structure selected")

    def generatedialog_clicked_arduino_file_output_structure(self):
        CodeGeneration.logger.info("arduino file output structure selected")

    def clickable(self, widget):
        """makes objects emit "clicked"

        Args:
            widget (QWidget): the widget to attach the signal to

        Returns:
            Filter (QObject): the filtered object interaction
        """

        class Filter(QObject):
            clicked = Signal()

            def eventFilter(self, obj, event):
                if (
                    obj == widget
                    and event.type() == QEvent.MouseButtonRelease
                    and obj.rect().contains(event.pos())
                ):
                    self.clicked.emit()
                    return True
                else:
                    return False

        filter = Filter(widget)
        widget.installEventFilter(filter)
        return filter.clicked

    def cli_generation_dialog_setup(self, ui):
        self = self._parent
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
            self.session["opt"]["cli_output_dir"]
        )
        self.ui.generateDialog.dlg.pushButton.clicked.connect(
            self.generatedialog_set_output_dir
        )
        self.ui.generateDialog.dlg.buttonBox.accepted.connect(self.generate_cli_files)
        self.ui.generateDialog.dlg.buttonBox.rejected.connect(
            self.ui.generateDialog.close
        )
        arduino_compatibility = self.detect_output_type(
            self.session["opt"]["cli_output_dir"]
        )
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
        self.clickable(self.ui.generateDialog.dlg.outputPathLineEdit).connect(
            self.generatedialog_set_output_dir
        )

    def parse_config(self):
        """config parser wrapper"""
        self.parse_config_header_file(
            self.session["opt"]["inputhandler_config_file_path"]
        )

    def initial_code_preview(self):
        """code preview wrapper"""
        self.tab_1.initial_code_preview()
        self.tab_2.initial_code_preview()

    def update_code(self, file: str, item_string: str, place_cursor: bool) -> None:
        """code update wrapper

        Args:
            file (str): filename
            item_string (str): code to highlight
            place_cursor (bool): place cursor on highlighted code if True.
        """
        self.tab_1.update_code(file, item_string, place_cursor)
        self.tab_2.update_code(file, item_string, place_cursor)

    def set_code_string(
        self,
        filename: str,
        code_string: str,
        item_string: str,
        place_cursor: bool = False,
    ) -> None:
        """sets the code string in `filename` widget

        Args:
            filename (str): cli filename
            code_string (str): file code
            item_string (str): highlighted code
            place_cursor (bool, optional): place cursor on highlighted code if True. Defaults to False.
        """
        self.tab_1.set_code_string(
            filename,
            code_string,
            item_string,
            place_cursor,
        )
        self.tab_2.set_code_string(
            filename,
            code_string,
            item_string,
            place_cursor,
        )

    def display_initial_code_preview(self):
        """displays initial code after loading app"""
        self.tab_1.initial_code_preview()
        self.tab_2.initial_code_preview()

    def make_collapse_button(self) -> QPushButton:
        """makes a QPushButton object that collapses a tree

        Returns:
            QPushButton: a button
        """
        button = QPushButton()
        button.setMaximumSize(150, 25)
        return button

    def build_code_preview_widgets(self):
        """builds code preview widgets"""
        container = self.ui.settings_code_preview_container
        container.layout = QVBoxLayout(container)
        container.collapse_button = self.make_collapse_button()
        container.layout.addWidget(container.collapse_button)
        self.tab_1 = CodePreviewWidget(
            self,
            container,
            self.code_preview_dict,
            self.cliOpt,
        )
        self.tab_1._cursor = self.qcursor
        container.layout.addWidget(self.tab_1)
        container.setLayout(container.layout)
        self.tab_1.viewport().installEventFilter(self.tab_1)

        container = self.ui.commands_code_preview_container
        container.layout = QVBoxLayout(container)
        container.collapse_button = self.make_collapse_button()
        container.layout.addWidget(container.collapse_button)
        self.tab_2 = CodePreviewWidget(
            self,
            container,
            self.code_preview_dict,
            self.cliOpt,
        )
        self.tab_1._cursor = self.qcursor
        container.layout.addWidget(self.tab_2)
        container.setLayout(container.layout)
        self.tab_2.viewport().installEventFilter(self.tab_2)

    # TODO detect file structure as defined in dataModels
    def detect_output_type(self, project_path):
        pio_structure = dataModels.pio_structure
        arduino_structure = dataModels.arduino_structure
        if project_path == None:
            project_path = ""
        ino_search = glob.glob(os.path.join(project_path, "*.ino"))
        arduino_compatibility = False
        if bool(ino_search):
            # ino file detected
            arduino_compatibility = True
        if project_path.find("sketch") != -1:
            # empty sketch folder case
            arduino_compatibility = True
        if arduino_compatibility:
            CodeGeneration.logger.info("detected arduino file structure")
        else:
            CodeGeneration.logger.info("detected platformio file structure")
        return arduino_compatibility

    # TODO revert on fail
    def generate_cli(self, project_path: str = None) -> int:
        """generates the platform appropriate CLI in `project_path`
           set in preferences

        Args:
            project_path (str, optional): valid os path. Defaults to None.

        Returns:
            int:
        """
        if project_path == None:
            project_path = self.session["opt"]["cli_output_dir"]
            if project_path == None or project_path == "" and not self._parent.headless:
                project_path = self.get_project_dir()
            if project_path == None:
                self.codegen_logger.info("Output directory not set")
                return -1
        qdir = QDir()
        src = qdir.toNativeSeparators(self.lib_root_path + "/src/")
        if qdir.exists(src + "InputHandler.h"):
            self.codegen_logger.info("found library")
        else:
            self.codegen_logger.info("couldn't find library; aborting!")
            return -1
        src_path = os.path.abspath(src)

        dst = qdir.toNativeSeparators(project_path)
        if os.path.exists(dst):
            self.codegen_logger.info("found project dir")
        else:
            project_path = self.get_project_dir()
        if os.path.exists(dst):
            self.codegen_logger.info("found project dir")
        else:
            self.codegen_logger.info("invalid project directory!")
            return -1

        self.readme_md(None, False)
        self.config_h(None, False)
        self.cli_h(None, False)
        self.parameters_h(None, False)
        self.functions_h(None, False)

        arduino_compatibility = self.detect_output_type(project_path)

        # TODO use file structure in data models for pathing
        if arduino_compatibility:
            # arduino
            cli_path = os.path.join(project_path, "CLI")
            cli_src_path = os.path.join(cli_path, "src")
            cli_config_h_path = os.path.join(cli_src_path, "config/config.h")
        else:
            # platformio
            cli_path = os.path.join(project_path, "lib", "CLI")
            cli_src_path = cli_path  # os.path.join(cli_path, "src")
            cli_config_h_path = os.path.join(cli_src_path, "config/config.h")

        # Create in project dir
        # /CLI/
        # copy /InputHandler/src/ to project_path/CLI/src/
        # remove original config.h
        if not os.path.exists(cli_path):
            CodeGeneration.logger.info(
                "creating dir <CLI> in <" + str(project_path) + ">"
            )
            shutil.copytree(src_path, cli_src_path)
            os.remove(cli_config_h_path)
            if os.path.exists(cli_src_path):
                CodeGeneration.logger.info(
                    "dir <CLI> created in <" + str(project_path) + ">"
                )
            else:
                CodeGeneration.logger.info(
                    "Error creating dir <CLI> in <"
                    + str(project_path)
                    + "> aborting generation!"
                )
                return -1
        else:
            CodeGeneration.logger.info(
                "dir <CLI> already exists in <" + str(project_path) + ">"
            )
            shutil.rmtree(cli_path)
            shutil.copytree(src_path, cli_src_path)
            os.remove(cli_config_h_path)

        files = self.code_preview_dict["files"].keys()
        for filename in files:
            if filename == "README.md":
                path = os.path.join(project_path, "CLI_" + filename)
                self.write_cli_file(
                    path, self.code_preview_dict["files"][filename], True
                )
                path = os.path.join(cli_path, "library.properties")
                f = {
                    "file_string": self.fsdb["library"]["properties"][
                        "filestring"
                    ].format(lib_version=self.lib_version)
                }
                self.write_cli_file(path, f, True)
            elif filename == "config.h":
                self.write_cli_file(
                    cli_config_h_path, self.code_preview_dict["files"][filename], True
                )
            else:
                path = os.path.join(cli_src_path, filename)
                self.write_cli_file(
                    path, self.code_preview_dict["files"][filename], True
                )

    def write_cli_file(
        self, path: str, dict_to_write: dict, create_error_dialog: bool = False
    ) -> int:
        """writes a file

        Args:
            path (str): path to file
            dict_to_write (dict): file dict
            create_error_dialog (bool, optional): Create error dialog on fail if True. Defaults to False.

        Returns:
            int: the number of bytes written if successful else -1
        """
        qfile = QFile(path)
        if not qfile.open(QIODevice.WriteOnly | QIODevice.Text):
            CodeGeneration.logger.info("Save " + qfile.fileName() + " error.")
            if create_error_dialog:
                self.create_file_error_qdialog("Save file", qfile)
            return -1  # file error

        # file object
        out = QByteArray(dict_to_write["file_string"])

        size = qfile.write(out)
        if size != -1:
            CodeGeneration.logger.info(
                "wrote " + str(size) + " bytes to " + str(qfile.fileName())
            )

        else:
            CodeGeneration.logger.info("Write " + qfile.fileName() + " error.")
            if create_error_dialog:
                self.create_file_error_qdialog("Write file", qfile)
        qfile.close()
        return size


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

        self.cliOpt = parent.cliOpt
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
        self.readme_md(None, False)
        self.config_h(None, False)
        self.cli_h(None, False)
        self.parameters_h(None, False)
        self.functions_h(None, False)

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

    def update_code(self, file: str, item_string: str, place_cursor: bool) -> None:
        """updates code in text_widget.objectName(`file`);
           highlights `item_string` if exists;
           places the cursor on `item_string` if `place_cursor` True.

        Args:
            file (str): filename.extension
            item_string (str): item within `file` that changed, if any.
            place_cursor (bool): place the text cursor on `item_string` if True and `item_string` exists.
        """
        self.logger.debug("update {filename}".format(filename=file))
        # update widgets
        if file == "README.md":
            self.readme_md(item_string, place_cursor)
        if file == "config.h":
            self.config_h(item_string, place_cursor)
        if file == "CLI.h":
            self.cli_h(item_string, place_cursor)
        if file == "parameters.h":
            self.parameters_h(item_string, place_cursor)
        if file == "functions.h":
            self.functions_h(item_string, place_cursor)

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
            len(self.code_preview_dict["files"][filename]["file_lines_list"])
            <= self.minimum_file_len[filename]
        ):
            text_widget.clear()
            self.code_preview_dict["files"][filename]["file_lines_list"] = []
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


# end of file
