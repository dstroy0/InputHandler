##
# @file functions.py
# @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
# @brief CodePreview/file generation external methods
# @version 1.0
# @date 2022-07-29
# @copyright Copyright (c) 2022
# Copyright (C) 2022 Douglas Quigg (dstroy0) <dquigg123@gmail.com>
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 3 as published by the Free Software Foundation.


class cliFunctions(object):
    ## the constructor
    def __init__(self) -> None:
        super(cliFunctions, self).__init__()

    ## update the text for functions.h
    def functions_h(self, item_string, place_cursor=False):
        object_name = "inputHandler"
        self.code_preview_dict["files"]["functions.h"]["file_lines_list"] = []
        docstring = self.generate_docstring_list_for_filename(
            "functions.h", "InputHandler autogenerated functions.h"
        )
        code_string = self.list_to_code_string(docstring)
        functions_h_fs = self.fsdb["functions"]["h"]["filestring"]
        functions_h_prototype_string = self.fsdb["functions"]["h"][
            "filestring components"
        ]["function prototype"]
        functions_h_prototype_list = []

        # default function
        if self.cliOpt["builtin methods"]["var"]["defaultFunction"] == True:
            functions_h_prototype_list.append(
                functions_h_prototype_string.format(
                    functionname="unrecognized", objectname=object_name
                )
            )

        # functions with parameters
        for key in self.cliOpt["commands"]["parameters"]:
            parameters = self.cliOpt["commands"]["parameters"][key]
            functions_h_prototype_list.append(
                functions_h_prototype_string.format(
                    functionname=parameters["functionName"], objectname=object_name
                )
            )

        statements = ""
        for item in functions_h_prototype_list:
            statements += item
        f_h_fs = functions_h_fs.format(functionprototypes=statements)
        code_string = code_string + f_h_fs
        self.code_preview_dict["files"]["functions.h"][
            "file_lines_list"
        ] = code_string.split("\n")
        self.set_code_string("functions.h", code_string, item_string, place_cursor)

    ## update the text for functions.cpp
    def functions_cpp(self, item_string, place_cursor=False):
        object_name = "inputHandler"

        stream_string = self.cliOpt["process output"]["var"]["output stream"]

        self.code_preview_dict["files"]["functions.cpp"]["file_lines_list"] = []
        docstring = self.generate_docstring_list_for_filename(
            "functions.cpp", "InputHandler autogenerated functions.cpp"
        )
        code_string = self.list_to_code_string(docstring)
        cpp_fs = self.fsdb["functions"]["cpp"]["filestring"]
        func_string = self.fsdb["functions"]["cpp"]["filestring components"]["function"]
        func_list = []

        # default function
        if self.cliOpt["builtin methods"]["var"]["defaultFunction"] == True:
            statement = self.fsdb["functions"]["cpp"]["filestring components"][
                "outputToStream"
            ]["call"].format(objectname=object_name, stream=stream_string)
            func_list.append(
                func_string.format(
                    functionname="unrecognized",
                    objectname=object_name,
                    statements=statement,
                )
            )

        # functions with parameters
        for key in self.cliOpt["commands"]["parameters"]:
            parameters = self.cliOpt["commands"]["parameters"][key]
            if (
                parameters["functionName"]
                in self.fsdb["functions"]["cpp"]["filestring components"]
            ):
                statement = self.fsdb["functions"]["cpp"]["filestring components"][
                    parameters["functionName"]
                ]["call"].format(objectname=object_name, stream=stream_string)
                func_list.append(
                    func_string.format(
                        functionname=parameters["functionName"],
                        objectname=object_name,
                        statements=statement,
                    )
                )

        # concatenate individual function strings into one string
        funcs_string = ""
        for item in func_list:
            funcs_string += item

        code_string = code_string + cpp_fs.format(functions=funcs_string)

        self.code_preview_dict["files"]["functions.cpp"][
            "file_lines_list"
        ] = code_string.split("\n")
        self.set_code_string("functions.cpp", code_string, item_string, place_cursor)


# end of file
