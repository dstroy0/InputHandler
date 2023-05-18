##
# @file gui_code_generation.py
# @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
# @brief MainWindow external methods
# @version 1.0
# @date 2023-005-17
# @copyright Copyright (c) 2023
# Copyright (C) 2023 Douglas Quigg (dstroy0) <dquigg123@gmail.com>
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 3 as published by the Free Software Foundation.

from __future__ import absolute_import

# pyside imports
from PySide6.QtCore import (
    QEvent,
    QObject,
    Signal,
)

from PySide6.QtWidgets import (
    QWidget,
    QStyle,
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
from modules.widgets import CodePreviewWidget


# TODO rename GUICodeGeneration
# code generation and preview
class GUICodeGeneration(
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
        super().__init__()
        self.codegen_logger = self.get_child_logger(__name__)
        self._parent = self
        self.session = self._parent.session
        self.minimum_file_len = self.minimum_file_len
        self.input_config_file_lines = self.input_config_file_lines
        self.cli_options = self.cli_options
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
            GUICodeGeneration.logger.info(
                "set session output_dir to:\n" + str(project_path)
            )
            self.ui.generateDialog.dlg.outputPathLineEdit.setText(
                self.session["opt"]["cli_output_dir"]
            )
            arduino_compatibility = self.detect_output_type(project_path)
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
        GUICodeGeneration.logger.info("platformio file output structure selected")

    def generatedialog_clicked_arduino_file_output_structure(self):
        GUICodeGeneration.logger.info("arduino file output structure selected")

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
            self.cli_options,
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
            self.cli_options,
        )
        self.tab_1._cursor = self.qcursor
        container.layout.addWidget(self.tab_2)
        container.setLayout(container.layout)
        self.tab_2.viewport().installEventFilter(self.tab_2)


# end of file
