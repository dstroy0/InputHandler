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


class cliParameters(object):
    ## the constructor
    def __init__(self) -> None:
        super(cliParameters, self).__init__()
        self.cliopt = self.cliOpt
        self.command_index = self.cliopt["commands"]["index"]
        self.nested_child_parameters = ""
        self.nested_children_string = ""
        self.num_nested_children = 0
        self.child_parameters_list = []

    def ret_nested_child(self, parameters, comma=True):
        _comma = ","
        _newline = "\n"
        if comma == False:
            _comma = ""
            _newline = ""
        ret = self.fsdb["parameters"]["h"]["filestring components"][
            "nested child"
        ].format(
            functionname=parameters["functionName"], comma=_comma, newline=_newline
        )
        return ret

    def ret_unnested_param(self, parameters, has_constructor=True):
        parameters_string = self.fsdb["parameters"]["h"]["filestring components"][
            "parameters"
        ]
        command_constructor_string = ""
        _newline = ""
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
            argtypearray=parameters["commandArguments"],
            commandconstructor=command_constructor_string,
            newline=_newline,
        )
        return ret

    def ret_nested_param(self, num_children, nested_children_string, parameters):
        parameters_string = self.fsdb["parameters"]["h"]["filestring components"][
            "nested parameters"
        ]
        command_constructor_string = self.fsdb["parameters"]["h"][
            "filestring components"
        ]["command constructor"].format(functionname=parameters["functionName"])

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
            argtypearray=parameters["commandArguments"],
            commandconstructor=command_constructor_string,
            children=nested_children_string,
            numberofchildren=num_children,
        )
        return ret

    def get_command_parameters_string(self, parent_command_parameters, index):
        if bool(self.command_index[index]["child index key list"]):
            for child_index in self.command_index[index]["child index key list"]:
                child_parameters = self.cliopt["commands"]["parameters"][
                    self.command_index[child_index]["parameters key"]
                ]
                self.nested_child_parameters += self.ret_unnested_param(
                    child_parameters, False
                )
                self.child_parameters_list.append(child_parameters)
                self.num_nested_children += 1

                if bool(self.command_index[child_index]["child index key list"]):
                    self.get_command_parameters_string(child_parameters, child_index)

        ret_string = ""
        if self.num_nested_children == 0:
            ret_string = self.ret_unnested_param(parent_command_parameters)
        else:
            ret_string += self.nested_child_parameters
            for index in range(len(self.child_parameters_list)):
                if index < len(self.child_parameters_list) - 1:
                    self.nested_children_string += self.ret_nested_child(
                        self.child_parameters_list[index]
                    )
                else:
                    self.nested_children_string += self.ret_nested_child(
                        child_parameters, False
                    )
            ret_string += self.ret_nested_param(
                self.num_nested_children,
                self.nested_children_string,
                parent_command_parameters,
            )
            self.nested_child_parameters = ""
            self.nested_children_string = ""
            self.num_nested_children = 0
            self.child_parameters_list = []
        return ret_string

    def parameters_h(self, item_string, place_cursor=False):
        self.code_preview_dict["files"]["parameters.h"]["file_lines_list"] = []
        docstring = self.generate_docstring_list_for_filename(
            "parameters.h", "InputHandler autogenerated parameters.h"
        )

        code_string = ""
        code_string = self.list_to_code_string(docstring)

        parameters_h_fs = self.fsdb["parameters"]["h"]["filestring"]

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
                parameters_code_string += self.get_command_parameters_string(
                    root_command_parameters, root_command_index
                )

        code_string = code_string + parameters_h_fs.format(
            parameters=parameters_code_string
        )
        self.code_preview_dict["files"]["parameters.h"][
            "file_lines_list"
        ] = code_string.split("\n")
        self.code_preview_dict["files"]["parameters.h"]["file_string"] = code_string
        self.set_code_string("parameters.h", code_string, item_string, place_cursor)


# end of file
