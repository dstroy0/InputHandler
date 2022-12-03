##
# @file config.py
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


class cliConfig(object):
    def __init__(self) -> None:
        super(cliConfig, self).__init__()

    # refresh the contents of config.h
    def config_h(self, item_string, place_cursor=False):
        disable_define = "    // "
        enable_define = "       "
        self.code_preview_dict["files"]["config.h"]["file_lines_list"] = copy.deepcopy(
            self.input_config_file_lines
        )
        cfg_dict = self.cliOpt["config"]["var"]
        # the contents at each key represents a config.h file line
        for key in cfg_dict:
            for item in cfg_dict[key]:
                sub_dict = cfg_dict[key][item]
                if (
                    int(sub_dict["lineno"])
                    >= self.config_file_boolean_define_fields_line_start
                ):
                    if bool(sub_dict["value"]) == True:
                        val = ""
                        _enable = enable_define
                    elif bool(sub_dict["value"]) == False:
                        val = ""
                        _enable = disable_define
                else:
                    _enable = enable_define
                    val = sub_dict["value"]

                line = _enable + "#define " + str(item) + " " + val
                self.code_preview_dict["files"]["config.h"]["file_lines_list"][
                    int(sub_dict["lineno"])
                ] = line
        code_string = self.list_to_code_string(
            self.code_preview_dict["files"]["config.h"]["file_lines_list"]
        )
        self.set_code_string("config.h", code_string, item_string, place_cursor)
        # end update_config_h


# end of file
