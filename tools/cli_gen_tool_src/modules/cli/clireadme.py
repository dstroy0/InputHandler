##
# @file clireadme.py
# @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
# @brief CodePreview/file generation external methods
# @version 1.0
# @date 2022-08-28
# @copyright Copyright (c) 2022
# Copyright (C) 2022 Douglas Quigg (dstroy0) <dquigg123@gmail.com>
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 3 as published by the Free Software Foundation.

from __future__ import absolute_import
from modules.cli.filestrings import cliFileStrings
import datetime
import os


class cliReadme(object):
    ## the constructor
    def __init__(self) -> None:
        super(cliReadme, self).__init__()
        self.cliopt = self.cliOpt
        self.fsdb = self.fsdb

    def readme_md(self, item_string, place_cursor=False):
        object_name = "inputHandler"
        username = os.getlogin()
        buffer_size = self.cliOpt["process output"]["var"]["buffer size"]
        stream_string = self.cliOpt["process output"]["var"]["output stream"]

        self.code_preview_dict["files"]["README.md"]["file_lines_list"] = []
        year = str(datetime.date.today())[0:4]
        date = datetime.date.today()

        return_function_code = ""
        parameters = self.cliopt["commands"]["parameters"]
        for item in parameters:
            if len(parameters[item]["returnFunctionName"]) > 0:
                function_string = self.fsdb["readme"]["md"]["filestring components"][
                    "return function code"
                ].format(
                    functionname=parameters[item]["returnFunctionName"],
                    objectname=object_name,
                )
                return_function_code += function_string
        wrapped_return_function_code = self.fsdb["readme"]["md"][
            "filestring components"
        ]["cpp md tag"].format(statements=return_function_code)
        return_function_inst = ""
        copy_inst = ""
        wrapped_include_inst = ""
        gen_code_sect = ""
        wrapped_loop_code = ""
        wrapped_setup_code = ""
        _loop_code = ""
        _setup_code = ""
        _loop_inst = ""
        _setup_inst = ""

        if stream_string != "" and stream_string != None and int(buffer_size) != 0:
            _setup_code = "InputHandler_setup();"
            _loop_code = "InputHandler_loop();"
        elif stream_string == "" or stream_string == None and int(buffer_size) != 0:
            _setup_code = "InputHandler_setup();"
            _loop_code = "InputHandler_loop();"

        if len(return_function_code) > 0:
            return_function_inst = cliFileStrings.rdme_function_inst
            copy_inst = cliFileStrings.rdme_copy_inst
            gen_code_sect = cliFileStrings.rdme_gen_inst
            include_inst = cliFileStrings.rdme_include_inst
            wrapped_include_inst = self.fsdb["readme"]["md"]["filestring components"][
                "cpp md tag"
            ].format(statements=include_inst)
            _setup_code = "InputHandler_setup();"
            _loop_code = "InputHandler_loop();"

        if len(_setup_code) > 0:
            wrapped_setup_code = self.fsdb["readme"]["md"]["filestring components"][
                "cpp md tag"
            ].format(statements=_setup_code)
            _setup_inst = cliFileStrings.rdme_setup_inst

        if len(_loop_code) > 0:
            wrapped_loop_code = self.fsdb["readme"]["md"]["filestring components"][
                "cpp md tag"
            ].format(statements=_loop_code)
            _loop_inst = cliFileStrings.rdme_loop_inst

        if len(username) > 0:
            username = username + " (retrieved using os.getlogin())"

        docstring = cliFileStrings.readmemd.format(
            user=username,
            docs_version=cliFileStrings.version,
            docs_date=date,
            docs_year=year,
            generated_code_section=gen_code_sect,
            include_instructions=wrapped_include_inst,
            function_instructions=return_function_inst,
            copy_instructions=copy_inst,
            functions_with_return=wrapped_return_function_code,
            setup_instructions=_setup_inst,
            setup_code=wrapped_setup_code,
            loop_instructions=_loop_inst,
            loop_code=wrapped_loop_code,
        )
        self.code_preview_dict["files"]["README.md"][
            "file_lines_list"
        ] = docstring.split("\n")
        self.code_preview_dict["files"]["README.md"]["file_string"] = docstring
        self.set_code_string("README.md", docstring, item_string, place_cursor)
