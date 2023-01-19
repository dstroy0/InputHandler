##
# @file parameters.py
# @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
# @brief CodePreview/file generation external methods
# @version 1.0
# @date 2022-07-29
# @copyright Copyright (c) 2022
# Copyright (C) 2022 Douglas Quigg (dstroy0) <dquigg123@gmail.com>
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 3 as published by the Free Software Foundation.

import copy


class cliParameters(object):
    """parameters.h generator

    Args:
        object (object): base object specialization
    """

    ## the constructor
    def __init__(self) -> None:
        """the constructor"""
        super(cliParameters, self).__init__()
        self.cliopt = self.cliOpt
        self.command_index = self.cliopt["commands"]["index"]
        self.nested_children_string = ""
        self.nested_child_parameters_string = ""
        self.num_nested_children = 0
        self.child_parameters_list = []
        self.max_depth = 0

    def parse_commandarguments_string(self, args: str) -> list:
        args_list = copy.deepcopy(args)
        args_list = args_list.replace("UITYPE::", "")
        args_list = args_list.replace("{", "")
        args_list = args_list.replace("}", "")
        args_list = args_list.replace(" ", "")
        args_list = args_list.replace("\n", "")
        args_list = args_list.split(",")
        return args_list

    def generate_commandarguments_string(self, args_list: list) -> str:
        comma = ""
        newline = ""
        padding = ""
        arr_indent = ""
        arguments = ""
        if len(args_list) > 1:
            padding = "    "
            arr_indent = "  "
        for i in range(len(args_list)):
            arg_type = args_list[i]
            if i < len(args_list) - 1:
                comma = ","
                newline = "\n"
            else:
                comma = ""
                newline = ""
            arg_format = f"{padding}{arr_indent}UITYPE::{arg_type}{comma}{newline}"
            arguments += arg_format
        if len(args_list) > 1:
            newline = "\n"
        argstring = f"{{{newline}{arguments}{newline}{padding}}}"
        return argstring

    def ret_nested_child(self, parameters: dict, comma: bool = True) -> str:
        """returns string that is a valid C++11 pointer.

        Args:
            parameters (dict): command parameters
            comma (bool, optional): place comma after pointer because there are more pointers if True. Defaults to True.

        Returns:
            str: a string that is a valid C++11 pointer
        """
        _comma = ","
        _newline = "\n"
        if comma == False:
            _comma = " "
            _newline = ""
        ret = self.fsdb["parameters"]["h"]["filestring components"][
            "nested child"
        ].format(
            functionname=parameters["functionName"], comma=_comma, newline=_newline
        )
        return ret

    def ret_unnested_param(self, parameters: dict, has_constructor: bool = True) -> str:
        """returns an unnested CommandParameters string

        Args:
            parameters (dict): the command parameters
            has_constructor (bool, optional): There will be a constructor string after
            the CommandParameters struct if True. Defaults to True.

        Returns:
            str: CommandParameters string
        """
        parameters_string = self.fsdb["parameters"]["h"]["filestring components"][
            "parameters"
        ]
        command_constructor_string = ""
        _newline = ""
        argstring = self.generate_commandarguments_string(
            self.parse_commandarguments_string(parameters["commandArguments"])
        )
        if has_constructor == True:
            command_constructor_string = self.fsdb["parameters"]["h"][
                "filestring components"
            ]["command constructor"].format(functionname=parameters["functionName"])
            _newline = "\n"
        ret = parameters_string.format(
            functionname=parameters["functionName"],
            wildcardflag=parameters["commandHasWildcards"],
            commandstring=parameters["commandString"],
            lencommandstring=parameters["commandLength"],
            parentid=parameters["parentId"],
            commandid=parameters["commandId"],
            commanddepth=parameters["commandDepth"],
            commandsubcommands=parameters["commandSubcommands"],
            argumenthandling=parameters["commandArgumentHandling"],
            minnumargs=parameters["commandMinArgs"],
            maxnumargs=parameters["commandMaxArgs"],
            argtypearray=argstring,
            commandconstructor=command_constructor_string,
            newline=_newline,
        )
        return ret

    def ret_nested_param(
        self,
        num_children: int,
        nested_children_string: str,
        parameters: dict,
        max_depth: int,
    ) -> str:
        """generates the root command and all of its nested children CommandParameters

        Args:
            num_children (int): number of child CommandParameters
            nested_children_string (str): the CommandParameters with no constructors
            parameters (dict): root command CommandParameters
            max_depth (int): max command tree depth

        Returns:
            str: the complete set of CommandParameters for the command in a string
        """
        parameters_string = self.fsdb["parameters"]["h"]["filestring components"][
            "nested parameters"
        ]
        nested_command_constructor_string = self.fsdb["parameters"]["h"][
            "filestring components"
        ]["nested command constructor"].format(
            functionname=parameters["functionName"], maxdepth=max_depth
        )
        argstring = self.generate_commandarguments_string(
            self.parse_commandarguments_string(parameters["commandArguments"])
        )
        ret = parameters_string.format(
            functionname=parameters["functionName"],
            wildcardflag=parameters["commandHasWildcards"],
            commandstring=parameters["commandString"],
            lencommandstring=parameters["commandLength"],
            parentid=parameters["parentId"],
            commandid=parameters["commandId"],
            commanddepth=parameters["commandDepth"],
            commandsubcommands=parameters["commandSubcommands"],
            argumenthandling=parameters["commandArgumentHandling"],
            minnumargs=parameters["commandMinArgs"],
            maxnumargs=parameters["commandMaxArgs"],
            argtypearray=argstring,
            commandconstructor=nested_command_constructor_string,
            children=nested_children_string,
            numberofchildren=num_children,
        )
        return ret

    def get_command_parameters_string(
        self, parent_command_parameters: dict, index: str
    ) -> None:
        """recursive CommandParameters search

        Args:
            parent_command_parameters (dict): CommandParameters
            index (str): command index
        """
        if bool(self.command_index[index]["child index key list"]):
            for child_index in self.command_index[index]["child index key list"]:
                child_parameters = self.cliopt["commands"]["parameters"][
                    self.command_index[child_index]["parameters key"]
                ]
                self.child_parameters_list.append(child_parameters)
                if self.max_depth == "":
                    self.max_depth = 0
                if int(child_parameters["commandDepth"]) > int(self.max_depth):
                    self.max_depth = child_parameters["commandDepth"]
                self.num_nested_children += 1
                if bool(self.command_index[child_index]["child index key list"]):
                    self.get_command_parameters_string(child_parameters, child_index)

    def parameters_h(self, item_string: str, place_cursor: bool = False) -> None:
        """generates the parameters.h file for InputHandlers autogenerated CLI

        Args:
            item_string (str): the code to highlight
            place_cursor (bool, optional): Moves the cursor to highlighted code if True. Defaults to False.
        """
        parameters_code_string = ""
        for root_command_index in self.command_index:
            # only populates root commands with their children, because
            # self.command_index is flat, not a matrix
            if int(self.command_index[root_command_index]["root index key"]) == int(
                self.command_index[root_command_index]["parameters key"]
            ):
                root_command_parameters = self.cliopt["commands"]["parameters"][
                    self.command_index[root_command_index]["parameters key"]
                ]
                self.get_command_parameters_string(
                    root_command_parameters, root_command_index
                )
                if self.num_nested_children == 0:
                    parameters_code_string += self.ret_unnested_param(
                        root_command_parameters
                    )
                else:
                    for index in range(len(self.child_parameters_list)):
                        if index < len(self.child_parameters_list) - 1:
                            self.nested_children_string += self.ret_nested_child(
                                self.child_parameters_list[index]
                            )
                            self.nested_child_parameters_string += (
                                self.ret_unnested_param(
                                    self.child_parameters_list[index], False
                                )
                            )
                        else:
                            self.nested_children_string += self.ret_nested_child(
                                self.child_parameters_list[index], False
                            )
                            self.nested_child_parameters_string += (
                                self.ret_unnested_param(
                                    self.child_parameters_list[index], False
                                )
                            )

                    parameters_code_string += self.nested_child_parameters_string
                    parameters_code_string += self.ret_nested_param(
                        self.num_nested_children,
                        self.nested_children_string,
                        root_command_parameters,
                        self.max_depth,
                    )

                    self.nested_children_string = ""
                    self.nested_child_parameters_string = ""
                    self.max_depth = ""
                    self.num_nested_children = 0
                    self.child_parameters_list = []

        self.code_preview_dict["files"]["parameters.h"]["file_lines_list"] = []
        docstring = self.generate_docstring_list_for_filename(
            "parameters.h", "InputHandler autogenerated parameters.h"
        )
        code_string = ""
        code_string = self.list_to_code_string(docstring)
        parameters_h_fs = self.fsdb["parameters"]["h"]["filestring"]
        code_string = code_string + parameters_h_fs.format(
            parameters=parameters_code_string
        )
        self.code_preview_dict["files"]["parameters.h"][
            "file_lines_list"
        ] = code_string.split("\n")
        self.code_preview_dict["files"]["parameters.h"]["file_string"] = code_string
        self.set_code_string("parameters.h", code_string, item_string, place_cursor)


# end of file
