##
# @file functions_h.py
# @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
# @brief functions.h generator
# @version 1.0
# @date 2023-05-22
# @copyright Copyright (c) 2023
# Copyright (C) 2023 Douglas Quigg (dstroy0) <dquigg123@gmail.com>
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 3 as published by the Free Software Foundation.


class Functions_H(object):
    """functions.h generator

    Args:
        object (object): base object specialization
    """

    ## the constructor
    def __init__(self) -> None:
        """the constructor"""
        super(Functions_H, self).__init__()

    ## update the text for functions.h
    def functions_h(self) -> str:
        """generates the file functions.h

        Args:
            item_string (str): code to highlight
            place_cursor (bool, optional): Place cursor on highlighted code if True. Defaults to False.
        """
        object_name = "inputHandler"

        functions_h_fs = self.fsdb["functions"]["h"]["filestring"]
        functions_h_return_prototype_string = self.fsdb["functions"]["h"][
            "filestring components"
        ]["return function prototype"]
        stream_string = self.cli_options["process output"]["var"]["output stream"]
        func_string = self.fsdb["functions"]["h"]["filestring components"]["function"]
        functions_h_builtin_function_list = []
        functions_h_function_list = []
        functions_h_return_prototype_list = []

        # functions with parameters
        for key in self.cli_options["commands"]["parameters"]:
            parameters = self.cli_options["commands"]["parameters"][key]
            if bool(parameters["returnFunctionName"]):
                functions_h_return_prototype_list.append(
                    functions_h_return_prototype_string.format(
                        functionname=parameters["returnFunctionName"],
                        objectname=object_name,
                    )
                )

        # default function
        if self.cli_options["builtin methods"]["var"]["defaultFunction"] == True:
            statement = self.fsdb["functions"]["h"]["filestring components"][
                "outputToStream"
            ]["call"].format(objectname=object_name, stream=stream_string)
            functions_h_builtin_function_list.append(
                func_string.format(
                    functionname="unrecognized",
                    objectname=object_name,
                    statements=statement,
                )
            )

        # functions with parameters
        for key in self.cli_options["commands"]["parameters"]:
            parameters = self.cli_options["commands"]["parameters"][key]
            if (
                parameters["functionName"]
                in self.fsdb["functions"]["h"]["filestring components"]
            ):
                statement = self.fsdb["functions"]["h"]["filestring components"][
                    parameters["functionName"]
                ]["call"].format(objectname=object_name, stream=stream_string)
                functions_h_builtin_function_list.append(
                    func_string.format(
                        functionname=parameters["functionName"],
                        objectname=object_name,
                        statements=statement,
                    )
                )
            else:
                # if statement string is blank it's a vestigial function by accident or design
                statement = ""
                functionname = parameters["returnFunctionName"]
                if bool(functionname):
                    statement = f"{functionname}(_{object_name});"
                functions_h_function_list.append(
                    func_string.format(
                        functionname=parameters["functionName"],
                        objectname=object_name,
                        statements=statement,
                    )
                )

        statements = "\n\n/* InputHandler user return function prototypes */\n"
        for item in functions_h_return_prototype_list:
            statements += item

        statements += "\n\n/* InputHandler builtin functions */\n\n"
        for item in functions_h_builtin_function_list:
            statements += item

        statements += "\n/* InputHandler user defined functions */\n\n"
        for item in functions_h_function_list:
            statements += item

        docstring = self.generate_docstring_list_for_filename(
            "functions.h", "InputHandler autogenerated functions.h"
        )
        code_string = self.list_to_code_string(docstring)
        f_h_fs = functions_h_fs.format(functionprototypes=statements)
        code_string = f"{code_string}{f_h_fs}"

        return code_string


# end of file
