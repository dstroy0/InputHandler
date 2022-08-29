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
from res.modules.cli.filestrings import CLIfilestrings
import datetime
class cliReadme(object):
    ## the constructor
    def __init__(self) -> None:
        super(cliReadme, self).__init__()
        
    def readme_md(self, item_string, place_cursor=False):
        object_name = "inputHandler"
        self.code_preview_dict["files"]["README.md"]["file_lines_list"] = []
        year = str(datetime.date.today())[0:4]
        date = datetime.date.today()
        docstring = CLIfilestrings.readmemd.format(
            docs_version=CLIfilestrings.version,
            docs_date=date,
            docs_year=year,
            initial_instructions=CLIfilestrings.rdme_initial_inst,
            function_instructions=CLIfilestrings.rdme_function_inst,
            functions_with_return="",
            setup_instructions=CLIfilestrings.rdme_setup_inst,
            setup_code="",
            loop_instructions=CLIfilestrings.rdme_loop_inst,
            loop_code=""
        )
        self.code_preview_dict["files"]["README.md"]["file_lines_list"] = docstring.split("\n")
        self.set_code_string("README.md", docstring, item_string, place_cursor)
        