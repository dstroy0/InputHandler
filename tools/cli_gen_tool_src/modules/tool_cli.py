##
# @file tool_cli.py
# @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
# @brief MainWindow external methods
# @version 1.0
# @date 2023-05-22
# @copyright Copyright (c) 2023
# Copyright (C) 2023 Douglas Quigg (dstroy0) <dquigg123@gmail.com>
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 3 as published by the Free Software Foundation.

import argparse, pathlib, json, sys, os


class ToolCLI(object):
    def __init__(self):
        super(ToolCLI, self).__init__()

    def script_cli(self):
        # cli_gen_tool script command line interface
        self.parser = argparse.ArgumentParser(
            prog=os.path.basename(__file__),
            description="generate a CLI in target directory using a CLI settings json",
        )
        self.parser.add_argument(
            "-g",
            "--generate",
            nargs=3,
            type=pathlib.Path,
            required=False,
            help="-g <InputHandler dir> <dest dir> <path to cli options json> generates a CLI",
            metavar="",
        )
        self.parser.add_argument(
            "-c",
            "--config",
            nargs=1,
            type=pathlib.Path,
            required=False,
            help="-c <path to Inputhandler config.h> path to alternate config file",
            metavar="",
        )
        args = self.parser.parse_args(sys.argv[1:])

        # script cli only (no gui) when true
        args.headless = False
        # validate argparser input further
        if bool(args.generate):
            args.headless = True
            self.root_log_handler.info("InputHandler path: " + str(args.generate[0]))
            self.root_log_handler.info("output path: " + str(args.generate[1]))
            self.root_log_handler.info("cli options path: " + str(args.generate[2]))
            if not os.path.exists(str(args.generate[0])):
                self.root_log_handler.warning(
                    "the selected output directory:\n<"
                    + str(args.generate[1])
                    + ">\ndoes not exist, please enter the full path to the output directory"
                )
                sys.exit(0)
            if ".json" not in str(args.generate[2]):
                # no cliopt json
                self.root_log_handler.warning(
                    "invalid path:\n<"
                    + str(args.generate[2])
                    + ">\nplease enter the full path to the cli options json"
                )
                sys.exit(0)
            try:
                with open(str(args.generate[1]), "r") as file:
                    filedata = file.read()
                file.close()
            except Exception as e:
                self.root_log_handler.warning(
                    "cannot open:\n<"
                    + str(args.generate[1])
                    + ">\nmsg: "
                    + str(e.message)
                    + "\nargs: "
                    + str(e.args)
                )
                sys.exit(0)
            try:
                filedata = json.loads(filedata)
            except:
                # bad json
                self.root_log_handler.warning(
                    "this json:\n<"
                    + str(args.generate[1])
                    + ">\nis not valid, please enter the full path to a valid cli options json"
                )
                sys.exit(0)
            if filedata["type"] != "cli options":
                # wrong json
                self.root_log_handler.warning(
                    "this json:\n<"
                    + str(args.generate[1])
                    + ">\nis not a cli options json, please enter the full path to a valid cli options json"
                )
                sys.exit(0)
            self.cli_options = filedata

        if bool(args.config):
            filedata = ""
            self.root_log_handler.info(
                "InputHandler config.h path:\n<" + str(args.config[0]) + ">"
            )
            if ".h" not in str(args.config[0]):
                # no config.h
                self.root_log_handler.warning(
                    "please enter the full path to an InputHandler config.h"
                )
                sys.exit(0)
            try:
                with open(str(args.config[0]), "r") as file:
                    filedata = file.read()
                file.close()
            except Exception as e:
                self.root_log_handler.warning(
                    "cannot open:\n<"
                    + str(args.generate[1])
                    + ">\nmsg: "
                    + str(e.message)
                    + "\nargs: "
                    + str(e.args)
                )
                sys.exit(0)
            if "#if !defined(__INPUTHANDLER_CONFIG_H__)" not in filedata:
                # bad config.h
                self.root_log_handler.warning(
                    "this .h file:\n<"
                    + str(args.config[0])
                    + ">\nis not valid, please enter the full path to a valid InputHandler config.h"
                )
                sys.exit(0)
            self.session["opt"]["inputhandler_config_file_path"] = os.path.abspath(
                args.config[0]
            )
        return args
