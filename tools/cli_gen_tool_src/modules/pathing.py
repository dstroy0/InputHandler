##
# @file pathing.py
# @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
# @brief InputHandler CLI generation tool
# @version 1.0
# @date 2023-05-16
# @copyright Copyright (c) 2023
# Copyright (C) 2023 Douglas Quigg (dstroy0) <dquigg123@gmail.com>
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 3 as published by the Free Software Foundation.

import os, sys
class Pathing(object):
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
        self.user_home_dir = os.path.expanduser("~")
        self.inputhandler_save_path = os.path.join(
            self.user_home_dir, "Documents", "InputHandler"
        )
        if not os.path.exists(self.inputhandler_save_path):
            os.mkdir(self.inputhandler_save_path)
            if not os.path.exists(self.inputhandler_save_path):
                print(
                    f"failed to make necessary directory:\n{self.inputhandler_save_path}\nexiting."
                )
                sys.exit(1)
        interfaces_path = os.path.join(self.inputhandler_save_path, "interfaces")
        if not os.path.exists(interfaces_path):
            os.mkdir(interfaces_path)
            if not os.path.exists(interfaces_path):
                print(f"failed to make necessary directory:\n{interfaces_path}")
                sys.exit(1)
        session_path = os.path.join(self.inputhandler_save_path, "session")
        if not os.path.exists(session_path):
            os.mkdir(session_path)
            if not os.path.exists(session_path):
                print(f"failed to make necessary directory:\n{session_path}")
                sys.exit(1)
        logs_path = os.path.join(self.inputhandler_save_path, "logs")
        if not os.path.exists(logs_path):
            os.mkdir(logs_path)
            if not os.path.exists(logs_path):
                print(f"failed to make necessary directory:\n{logs_path}")
                sys.exit(1)