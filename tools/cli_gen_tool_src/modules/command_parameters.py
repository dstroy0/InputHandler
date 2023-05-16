##
# @file command_parameters.py
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

import copy

# pyside imports
from PySide6.QtCore import QRegularExpression, Qt
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import (
    QStyle,
    QLineEdit,
    QComboBox,
    QSpinBox,
    QWidget,
    QDialog,
    QTableWidgetItem,
    QHeaderView,
)

# data models
from modules.data_models import dataModels
from modules.display_models import displayModels
from modules.mainwindow_methods import TableButtonBox


# command parameters methods
class CommandParametersMethods(object):
    """All things related to CommandParametersDialog operation

    Args:
        object (class): Base class object

    Returns:
        None: None
    """

    ## edit command sentinel
    editing_existing_command = False

    ## command being edited parameters key
    existing_command_parameters_key = ""

    ## Command parameters dicts are constructed using keys from this list.
    command_parameters_dict_keys_list = dataModels.command_parameters_dict_keys_list

    ## Acceptable command argument types.
    command_arg_types_list = dataModels.command_arg_types_list

    ## the constructor
    def __init__(self) -> None:
        """Constructor method"""
        super(CommandParametersMethods, self).__init__()
        CommandParametersMethods.logger = self.get_child_logger(__name__)
        self.create_qdialog = self.create_qdialog
        self.cliopt = self.cli_options
        # inherit from parameters.py
        self.generate_commandarguments_string = self.generate_commandarguments_string
        self.parse_commandarguments_string = self.parse_commandarguments_string

    def build_commandparameters_dialog_arg_table(self, command_parameters):
        args = command_parameters["commandArguments"]
        args_list = self.parse_commandarguments_string(args)
        self.generate_commandparameters_arg_table(args_list)

    def generate_commandparameters_arg_table(self, args_list: list):
        table = self.ui.commandParameters.dlg.argTable
        table._cursor = self.qcursor
        table.clear()
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(["type", "controls"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        table.setRowCount(len(args_list))

        for r in range(len(args_list)):
            type_item = QTableWidgetItem()
            type_item.setData(0, args_list[r])
            type_item.setToolTip(
                displayModels.argument_table_tooltip_dict[args_list[r]]
            )
            table.setItem(r, 0, type_item)
            control_item = QTableWidgetItem()
            table.setItem(r, 1, control_item)
            table.setCellWidget(r, 1, TableButtonBox(table))

    def get_args_from_commandparameters_arg_table(self) -> list:
        table = self.ui.commandParameters.dlg.argTable
        arg_list = []
        for r in range(table.rowCount()):
            item_data = table.item(r, 0).data(0)
            arg_list.append(item_data)
        return arg_list

    def set_up_command_parameters_dialog(self, ui):
        """sets up command parameters dialog

        Args:
            ui (class): command parameters ui
        """
        # load command parameters input dialog ui
        self.ui.commandParameters = QDialog(self)
        # blue circle question icon
        self.ui.commandParameters.setWindowIcon(
            QWidget().style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxQuestion)
        )
        self.ui.commandParameters.dlg = ui
        self.ui.commandParameters.dlg.setupUi(self.ui.commandParameters)
        self.ui.commandParameters.setMaximumSize(0, 0)

        # CommandParameters user input objects
        self.command_parameters_user_input_objects = {
            # line edit
            "returnFunctionName": self.ui.commandParameters.dlg.returnFunctionName,
            # line edit
            "commandString": self.ui.commandParameters.dlg.commandString,
            # read only label
            "commandLength": self.ui.commandParameters.dlg.commandLengthLabel,
            # line edit
            "parentId": self.ui.commandParameters.dlg.commandParentId,
            # line edit
            "commandId": self.ui.commandParameters.dlg.commandId,
            # check box
            "commandHasWildcards": self.ui.commandParameters.dlg.commandHasWildcards,
            # spinbox
            "commandDepth": self.ui.commandParameters.dlg.commandDepth,
            # spinbox
            "commandSubcommands": self.ui.commandParameters.dlg.commandSubcommands,
            # combobox
            "commandArgumentHandling": self.ui.commandParameters.dlg.commandArgumentHandling,
            # spinbox
            "commandMinArgs": self.ui.commandParameters.dlg.commandMinArgs,
            # spinbox
            "commandMaxArgs": self.ui.commandParameters.dlg.commandMaxArgs,
        }

        self.command_parameters_input_field_settings = (
            dataModels.command_parameters_input_field_settings_dict
        )
        # set input field defaults
        self.set_commandparameters_field_defaults()
        # command parameters dialog box setup
        cmd_dlg = self.ui.commandParameters.dlg
        # This dict contains regexp strings and int limits for user input
        # the values are placeholder values and will change on user interaction
        cmd_dlg.validatorDict = {
            "returnFunctionName": "^([a-zA-Z_])+$",
            "commandString": "^([a-zA-Z_*])+$",
            "commandParentId": "^([0-9])+$",
            "commandId": "^([0-9])+$",
            "commandDepth": 255,
            "commandSubcommands": 255,
            "commandMinArgs": 255,
            "commandMaxArgs": 255,
        }
        # set validators to user preset or defaults
        self.set_command_parameter_validators()
        # user interaction triggers
        self.set_command_parameters_triggers()
        # argumentsPane QWidget is automatically enabled/disabled with the setting of the arguments handling combobox
        # set False by default
        cmd_dlg.argumentsPane.setEnabled(False)
        combobox_word_list = displayModels.argument_table_tooltip_dict.keys()
        cmd_dlg.argComboBox.addItems(combobox_word_list)

    ## spawns a regexp validator
    def regex_validator(self, input: str):
        """Turns a string into a QRegularExpressionValidator"""
        exp = QRegularExpression(input)
        return QRegularExpressionValidator(exp)

    # TODO search entire command tree for duplicate commandString
    ## simple user input validation
    def validate_command_parameters(self) -> dict:
        """validates input command parameters

        Returns:
            dict: key 0 is bool; True on success.  key 1 is a dict of the input parameters.
        """
        wildcard_flag_strings = dataModels.wildcard_flag_strings

        arg_handling_strings = dataModels.arg_handling_strings

        error_list = []
        settings_to_validate = dict.fromkeys(
            CommandParametersMethods.command_parameters_dict_keys_list, None
        )
        settings_to_validate[
            "returnFunctionName"
        ] = self.command_parameters_user_input_objects["returnFunctionName"].text()
        settings_to_validate["functionName"] = str(
            str(self.command_parameters_user_input_objects["commandString"].text())
            + "_"
            + str(self.cli_options["commands"]["primary id key"])
        )
        settings_to_validate[
            "commandString"
        ] = self.command_parameters_user_input_objects["commandString"].text()
        settings_to_validate["commandLength"] = str(
            len(settings_to_validate["commandString"])
        )
        settings_to_validate["parentId"] = self.command_parameters_user_input_objects[
            "parentId"
        ].text()
        settings_to_validate["commandId"] = self.command_parameters_user_input_objects[
            "commandId"
        ].text()
        settings_to_validate["commandHasWildcards"] = wildcard_flag_strings[
            int(
                self.command_parameters_user_input_objects[
                    "commandHasWildcards"
                ].isChecked()
            )
        ]
        settings_to_validate[
            "commandDepth"
        ] = self.command_parameters_user_input_objects["commandDepth"].text()
        settings_to_validate[
            "commandSubcommands"
        ] = self.command_parameters_user_input_objects["commandSubcommands"].text()
        settings_to_validate["commandArgumentHandling"] = arg_handling_strings[
            self.command_parameters_user_input_objects[
                "commandArgumentHandling"
            ].currentIndex()
        ]
        settings_to_validate[
            "commandMinArgs"
        ] = self.command_parameters_user_input_objects["commandMinArgs"].text()
        settings_to_validate[
            "commandMaxArgs"
        ] = self.command_parameters_user_input_objects["commandMaxArgs"].text()
        # err is the error sentinel
        err = False

        if settings_to_validate["commandString"] == "":
            error_list.append("'Command string' cannot be empty")
            err = True
        if int(settings_to_validate["commandLength"]) == 0:
            error_list.append("'Command length' cannot be zero")
            err = True
        if settings_to_validate["parentId"] == "":
            error_list.append("'Parent id' cannot be blank")
            err = True
        elif int(settings_to_validate["parentId"]) > 65535:
            error_list.append("'Parent id' cannot be greater than 65535")
            err = True
        if settings_to_validate["commandId"] == "":
            error_list.append("'Command id' cannot be blank")
            err = True
        elif int(settings_to_validate["commandId"]) > 65535:
            error_list.append("'Command id' cannot be greater than 65535")
            err = True
        if settings_to_validate["commandDepth"] == "":
            error_list.append("'Command depth' cannot be blank")
            err = True
        elif int(settings_to_validate["commandDepth"]) > 255:
            error_list.append("'Command depth' cannot be greater than 255")
            err = True
        if settings_to_validate["commandSubcommands"] == "":
            error_list.append("'Subcommands' cannot be blank")
            err = True
        elif int(settings_to_validate["commandSubcommands"]) > 255:
            error_list.append(
                "'Subcommands'; Command cannot have more than 255 subcommands"
            )
            err = True
        arg_handling_idx = self.command_parameters_user_input_objects[
            "commandArgumentHandling"
        ].currentIndex()
        if arg_handling_idx == 0:
            settings_to_validate[
                "commandArguments"
            ] = self.generate_commandarguments_string(
                [self.get_args_from_commandparameters_arg_table()[0]]
            )
        elif arg_handling_idx == 1:
            args_list = self.get_args_from_commandparameters_arg_table()
            # single argument
            if not bool(args_list):
                err = True
                error_list.append(
                    "'Arguments' field cannot be blank with current 'Argument Handling' selection"
                )
            if settings_to_validate["returnFunctionName"] == "":
                error_list.append(
                    "'Return function name' cannot be empty with current 'Argument Handling' selection"
                )
            settings_to_validate[
                "commandArguments"
            ] = self.generate_commandarguments_string(args_list)
        elif arg_handling_idx == 2:
            args_list = self.get_args_from_commandparameters_arg_table()
            # argument array
            if not bool(args_list):
                err = True
                error_list.append(
                    "'Arguments' field cannot be blank with current 'Argument Handling' selection"
                )
            if settings_to_validate["returnFunctionName"] == "":
                error_list.append(
                    "'Return function name' cannot be empty with current 'Argument Handling' selection"
                )
            settings_to_validate[
                "commandArguments"
            ] = self.generate_commandarguments_string(args_list)
        CommandParametersMethods.logger.debug(settings_to_validate)
        CommandParametersMethods.logger.debug(error_list)
        if err == True:
            self.err_settings_to_validate(error_list)
        return {0: err, 1: settings_to_validate}

    ## create error dialog where `error_list` contains error text
    def err_settings_to_validate(self, error_list: list) -> None:
        """Creates a popup dialog listing the errors found in the input parameters.

        Args:
            error_list (list): A human readable list of errors found.
        """
        error_text = ""
        for item in error_list:
            error_text += item
            if item != error_list[len(error_list) - 1]:
                error_text += "\n"
        self.create_qdialog(
            error_text,
            Qt.AlignLeft,
            0,
            "Command Parameters Error",
            None,
            None,
            QStyle.StandardPixmap.SP_MessageBoxCritical,
        )

    ## sets the regexp and range validators for CommandParameters input
    def set_command_parameter_validators(self) -> None:
        """Sets CommandParametersDialog input validators."""
        cmd_dlg = self.ui.commandParameters.dlg
        # allowed function name char
        cmd_dlg.returnFunctionName.setValidator(
            self.regex_validator(cmd_dlg.validatorDict["returnFunctionName"])
        )
        # allowed command string char
        cmd_dlg.commandString.setValidator(
            self.regex_validator(cmd_dlg.validatorDict["commandString"])
        )
        cmd_dlg.commandParentId.setValidator(
            self.regex_validator(cmd_dlg.validatorDict["commandParentId"])
        )
        cmd_dlg.commandId.setValidator(
            self.regex_validator(cmd_dlg.validatorDict["commandId"])
        )
        cmd_dlg.commandDepth.setMaximum(cmd_dlg.validatorDict["commandDepth"])
        cmd_dlg.commandSubcommands.setMaximum(
            cmd_dlg.validatorDict["commandSubcommands"]
        )
        cmd_dlg.commandMinArgs.setMaximum(cmd_dlg.validatorDict["commandMinArgs"])
        cmd_dlg.commandMaxArgs.setMaximum(cmd_dlg.validatorDict["commandMaxArgs"])

    ## triggers related to the command parameters dialog
    def set_command_parameters_triggers(self) -> None:
        """Set up interaction triggers for CommandParametersDialog"""
        cmd_dlg = self.ui.commandParameters.dlg
        cmd_dlg.reset.clicked.connect(self.clicked_command_parameters_buttonbox_reset)
        cmd_dlg.ok.clicked.connect(self.clicked_command_parameters_buttonbox_ok)
        cmd_dlg.cancel.clicked.connect(self.clicked_command_parameters_buttonbox_cancel)
        cmd_dlg.commandArgumentHandling.currentIndexChanged.connect(
            self.argument_handling_changed
        )
        cmd_dlg.commandString.textChanged.connect(self.command_string_text_changed)
        cmd_dlg.insert.clicked.connect(self.insert_arg)

    def insert_arg(self):
        cmb = self.ui.commandParameters.dlg.argComboBox
        table = self.ui.commandParameters.dlg.argTable
        selected_item = table.currentItem()
        arg_list = self.get_args_from_commandparameters_arg_table()

        if not bool(selected_item):
            arg_list.append(cmb.currentText())
            cell_row = table.rowCount()
        else:
            row = table.row(selected_item)
            cell_row = row + 1
            arg_list.insert(row + 1, cmb.currentText())
        self.generate_commandparameters_arg_table(arg_list)
        table.setCurrentCell(cell_row, 0)

    def edit_existing_command(self, parameters_key):
        fields = copy.deepcopy(dataModels.command_parameters_input_field_settings_dict)
        command_parameters = self.cli_options["commands"]["parameters"][parameters_key]
        for key in fields:
            fields[key]["value"] = command_parameters[key]
        self.commandparameters_set_fields(fields)
        self.ui.commandParameters.dlg.defaults = fields
        CommandParametersMethods.editing_existing_command = True
        CommandParametersMethods.existing_command_parameters_key = parameters_key
        parameters = self.cliopt["commands"]["parameters"][parameters_key]
        self.build_commandparameters_dialog_arg_table(parameters)
        self.ui.commandParameters.exec()

    ## command parameters dialog buttonbox ok
    def clicked_command_parameters_buttonbox_ok(self) -> None:
        """This function is reached when the user clicks `ok` on the CommandParametersDialog"""
        CommandParametersMethods.logger.debug("clicked ok on command parameters menu")
        validate_result = self.validate_command_parameters()
        # error
        if validate_result[0] == True:
            CommandParametersMethods.logger.info(
                "one or more errors were detected in the input command parameters"
            )
            return
        validated_result = {}
        validated_result = validate_result[1]

        # edit commands
        if CommandParametersMethods.editing_existing_command == True:
            CommandParametersMethods.editing_existing_command = False  # reset state
            self.cli_options["commands"]["parameters"].pop(
                CommandParametersMethods.existing_command_parameters_key
            )
            self.cli_options["commands"]["parameters"].update(
                {
                    CommandParametersMethods.existing_command_parameters_key: validated_result
                }
            )
            CommandParametersMethods.existing_command_parameters_key = (
                ""  # reset parameters key
            )
            self.update_code("parameters.h", validated_result["functionName"], True)
            self.update_code("functions.h", validated_result["functionName"], True)
            self.update_code("CLI.h", validated_result["functionName"], True)
            self.update_code("README.md", validated_result["functionName"], True)
            self.command_tree.update_command(self.command_tree.active_item)
            self.ui.commandParameters.close()
            return

        # new commands
        cmd_idx = str(self.cli_options["commands"]["primary id key"])
        # root command
        if (
            self.command_tree.active_item == self.command_tree.invisibleRootItem()
            or self.command_tree.active_item == None
        ):
            # make dict from defined keys
            self.cli_options["commands"]["parameters"].update(
                {cmd_idx: validated_result}
            )
            self.command_tree.add_command_to_tree(self.command_tree.invisibleRootItem())
        # non root command
        else:
            parent_string = ""
            if (
                self.command_tree.active_item.data(0, 0) == None
                and self.command_tree.active_item.parent is not None
            ):
                parent_string = self.command_tree.active_item.parent().data(0, 0)
            else:
                parent_string = str(self.command_tree.active_item.data(0, 0))
            items = self.command_tree.findItems(
                parent_string, Qt.MatchWrap | Qt.MatchRecursive, 0
            )
            self.cli_options["commands"]["parameters"].update(
                {cmd_idx: validated_result}
            )
            if items:
                parent = items[0]
                cmd_idx_key = parent.data(1, 0)
                cmd_idx = self.cliopt["commands"]["index"]
                prm_key = cmd_idx[cmd_idx_key]["parameters key"]
                prm = self.cliopt["commands"]["parameters"][prm_key]
                subcommands = int(prm["commandSubcommands"]) + 1
                prm["commandSubcommands"] = str(subcommands)
                self.command_tree.add_command_to_tree(parent)
                CommandParametersMethods.logger.info(
                    parent_string + " commandSubcommands = " + str(subcommands)
                )
            else:
                CommandParametersMethods.logger.info("couldn't find parent")

        self.update_code("parameters.h", validated_result["functionName"], True)
        self.update_code("functions.h", validated_result["functionName"], True)
        self.update_code("CLI.h", validated_result["functionName"], True)
        self.update_code("README.md", validated_result["functionName"], True)
        self.ui.commandParameters.close()

    ## command parameters dialog buttonbox reset value
    def clicked_command_parameters_buttonbox_reset(self) -> None:
        """This function is reached if the user clicked `reset` on CommandParametersDialog."""
        CommandParametersMethods.logger.info("reset")
        cmd_dlg = self.ui.commandParameters.dlg
        self.commandparameters_set_fields(cmd_dlg.defaults)

    ## command parameters dialog buttonbox cancel changes
    def clicked_command_parameters_buttonbox_cancel(self) -> None:
        """This function is reached if the user clicked `cancel` on CommandParametersDialog."""
        CommandParametersMethods.logger.info("cancel")
        self.ui.commandParameters.close()

    ## refreshes `commandLength`
    def command_string_text_changed(self) -> None:
        """Updates `commandLength` when the user enters or removes
        characters from `commandString`
        """
        cmd_dlg = self.ui.commandParameters.dlg
        cmd_dlg.commandLengthLabel.setText(str(len(cmd_dlg.commandString.text())))

    ## command parameters dialog argument handling combobox index changed
    def argument_handling_changed(self) -> None:
        """This function is reached if the user changes the position
        of the `Argument Handling` combobox on CommandParametersDialog.
        """
        CommandParametersMethods.logger.info("argument handling changed")
        cmd_dlg = self.ui.commandParameters.dlg
        if cmd_dlg.commandArgumentHandling.currentIndex() != 0:
            cmd_dlg.argumentsPane.setEnabled(True)
        else:
            cmd_dlg.argumentsPane.setEnabled(False)

    def commandparameters_set_fields(self, _fields: dict) -> None:
        """Sets the fields of CommandParametersDialog to the values
        of the command being edited.

        Args:
            _fields (dict): This contains all of the values being set in the CommandParametersDialog that is being launched.
        """
        if not bool(_fields):
            for key in self.command_parameters_user_input_objects:
                if isinstance(
                    self.command_parameters_user_input_objects[key], QLineEdit
                ):
                    self.command_parameters_user_input_objects[key].setText("")
                if isinstance(
                    self.command_parameters_user_input_objects[key], QSpinBox
                ):
                    self.command_parameters_user_input_objects[key].setValue(0)
                if isinstance(
                    self.command_parameters_user_input_objects[key], QComboBox
                ):
                    self.command_parameters_user_input_objects[key].setCurrentIndex(0)
                self.command_parameters_user_input_objects[key].setEnabled(False)
        else:
            for key in _fields:
                if key in self.command_parameters_user_input_objects:
                    if isinstance(
                        self.command_parameters_user_input_objects[key], QLineEdit
                    ):
                        if key != "commandArguments":
                            self.command_parameters_user_input_objects[key].setText(
                                str(_fields[key]["value"])
                            )
                    elif isinstance(
                        self.command_parameters_user_input_objects[key], QSpinBox
                    ):
                        self.command_parameters_user_input_objects[key].setValue(
                            int(_fields[key]["value"])
                        )
                    elif isinstance(
                        self.command_parameters_user_input_objects[key], QComboBox
                    ):
                        self.command_parameters_user_input_objects[key].setCurrentIndex(
                            dataModels.arg_handling_strings.index(_fields[key]["value"])
                        )

                    self.command_parameters_user_input_objects[key].setEnabled(
                        _fields[key]["enabled"]
                    )
                    CommandParametersMethods.logger.debug(
                        str(key)
                        + " field"
                        + str(_fields[key]["value"])
                        + " "
                        + str(_fields[key]["enabled"])
                    )
                else:
                    CommandParametersMethods.logger.debug("unknown field: " + str(key))

    def set_commandparameters_field_defaults(self) -> None:
        """This function sets the DEFAULT values for CommandParametersDialog."""
        # CommandParameters default field values
        inp_setup = self.command_parameters_input_field_settings
        inp_setup["returnFunctionName"]["value"] = ""
        inp_setup["commandString"]["value"] = ""
        inp_setup["commandLength"]["value"] = "0"
        inp_setup["parentId"]["value"] = 0
        inp_setup["commandId"]["value"] = 0
        inp_setup["commandHasWildcards"]["value"] = False
        inp_setup["commandDepth"]["value"] = 0
        inp_setup["commandSubcommands"]["value"] = 0
        inp_setup["commandArgumentHandling"]["value"] = dataModels.arg_handling_strings[
            0
        ]
        inp_setup["commandMinArgs"]["value"] = 0
        inp_setup["commandMaxArgs"]["value"] = 0
        inp_setup["commandArguments"]["value"] = "{{UITYPE::NO_ARGS}}"


# end of file
