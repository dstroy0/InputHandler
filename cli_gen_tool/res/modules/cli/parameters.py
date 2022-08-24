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

from __future__ import absolute_import


class cliParameters(object):
    ## the constructor
    def __init__(self) -> None:
        super(cliParameters, self).__init__()

    def ret_unnested_param(self, parameters):
        parameters_string = self.fsdb["parameters"]["h"]["filestring components"][
            "parameters"
        ]
        command_constructor_string = self.fsdb["parameters"]["h"][
            "filestring components"
        ]["command constructor"]
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
            commandconstructor=command_constructor_string.format(
                functionname=parameters["functionName"]
            ),
        )
        return ret

    def parameters_h(self, item_string, place_cursor=False):
        object_name = "inputHandler"
        self.code_preview_dict["files"]["parameters.h"]["file_lines_list"] = []
        docstring = self.generate_docstring_list_for_filename(
            "parameters.h", "InputHandler autogenerated parameters.h"
        )

        code_string = self.list_to_code_string(docstring)

        parameters_h_fs = self.fsdb["parameters"]["h"]["filestring"]

        nested_child_string = self.fsdb["parameters"]["h"]["filestring components"][
            "nested child"
        ]
        command_constructor_string = self.fsdb["parameters"]["h"][
            "filestring components"
        ]["command constructor"]
        parameters_string = self.fsdb["parameters"]["h"]["filestring components"][
            "parameters"
        ]
        nested_parameters_string = self.fsdb["parameters"]["h"][
            "filestring components"
        ]["nested parameters"]

        parameters_code_string = ""

        if self.cliOpt["builtin methods"]["var"]["listCommands"] == True:
            parameters_code_string += self.ret_unnested_param(
                self.cliOpt["commands"]["parameters"]["listCommands"]
            )

        if self.cliOpt["builtin methods"]["var"]["listSettings"] == True:
            parameters_code_string += self.ret_unnested_param(
                self.cliOpt["commands"]["parameters"]["listSettings"]
            )

        code_string = code_string + parameters_h_fs.format(
            parameters=parameters_code_string
        )
        self.code_preview_dict["files"]["parameters.h"][
            "file_lines_list"
        ] = code_string.split("\n")
        self.set_code_string("parameters.h", code_string, item_string, place_cursor)


# end of file
