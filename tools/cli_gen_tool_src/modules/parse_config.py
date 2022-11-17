##
# @file parse_config.py
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

# imports
import copy
import json

# pyside imports
from PySide6.QtCore import QRegularExpression

# parse inputhandler config
class ParseInputHandlerConfig(object):
    ## the constructor
    def __init__(self) -> None:
        super(ParseInputHandlerConfig, self).__init__()
        ParseInputHandlerConfig.logger = self.get_child_logger(__name__)

    ## parses input config files for use
    def parse_config_header_file(self, path):
        ParseInputHandlerConfig.logger.debug("Attempt parse config.h")
        config_path = ""
        if path == "":
            config_path = self.default_lib_config_path
        else:
            config_path = path
        file_line_list = []
        config_file = open(config_path, "r")
        file_line_list = config_file.readlines()
        config_file.close()
        remove_number_of_lines = 16
        if "autogenerated" in file_line_list[0]:
            remove_number_of_lines = 17
        del file_line_list[0:remove_number_of_lines]
        for line in range(len(file_line_list)):
            file_line_list[line] = file_line_list[line].rstrip()
        self.cliOpt["config"]["file lines"] = self.generate_docstring_list_for_filename(
            "config.h", "InputHandler autogenerated config.h"
        )
        self.cliOpt["config"]["file lines"] = (
            self.cliOpt["config"]["file lines"] + file_line_list
        )

        debug_regexp = "(\s*[\/][\/]\s*)(\s*#define\s*)(DEBUG_\S*)"
        opt_method_regexp = "(\s*[\/]*\s*)(\s*#define\s*)(DISABLE_\S*)"
        setting_regexp = "(\s*[\/]*\s*)(\s*#define\s*)(?!\S*PGM_LEN)(UI_\S*\s*)(\d*)"
        progmem_regexp = "(\s*[\/]*\s*)(\s*#define\s*)(UI_\S*PGM_LEN\s*)(\d*)"
        regexp_dict = {
            "library settings": setting_regexp,
            "progmem settings": progmem_regexp,
            "debug methods": debug_regexp,
            "optional methods": opt_method_regexp,
        }
        index = {
            "library settings": 0,
            "progmem settings": 0,
            "optional methods": 0,
            "debug methods": 0,
        }
        # 0:line number 1:comment/uncomment 2:macro name 3:value/bool
        fields = {"fields": {"0": "", "1": "", "2": "", "3": ""}}
        line_num = 0
        for line in self.cliOpt["config"]["file lines"]:
            for key in regexp_dict:
                line_pos = 0
                regexp = QRegularExpression(regexp_dict[key])
                while line_pos != -1:
                    match = regexp.match(line, line_pos)
                    if (
                        match.hasMatch()
                        and "DOXYGEN_XML_BUILD"
                        not in self.cliOpt["config"]["file lines"][line_num - 1]
                    ):
                        entry = {index[key]: copy.deepcopy(fields)}
                        entry[index[key]]["fields"]["0"] = line_num
                        idx = 1
                        for i in range(1, regexp.captureCount() + 1):
                            if "#define" not in str(match.captured(i)):
                                entry[index[key]]["fields"][str(idx)] = str(
                                    match.captured(i)
                                ).strip("\n")
                                idx += 1
                                if (
                                    line_num
                                    >= self.config_file_boolean_define_fields_line_start
                                ):
                                    if "//" in str(match.captured(1)):
                                        entry[index[key]]["fields"]["3"] = False
                                    elif "//" not in str(match.captured(1)):
                                        entry[index[key]]["fields"]["3"] = True
                                if idx == 4:
                                    break
                        line_pos += match.capturedLength()
                        self.cliOpt["config"]["tree"]["items"][key].update(entry)
                        self.cliOpt["config"]["var"][key].update(
                            {
                                str(entry[index[key]]["fields"]["2"]).strip(): str(
                                    entry[index[key]]["fields"]["3"]
                                )
                            }
                        )
                        self.default_settings_tree_values.update(
                            {
                                str(entry[index[key]]["fields"]["2"]).strip(): entry[
                                    index[key]
                                ]["fields"]["3"]
                            }
                        )
                        index[key] += 1
                    else:
                        break
            line_num += 1
        ParseInputHandlerConfig.logger.debug(
            str(json.dumps(self.cliOpt["config"]["tree"]["items"], indent=2))
        )


# end of file
