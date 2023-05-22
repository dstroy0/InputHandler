##
# @file cli_helper_methods.py
# @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
# @brief cli helper methods
# @version 1.0
# @date 2023-05-22
# @copyright Copyright (c) 2023
# Copyright (C) 2023 Douglas Quigg (dstroy0) <dquigg123@gmail.com>
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 3 as published by the Free Software Foundation.

from __future__ import absolute_import
import datetime
from modules.cli.filestrings import CLIFileStrings


class CLIHelperMethods(object):
    def __init__(self):
        super(CLIHelperMethods, self).__init__()

    ## formats a docstring and returns a list populated with lines of text
    def generate_docstring_list_for_filename(self, filename: str, brief: str) -> list:
        """makes the docstring for generated files

        Args:
            filename (str): the filename
            brief (str): purpose of file

        Returns:
            list: list of docstring lines to prepend to filename
        """
        docstring_list = []
        year = str(datetime.date.today())[0:4]
        ll = CLIFileStrings.lib_license_cpp.format(docs_year=year)
        date = datetime.date.today()
        docstring = CLIFileStrings.docfs.format(
            docs_version=CLIFileStrings.version,
            lib_version=CLIFileStrings.lib_version,
            lib_license=ll,
            docs_filename=filename,
            docs_brief=brief,
            docs_year=year,
            docs_date=date,
        )
        docstring_list = docstring.split("\n")
        return docstring_list

    ## turns a list of text lines into a complete file string where each line ends with newline
    def list_to_code_string(self, list: list) -> str:
        """concatenates strings in a list to each other with a newline at the end

        Args:
            list (list): list of filelines

        Returns:
            str: continuous string generated from list arg
        """
        code_string = ""
        for line in list:
            code_string = code_string + line + "\n"
        return code_string
