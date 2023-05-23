##
# @file pathing.py
# @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
# @brief InputHandler CLI generation tool
# @version 1.0
# @date 2023-05-22
# @copyright Copyright (c) 2023
# Copyright (C) 2023 Douglas Quigg (dstroy0) <dquigg123@gmail.com>
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 3 as published by the Free Software Foundation.

import os
import sys


class Pathing(object):
    inputhandler_h_path = None
    user_home_dir = None
    inputhandler_save_path = None
    interfaces_path = None
    session_path = None
    logs_path = None
    default_config_path = None
    cli_gen_tool_json_path = None

    def __init__(self) -> None:
        super(Pathing, self).__init__()

    def set_pathing(self):
        inputhandler_h_path = os.path.join(self.lib_root_path, "src", "InputHandler.h")
        with open(inputhandler_h_path, "r") as file:
            firstline = file.readline()
        file.close()
        # TODO prompt for library root
        if "library version" not in firstline:
            # bad config.h
            self.root_log_handler.warning(
                "this .h file:\n<"
                + str(self.args.config[0])
                + ">\nis not a valid InputHandler.h, please enter the full path to a valid InputHandler.h"
            )
            sys.exit(0)
        self.lib_version = (
            firstline.strip()
            .replace("/*", "")
            .replace("*/", "")
            .replace("library version", "")
            .replace(" ", "")
        )
        # set save pathing and make save directories
        user_home_dir = os.path.expanduser("~")
        inputhandler_save_path = os.path.join(
            user_home_dir, "Documents", "InputHandler"
        )
        if not os.path.exists(inputhandler_save_path):
            os.mkdir(inputhandler_save_path)
            if not os.path.exists(inputhandler_save_path):
                print(
                    f"failed to make necessary directory:\n{inputhandler_save_path}\nexiting."
                )
                sys.exit(1)
        interfaces_path = os.path.abspath(
            os.path.join(inputhandler_save_path, "interfaces")
        )
        if not os.path.exists(interfaces_path):
            os.mkdir(interfaces_path)
            if not os.path.exists(interfaces_path):
                print(f"failed to make necessary directory:\n{interfaces_path}")
                sys.exit(1)
        session_path = os.path.abspath(os.path.join(inputhandler_save_path, "session"))
        if not os.path.exists(session_path):
            os.mkdir(session_path)
            if not os.path.exists(session_path):
                print(f"failed to make necessary directory:\n{session_path}")
                sys.exit(1)
        logs_path = os.path.abspath(os.path.join(inputhandler_save_path, "logs"))
        if not os.path.exists(logs_path):
            os.mkdir(logs_path)
            if not os.path.exists(logs_path):
                print(f"failed to make necessary directory:\n{logs_path}")
                sys.exit(1)

        # /InputHandler/src/config/config.h
        default_config_path = os.path.abspath(
            os.path.join(self.lib_root_path, "src/config/config.h")
        )
        # /InputHandler/session/cli_gen_tool.json
        cli_gen_tool_json_path = os.path.abspath(
            os.path.join(inputhandler_save_path, "session/cli_gen_tool.json")
        )
        print(inputhandler_save_path)
        print(cli_gen_tool_json_path)

        Pathing.default_config_path = default_config_path
        Pathing.cli_gen_tool_json_path = cli_gen_tool_json_path
        Pathing.inputhandler_h_path = inputhandler_h_path
        Pathing.user_home_dir = user_home_dir
        Pathing.inputhandler_save_path = inputhandler_save_path
        Pathing.interfaces_path = interfaces_path
        Pathing.session_path = session_path
        Pathing.logs_path = logs_path
        self.inputhandler_h_path = inputhandler_h_path
        self.user_home_dir = user_home_dir
        self.inputhandler_save_path = inputhandler_save_path
        self.interfaces_path = interfaces_path
        self.session_path = session_path
        self.logs_path = logs_path
        self.default_config_path = default_config_path
        self.cli_gen_tool_json_path = cli_gen_tool_json_path
