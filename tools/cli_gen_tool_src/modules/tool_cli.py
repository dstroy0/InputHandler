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

import os
import sys
import json
import logging
import pathlib
import argparse


class ToolCLI(object):
    def __init__(self):
        super(ToolCLI, self).__init__()

    def get_args(self):
        # cli_gen_tool script command line interface
        parser = argparse.ArgumentParser(
            prog=os.path.basename(__file__),
            description="generate a CLI in target directory using a CLI settings json",
        )
        parser.add_argument(
            "-p",
            "--preview",
            required=False,
            help="-p or --preview; generates a preview of all CLI files and prints them to the terminal, you will be prompted to generate the cli files after review.",
            action="store_true",
        )
        parser.add_argument(
            "-l",
            "--library",
            nargs=1,
            type=pathlib.Path,
            required=False,
            help="-l or --library <path to InputHandler library>; required.",
            metavar="",
        )
        parser.add_argument(
            "-o",
            "--options",
            nargs=1,
            type=pathlib.Path,
            required=False,
            help="-o or --options <path to InputHandler cli options json>; required.",
            metavar="",
        )
        parser.add_argument(
            "-d",
            "--destination",
            nargs=1,
            type=pathlib.Path,
            required=False,
            help="-d or --destination <path to output generated files>; required.",
            metavar="",
        )
        parser.add_argument(
            "-c",
            "--config",
            nargs=1,
            type=pathlib.Path,
            required=False,
            help="-c or --config <path to Inputhandler config.h>; path to alternate config file",
            metavar="",
        )
        args = parser.parse_args(sys.argv[1:])
        args.headless = False
        args.library_path = self.get_library_path(args)
        args.cli_options_json = self.get_options_json(args)
        args.destination_path = self.get_destination_path(args)
        args.config_header_file = self.get_config(args)        
        return args

    def log_and_get_input(self, handler, message):
        terminator = handler.terminator
        handler.terminator = ""
        handler.info(message)
        handler.terminator = terminator
        return self.get_input()

    def get_input(self):
        pos = ["y", "ye", "yes"]
        neg = ["n", "no"]
        ip = str(input(" y/n").lower().strip())
        if ip in pos:
            return True
        elif ip in neg:
            return False
        elif chr(int(ip[0])) == chr(27):
            self.root_log_handler.info("User pressed ESC, exiting.")
            sys.exit(0)
        else:
            self.log_and_get_input(self.stream_log_handler, "Please enter Yes, No, or press Esc to exit.")

    def user_interact(self, log_message: str, return_string: bool = False):
        terminator = self.stream_log_handler.terminator
        self.stream_log_handler.terminator = ""
        self.root_log_handler.info(log_message)
        self.stream_log_handler.terminator = terminator
        if not return_string:
            return self.get_input()
        else:
            return input()

    def get_library_path(self, args):
        ip = None
        path = None
        if bool(args.library):
            args.headless = True
            path = os.path.abspath(str(args.library[0]))
        else:
            return None
        while ip is None:
            src = "src/InputHandler.h"
            src_path = os.path.join(path, src)
            if not os.path.exists(path) or not os.path.exists(src_path):
                ip = self.user_interact(
                    f"Invalid library path:\n{path}\nwould you like to select another?"
                )
            if ip is True:
                path = self.user_interact("Enter a path: ", True)
                if os.path.exists(os.path.abspath(path)):
                    src_path = os.path.abspath(os.path.join(path, src))
                    if os.path.exists(os.path.abspath(src_path)):
                        return path
                else:
                    ip = None
            if ip is False:
                self.root_log_handler.info(f"User elected to exit.")
                sys.exit(0)
        return path

    def get_destination_path(self, args):
        ip = None
        path = None
        if bool(args.destination):
            args.headless = True
            path = os.path.abspath(str(args.destination[0]))
        else:
            return None
        while ip is None:
            if not os.path.exists(path) and ip is None:
                ip = self.user_interact(
                    f"The selected destination directory:\n{path}\ndoes not exist, would you like to create it?",
                )
            else:
                break
            if ip is True:
                try:
                    path = os.path.abspath(
                        self.user_interact("Destination path: ", True)
                    )
                    if not os.path.exists(path):
                        os.mkdir(path)
                    break
                except Exception as e:
                    emsg = e.message
                    eargs = e.args
                    ip = self.user_interact(
                        f"Unable to create directory:\n{path}\nException:\n{emsg}\n{eargs}\nWould you like to try again?"
                    )
            if ip is False:
                self.root_log_handler.info("User elected to exit.")
                sys.exit(0)
        return path

    def get_options_json(self, args):
        ip = None
        if bool(args.options):
            args.headless = True
            cli_options_path = os.path.abspath(str(args.options[0]))
        else:
            return None
        filedata = None
        while ip is None:
            if (
                ".json" not in cli_options_path
                or not os.path.exists(cli_options_path)
                and ip is None
            ):
                if ".json" not in cli_options_path:
                    # no cliopt json
                    self.root_log_handler.info(
                        f"The path to the json is incorrect, did you forget the .json?"
                    )
                if not os.path.exists(cli_options_path):
                    self.root_log_handler.warning(
                        f"The path to the json does not exist."
                    )
                ip = self.user_interact(
                    "Would you like to select another cli options json?"
                )
            if ip is True:
                if os.path.exists(cli_options_path):
                    try:
                        with open(cli_options_path, "r") as file:
                            filedata = file.read()
                            file.close()
                            try:
                                filedata = json.loads(filedata)
                                break
                            except:
                                # bad json
                                self.root_log_handler.warning(f"Invalid json format")
                                cli_options_path = ""
                                ip = None
                            if filedata["type"] != "cli options":
                                # wrong json
                                self.root_log_handler.warning(f"Invalid json type")
                                cli_options_path = ""
                                ip = None
                    except Exception as e:
                        emsg = e.message
                        eargs = e.args
                        self.root_log_handler.warning(
                            f"Cannot open file:\n{cli_options_path}\nException:\n{emsg}\n{eargs}"
                        )
                        ip = None
                        cli_options_path = ""
                else:
                    cli_options_path = self.user_interact(
                        "Enter the path to a cli options json: ", True
                    )
                    ip = None
            if ip is False:
                self.root_log_handler.info("User elected to exit.")
                sys.exit(0)
        return filedata

    def get_config(self, args):
        ip = None
        filedata = None
        if bool(args.config):
            args.headless = True
            config_path = os.path.abspath(args.config[0])
        else:
            return None
        while ip is None:
            if (
                not os.path.exists(config_path)
                or ".h" not in config_path
                and ip is None
            ):
                if not os.path.exists(config_path):
                    self.root_log_handler.warning(
                        f"The path to config.h is incorrect:\n{config_path}"
                    )
                if ".h" not in config_path:
                    self.root_log_handler.warning("Did not find a header extension.")
                ip = self.user_interact(
                    "Would you like to enter a new path to config.h?"
                )
            if ip is True:
                config_path = os.path.abspath(
                    self.user_interact(
                        "Enter the path to the InputHandler config.h you want to use:",
                        True,
                    )
                )
                try:
                    with open(config_path, "r") as file:
                        filedata = file.read()
                    file.close()
                except Exception as e:
                    emsg = e.message
                    eargs = e.args
                    self.root_log_handler.warning(
                        f"Cannot open:\n{config_path}\nException:\n{emsg}\n{eargs}"
                    )
                    ip = None
                if (
                    "#if !defined(__INPUTHANDLER_CONFIG_H__)" not in filedata
                    and ip is not None
                ):
                    ip = self.user_interact(
                        f"The .h file at this path:\n{config_path}\nis not valid, would you like to select another?"
                    )
            if ip is False:
                self.root_log_handler.info("User elected to exit.")
                sys.exit(0)
        return filedata
