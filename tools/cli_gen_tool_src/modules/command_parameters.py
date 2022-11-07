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

import json
import copy

# pyside imports
from PySide6.QtCore import QRegularExpression, Qt
from PySide6.QtGui import QRegularExpressionValidator, QTextCursor
from PySide6.QtWidgets import (
    QDialogButtonBox,
    QStyle,
    QLineEdit,
    QComboBox,
    QPlainTextEdit,
    QSpinBox,    
)

# logging api
from modules.logging_setup import Logger

# data models
from modules.data_models import dataModels


# command parameters methods
class CommandParametersMethods(object):
    """All things related to CommandParametersDialog operation

    Args:
        object (class): Base class object

    Returns:
        None: None
    """
    ## Command parameters dicts are constructed using keys from this list.
    command_parameters_dict_keys_list = dataModels.command_parameters_dict_keys_list

    ## Acceptable command argument types.
    command_arg_types_list = dataModels.command_arg_types_list

    ## the constructor
    def __init__(self) -> None:
        """Constructor method"""
        super(CommandParametersMethods, self).__init__()
        CommandParametersMethods.logger = Logger.get_child_logger(self.logger, __name__)

    ## spawns a regexp validator
    def regex_validator(self, input: str):
        """Turns a pythonic regex string into a regex validator.

        Args:
            input (str): The input regex search string.

        Returns:
            QRegularExpressionValidator: An input validator for a QLineEdit.
        """
        exp = QRegularExpression(input)
        return QRegularExpressionValidator(exp)

    ## generates a dict from csv arguments in the command parameters dialog
    # TODO add text UITYPE:: and comma to returned list items
    def list_from_csv_args(self) -> None:
        """Pulls text from CommandParametersDialog arguments pane, separates
        them into arguments.

        Returns:
            list: A list of arguments.
        """
        args_list = []
        csv = self.ui.commandParameters.dlg.argumentsPlainTextCSV.toPlainText() + ","
        regexp = QRegularExpression('("(?:[^"]|")*"|[^,"\n\r]*)(,|\r?\n|\r)')
        csv_pos = 0
        i = 0
        while csv_pos != -1:
            match = regexp.match(csv, csv_pos)
            if match.hasMatch():
                csv_pos += match.capturedLength()
                if (
                    match.captured().upper().strip(",")
                ) in CommandParametersMethods.command_arg_types_list:
                    args_list.append(i)
                    i = i + 1
            else:
                break
        return args_list

    ## all buttons related to adding/removing arguments from the command parameters dialog
    def csv_button(self) -> None:
        """Buttons related to adding/removing arguments in CommandParametersDialog."""
        CommandParametersMethods.logger.info(self.sender().objectName())
        rem_list = ["rem", "rem1", "rem2", "rem3", "rem4", "rem5", "rem6", "rem7"]
        test_string = self.sender().objectName()
        if test_string == "add8bituint":
            self.append_to_arg_csv("UINT8_T,")
        elif test_string == "add16bituint":
            self.append_to_arg_csv("UINT16_T,")
        elif test_string == "add32bituint":
            self.append_to_arg_csv("UINT32_T,")
        elif test_string == "add16bitint":
            self.append_to_arg_csv("INT16_T,")
        elif test_string == "addfloat":
            self.append_to_arg_csv("FLOAT,")
        elif test_string == "addchar":
            self.append_to_arg_csv("CHAR,")
        elif test_string == "addstartstop":
            self.append_to_arg_csv("STARTSTOP,")
        elif test_string == "addnotype":
            self.append_to_arg_csv("NOTYPE,")
        elif test_string in rem_list:
            self.rem_from_arg_csv()

    ## appends an argument
    def append_to_arg_csv(self, string: str) -> None:
        """Appends an argument to the argument CSV in the arguments pane
        in CommandParametersDialog

        Args:
            string (str): The string to append to the arguements.
        """
        text = self.ui.commandParameters.dlg.argumentsPlainTextCSV
        cursor = QTextCursor()
        text.moveCursor(cursor.End)
        text.insertPlainText(string)
        text.moveCursor(cursor.End)

    ## removes the last argument added (pop)
    def rem_from_arg_csv(self) -> None:
        """Removes the argument at the end of the arguments pane CSV."""
        arg_dict = self.dict_from_csv_args()
        text = self.ui.commandParameters.dlg.argumentsPlainTextCSV
        text.clear()
        arg_text = ""
        arg_list = list(arg_dict.values())
        for index in range(len(arg_list)):
            arg_text = arg_text + arg_list[index] + ","
        text.insertPlainText(arg_text)

    ## simple user input validation
    def validate_command_parameters(self) -> dict:
        """validates input command parameters

        Returns:
            dict: key 0 is bool; True on success.  key 1 is a dict of the input parameters.
        """
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
            + str(self.cliOpt["var"]["primary id key"])
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
        settings_to_validate[
            "commandHasWildcards"
        ] = self.command_parameters_user_input_objects[
            "commandHasWildcards"
        ].isChecked()
        settings_to_validate[
            "commandDepth"
        ] = self.command_parameters_user_input_objects["commandDepth"].text()
        settings_to_validate[
            "commandSubcommands"
        ] = self.command_parameters_user_input_objects["commandSubcommands"].text()
        settings_to_validate[
            "commandArgumentHandling"
        ] = self.command_parameters_user_input_objects[
            "commandArgumentHandling"
        ].currentIndex()
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
        arg_handling_idx = settings_to_validate["commandArgumentHandling"]
        if arg_handling_idx == 0:
            settings_to_validate[
                "commandArguments"
            ] = self.command_parameters_user_input_objects[
                "commandArguments"
            ].toPlainText()
        elif arg_handling_idx == 1:
            tmp = self.list_from_csv_args()
            # single argument
            if not bool(tmp) or tmp[0] == "":
                tmp[0] = ""
                err = True
                error_list.append(
                    "'Arguments' field cannot be blank with current 'Argument Handling' selection"
                )
            if settings_to_validate["returnFunctionName"] == "":
                error_list.append(
                    "'Return function name' cannot be empty with current 'Argument Handling' selection"
                )
            settings_to_validate["commandArguments"] = "{UITYPE::" + str(tmp[0]) + "}"
        elif arg_handling_idx == 2:
            tmp = self.list_from_csv_args()
            # argument array
            if tmp == {} or tmp["0"] == "":
                tmp["0"] = ""
                err = True
                error_list.append(
                    "'Arguments' field cannot be blank with current 'Argument Handling' selection"
                )
            if settings_to_validate["returnFunctionName"] == "":
                error_list.append(
                    "'Return function name' cannot be empty with current 'Argument Handling' selection"
                )
            settings_to_validate["commandArguments"] = tmp
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
            self.get_icon(QStyle.StandardPixmap.SP_MessageBoxCritical),
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
        cmd_dlg.add8bituint.clicked.connect(self.csv_button)
        cmd_dlg.add16bituint.clicked.connect(self.csv_button)
        cmd_dlg.add32bituint.clicked.connect(self.csv_button)
        cmd_dlg.add16bitint.clicked.connect(self.csv_button)
        cmd_dlg.addfloat.clicked.connect(self.csv_button)
        cmd_dlg.addchar.clicked.connect(self.csv_button)
        cmd_dlg.addstartstop.clicked.connect(self.csv_button)
        cmd_dlg.addnotype.clicked.connect(self.csv_button)
        cmd_dlg.rem.clicked.connect(self.csv_button)
        cmd_dlg.rem1.clicked.connect(self.csv_button)
        cmd_dlg.rem2.clicked.connect(self.csv_button)
        cmd_dlg.rem3.clicked.connect(self.csv_button)
        cmd_dlg.rem4.clicked.connect(self.csv_button)
        cmd_dlg.rem5.clicked.connect(self.csv_button)
        cmd_dlg.rem6.clicked.connect(self.csv_button)
        cmd_dlg.rem7.clicked.connect(self.csv_button)
        cmd_dlg.buttonBox.button(QDialogButtonBox.Reset).clicked.connect(
            self.clicked_command_parameters_buttonbox_reset
        )
        cmd_dlg.buttonBox.accepted.connect(self.clicked_command_parameters_buttonbox_ok)
        cmd_dlg.buttonBox.rejected.connect(
            self.clicked_command_parameters_buttonbox_cancel
        )
        cmd_dlg.commandArgumentHandling.currentIndexChanged.connect(
            self.argument_handling_changed
        )
        cmd_dlg.commandString.textChanged.connect(self.command_string_text_changed)

    ## command parameters dialog buttonbox ok
    def clicked_command_parameters_buttonbox_ok(self) -> None:
        """This function is reached when the user clicks `ok` on the CommandParametersDialog"""
        CommandParametersMethods.logger.info("clicked ok on command parameters menu")
        validate_result = self.validate_command_parameters()
        # error
        if validate_result[0] == True:
            CommandParametersMethods.logger.info(
                "one or more errors were detected in the input command parameters"
            )
            return
        validated_result = {}
        validated_result = validate_result[1]
        if self.selected_command != None:  # existing command
            _object_list = self.selected_command.data(1, 0).split(",")
            prm_idx_struct = self.cliOpt["commands"]["index"][_object_list[0]]
            prm_idx = prm_idx_struct["parameters key"]
            self.cliOpt["commands"]["parameters"][prm_idx] = copy.deepcopy(
                validated_result
            )
            #self.rebuild_command_tree()
        else:  # new command being added
            # get array index
            cmd_idx = str(self.cliOpt["var"]["primary id key"])
            # make dict from defined keys
            self.cliOpt["commands"]["parameters"].update({cmd_idx: validated_result})
            p_idx = copy.deepcopy(dataModels.parameters_index_struct)
            # root command
            if self.selected_command_is_root and self.child_command_parent == None:
                p_idx["root index key"] = str(cmd_idx)
                p_idx["parent index key"] = str(cmd_idx)
                p_idx["parameters key"] = str(cmd_idx)
                self.cliOpt["commands"]["index"].update(
                    {p_idx["parameters key"]: p_idx}
                )
                CommandParametersMethods.logger.debug(
                    json.dumps(self.cliOpt["commands"]["parameters"][cmd_idx], indent=2)
                )
                self.add_qtreewidgetitem(
                    self.cliOpt["commands"]["QTreeWidgetItem"]["root"],
                    p_idx["parameters key"],
                )
            # non root command
            else:
                p_idx["parameters key"] = str(cmd_idx)
                                                            
                _pos = self.child_command_parent.data(1, 0).split(",")
                _parent_index_struct = self.cliOpt["commands"]["index"][_pos[0]]
                p_idx["parent index key"] = str(_pos[0])
                p_idx["root index key"] = _parent_index_struct["root index key"]
                self.cliOpt["commands"]["index"].update(
                    {p_idx["parameters key"]: p_idx}
                )                
                _parent_index_struct["child index key list"].append(cmd_idx)                
                CommandParametersMethods.logger.debug(
                    json.dumps(self.cliOpt["commands"]["parameters"][cmd_idx], indent=2)
                )
                self.add_qtreewidgetitem(
                    self.child_command_parent,
                    p_idx["parameters key"],
                )

            # command parameters were accepted, so increment the array index
            self.cliOpt["var"]["primary id key"] = str(
                int(self.cliOpt["var"]["primary id key"]) + 1
            )
            self.cliOpt["var"]["number of commands"] = str(
                int(self.cliOpt["var"]["number of commands"]) + 1
            )

        self.ui.commandParameters.close()

        self.prompt_to_save = True
        self.windowtitle_set = False

        self.update_code("parameters.h", validated_result["functionName"], True)
        self.update_code("functions.h", validated_result["functionName"], True)
        self.update_code("functions.cpp", validated_result["functionName"], True)
        self.update_code("setup.cpp", validated_result["functionName"], True)
        self.update_code("README.md", validated_result["functionName"], True)

    ## command parameters dialog buttonbox reset value
    def clicked_command_parameters_buttonbox_reset(self) -> None:
        """This function is reached if the user clicked `reset` on CommandParametersDialog."""
        CommandParametersMethods.logger.info("reset")
        cmd_dlg = self.ui.commandParameters.dlg
        cmd_dlg.argumentsPlainTextCSV.clear()

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
            self.ui.commandParameters.dlg.argumentsPlainTextCSV.clear()
            self.ui.commandParameters.dlg.argumentsPlainTextCSV.setPlaceholderText(
                "Enter your argument types in order, separated by a comma."
            )
        else:
            cmd_dlg.argumentsPane.setEnabled(False)
            self.ui.commandParameters.dlg.argumentsPlainTextCSV.setPlainText(
                "{UITYPE::NO_ARGS}"
            )

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
                    self.command_parameters_user_input_objects[key].setCurrentIndex(
                        "No arguments"
                    )
                self.command_parameters_user_input_objects[key].setEnabled(True)
        else:
            for key in _fields:
                if key in self.command_parameters_user_input_objects:
                    if isinstance(
                        self.command_parameters_user_input_objects[key], QLineEdit
                    ):
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
                            self.command_parameters_user_input_objects[key].findText(
                                _fields[key]["value"]
                            )
                        )
                    elif isinstance(
                        self.command_parameters_user_input_objects[key], QPlainTextEdit
                    ):
                        self.command_parameters_user_input_objects[key].clear()
                        self.command_parameters_user_input_objects[key].setPlainText(
                            str(_fields[key]["value"])
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
        inp_setup["commandArgumentHandling"]["value"] = "No arguments"
        inp_setup["commandMinArgs"]["value"] = 0
        inp_setup["commandMaxArgs"]["value"] = 0
        inp_setup["commandArguments"]["value"] = "{UITYPE::NO_ARGS}"


# end of file
