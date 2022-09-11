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

    def ret_nested_child(self, parameters, comma=True):
        _comma = ","
        if comma == False:
            _comma = ""
        ret = self.fsdb["parameters"]["h"]["filestring components"][
            "nested_child"
        ].format(
            functionname=parameters["functionName"],
            comma=_comma,
        )
        return ret

    def ret_unnested_param(self, parameters, has_constructor=True):
        parameters_string = self.fsdb["parameters"]["h"]["filestring components"][
            "parameters"
        ]
        command_constructor_string = "\n"
        if has_constructor == True:
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
        )
        return ret

    def ret_nested_param(self, num_children, nested_children_string, parameters):
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
            commandconstructor=command_constructor_string,
            children=nested_children_string,
            numberofchildren=num_children,
        )
        return ret

    def parameters_h(self, item_string, place_cursor=False):
        self.code_preview_dict["files"]["parameters.h"]["file_lines_list"] = []
        docstring = self.generate_docstring_list_for_filename(
            "parameters.h", "InputHandler autogenerated parameters.h"
        )

        code_string = self.list_to_code_string(docstring)

        parameters_h_fs = self.fsdb["parameters"]["h"]["filestring"]

        parameters_code_string = ""

        for index in self.cliOpt["commands"]["index"]:
            key = self.cliOpt["commands"]["index"][index]["parameters index"]
            # unnested parameters
            if (
                key in self.cliOpt["commands"]["parameters"]
                and bool(self.cliOpt["commands"]["index"][index]["indices of children"])
                == False
            ):
                parameters_code_string += self.ret_unnested_param(
                    self.cliOpt["commands"]["parameters"][key], True
                )
            elif (
                key in self.cliOpt["commands"]["parameters"]
                and bool(self.cliOpt["commands"]["index"][index]["indices of children"])
                == True
            ):
                # nested parameters
                for item in self.cliOpt["commands"]["index"][index][
                    "indices of children"
                ]:
                    parameters_code_string += self.ret_unnested_param(
                        self.cliOpt["commands"]["parameters"][item["parameters index"]],
                        False,
                    )
                num_children = len(
                    self.cliOpt["commands"]["index"][index]["indices of children"]
                )
                nested_children_string = ""
                for i in range(num_children):
                    if i < num_children:
                        nested_children_string += self.ret_nested_child(
                            self.self.cliOpt["commands"]["parameters"][
                                item["parameters index"]
                            ],
                            True,
                        )
                    else:
                        nested_children_string += self.ret_nested_child(
                            self.self.cliOpt["commands"]["parameters"][
                                item["parameters index"]
                            ],
                            False,
                        )
                parameters_code_string += self.ret_nested_param(
                    num_children,
                    nested_children_string,
                    self.cliOpt["commands"]["parameters"][
                        self.cliOpt["commands"]["index"][index]["parameters index"]
                    ],
                )

        code_string = code_string + parameters_h_fs.format(
            parameters=parameters_code_string
        )
        self.code_preview_dict["files"]["parameters.h"][
            "file_lines_list"
        ] = code_string.split("\n")
        self.set_code_string("parameters.h", code_string, item_string, place_cursor)


# end of file
