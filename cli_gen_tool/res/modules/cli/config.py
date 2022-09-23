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


class cliConfig(object):
    def __init__(self) -> None:
        super(cliConfig, self).__init__()

    # refresh the contents of config.h
    def config_h(self, item_string, place_cursor=False):
        self.code_preview_dict["files"]["config.h"]["file_lines_list"] = self.cliOpt[
            "config"
        ]["file lines"]
        cfg_dict = self.cliOpt["config"]["tree"]["items"]
        # the contents at each key represents a config.h file line
        for key in cfg_dict:
            for item in cfg_dict[key]:
                if "QComboBox" not in str(item) and "QTreeWidgetItem" not in str(item):
                    sub_dict = cfg_dict[key][item]["fields"]
                    if sub_dict["3"] == True or sub_dict["3"] == False:
                        val = ""
                    else:
                        val = sub_dict["3"]
                    line = (
                        str(sub_dict["1"]) + "#define " + str(sub_dict["2"]) + str(val)
                    )
                    self.code_preview_dict["files"]["config.h"]["file_lines_list"][
                        int(sub_dict["0"])
                    ] = line
        code_string = self.list_to_code_string(
            self.code_preview_dict["files"]["config.h"]["file_lines_list"]
        )
        self.set_code_string("config.h", code_string, item_string, place_cursor)
        # end update_config_h


# end of file
