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

# pyside imports
from PySide6.QtCore import QRegularExpression, Qt
from PySide6.QtGui import QRegularExpressionValidator, QTextCursor
from PySide6.QtWidgets import QDialogButtonBox, QStyle

# logging api
from res.modules.logging_setup import Logger
# data models
from res.modules.data_models import dataModels


# command parameters methods
class CommandParametersMethods(object):
    ## Command parameters dicts are constructed using keys from this list.
    command_parameters_dict_keys_list = dataModels.command_parameters_dict_keys_list

    ## Acceptable command argument types.
    command_arg_types_list = dataModels.command_arg_types_list

    ## the constructor
    def __init__(self) -> None:
        super(CommandParametersMethods, self).__init__()
        CommandParametersMethods.logger = Logger.get_child_logger(self.logger, __name__)

    ## spawns a regexp validator
    def regex_validator(self, input):
        exp = QRegularExpression(input)
        return QRegularExpressionValidator(exp)
    
    ## generates a dict from csv arguments in the command parameters dialog
    def dict_from_csv_args(self):
        args_dict = {}
        args_list = []
        arg_num_list = []
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
                    arg_num_list.append(i)
                    i = i + 1
                    args_list.append(match.captured().upper().strip(","))
            else:
                break
        args_dict = dict(zip(arg_num_list, args_list[:-1]))
        return args_dict

    ## all buttons related to adding/removing arguments from the command parameters dialog
    def csv_button(self):
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
    def append_to_arg_csv(self, string):
        text = self.ui.commandParameters.dlg.argumentsPlainTextCSV
        cursor = QTextCursor()
        text.moveCursor(cursor.End)
        text.insertPlainText(string)
        text.moveCursor(cursor.End)

    ## removes the last argument added (pop)
    def rem_from_arg_csv(self):
        arg_dict = self.dict_from_csv_args()
        text = self.ui.commandParameters.dlg.argumentsPlainTextCSV
        text.clear()
        arg_text = ""
        arg_list = list(arg_dict.values())
        for index in range(len(arg_list)):
            arg_text = arg_text + arg_list[index] + ","
        text.insertPlainText(arg_text)

    ## simple user input validation
    def validate_command_parameters(self):
        error_list = []
        cmd_dlg = self.ui.commandParameters.dlg
        settings_to_validate = dict.fromkeys(
            CommandParametersMethods.command_parameters_dict_keys_list, None
        )
        settings_to_validate["functionName"] = cmd_dlg.functionName.text()
        settings_to_validate["commandString"] = cmd_dlg.commandString.text()
        settings_to_validate["commandLength"] = len(
            settings_to_validate["commandString"]
        )
        settings_to_validate["parentId"] = cmd_dlg.commandParentId.text()
        settings_to_validate["commandId"] = cmd_dlg.commandId.text()
        settings_to_validate[
            "commandHasWildcards"
        ] = cmd_dlg.commandHasWildcards.isChecked()
        settings_to_validate["commandDepth"] = cmd_dlg.commandDepth.text()
        settings_to_validate["commandSubcommands"] = cmd_dlg.commandSubcommands.text()
        settings_to_validate[
            "commandArgumentHandling"
        ] = cmd_dlg.commandArgumentHandling.currentIndex()
        settings_to_validate["commandMinArgs"] = cmd_dlg.commandMinArgs.text()
        settings_to_validate["commandMaxArgs"] = cmd_dlg.commandMaxArgs.text()
        # err is the error sentinel
        err = False
        if settings_to_validate["functionName"] == "":
            error_list.append("'Function name' cannot be empty")
            err = True
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
        arg_handling_idx = int(settings_to_validate["commandArgumentHandling"])
        if arg_handling_idx == 0:
            settings_to_validate["commandArguments"] = {0: "NO_ARGS"}
        elif arg_handling_idx == 1:
            # single argument
            tmp = self.dict_from_csv_args()
            if tmp[0] == "":
                err = True
                error_list.append(
                    "'Arguments' field cannot be blank with current 'Argument Handling' selection"
                )
            settings_to_validate["commandArguments"] = {0: tmp[0]}
        elif arg_handling_idx == 2:
            # argument array
            tmp = self.dict_from_csv_args()
            if tmp[0] == "":
                err = True
                error_list.append(
                    "'Arguments' field cannot be blank with current 'Argument Handling' selection"
                )
            settings_to_validate["commandArguments"] = tmp
        CommandParametersMethods.logger.debug(settings_to_validate)
        CommandParametersMethods.logger.debug(error_list)
        if err == True:
            self.err_settings_to_validate(error_list)
        return {0: err, 1: settings_to_validate}

    ## create error dialog where `error_list` contains error text
    def err_settings_to_validate(self, error_list):
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
    def set_command_parameter_validators(self):
        cmd_dlg = self.ui.commandParameters.dlg
        # allowed function name char
        cmd_dlg.functionName.setValidator(
            self.regex_validator(cmd_dlg.validatorDict["functionName"])
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
    def set_command_parameters_triggers(self):
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
    def clicked_command_parameters_buttonbox_ok(self):
        CommandParametersMethods.logger.info("ok")
        validate_result = self.validate_command_parameters()
        # error
        if validate_result[0] == True:
            return
        validated_result = {}
        validated_result = validate_result[1]
        # get array index
        cmd_idx = self.cliOpt["var"]["num_commands"]
        # make dict from defined keys
        self.cliOpt["commands"][cmd_idx] = validated_result
        CommandParametersMethods.logger.info(self.cliOpt["commands"][cmd_idx])

        # command parameters were accepted, so increment the array index
        self.cliOpt["var"]["num_commands"] += 1
        CommandParametersMethods.logger.info(self.cliOpt["var"])
        self.ui.commandParameters.close()

    ## command parameters dialog buttonbox reset value
    def clicked_command_parameters_buttonbox_reset(self):
        CommandParametersMethods.logger.info("reset")
        cmd_dlg = self.ui.commandParameters.dlg
        cmd_dlg.argumentsPlainTextCSV.clear()

    ## command parameters dialog buttonbox cancel changes
    def clicked_command_parameters_buttonbox_cancel(self):
        CommandParametersMethods.logger.info("cancel")
        self.ui.commandParameters.close()

    ## refreshes `commandLength`
    def command_string_text_changed(self):
        cmd_dlg = self.ui.commandParameters.dlg
        cmd_dlg.commandLengthLabel.setText(str(len(cmd_dlg.commandString.text())))

    ## command parameters dialog argument handling combobox index changed
    def argument_handling_changed(self):
        CommandParametersMethods.logger.info("argument handling changed")
        cmd_dlg = self.ui.commandParameters.dlg
        if cmd_dlg.commandArgumentHandling.currentIndex() != 0:
            cmd_dlg.argumentsPane.setEnabled(True)
        else:
            cmd_dlg.argumentsPane.setEnabled(False)


# end of file
