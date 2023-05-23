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
import pathlib
import argparse


class ToolCLI(object):
    def __init__(self):
        super(ToolCLI, self).__init__()

    def get_args(self):
        # cli_gen_tool script command line interface
        self.parser = argparse.ArgumentParser(
            prog=os.path.basename(__file__),
            description="generate a CLI in target directory using a CLI settings json",
        )
        self.parser.add_argument(
            "-p",
            "--preview",
            required=False,
            help="-p or --preview; generates a preview of all CLI files and prints them to the terminal, you will be prompted to generate the cli files after review.",
            metavar="",
            action="store_true",
        )
        self.parser.add_argument(
            "-c",
            "--config",
            nargs=1,
            type=pathlib.Path,
            required=False,
            help="-c or --config <path to Inputhandler config.h>; path to alternate config file",
            metavar="",
        )
        self.parser.add_argument(
            "-d",
            "--destination",
            nargs=1,
            type=pathlib.Path,
            required=True,
            help="-d or --destination <path to output generated files>; required.",
            metavar="",
        )
        self.parser.add_argument(
            "-l",
            "--library",
            nargs=1,
            type=pathlib.Path,
            required=True,
            help="-l or --library <path to InputHandler library>; required.",
            metavar="",
        )
        self.parser.add_argument(
            "-o",
            "--options",
            nargs=1,
            type=pathlib.Path,
            required=True,
            help="-o or --options <path to InputHandler cli options json>; required.",
            metavar="",
        )
        args = self.parser.parse_args(sys.argv[1:])

        args.headless = False

        if bool(args.preview):
            self.root_log_handler.info("Previewing CLI before generating")
        args.library_path = self.get_library_path(args)
        args.cli_options = self.load_options_json(args)
        args.destination_path = self.get_destination_path(args)
        args.config_file = self.load_config(args)
        args.headless = True

        return args

    def get_input(self):
        pos = ["y", "ye", "yes"]
        neg = ["n", "no"]
        ip = str(input(" y/n").lower().strip())
        if ip in pos:
            return True
        elif ip in neg:
            return False
        elif chr(ip[0]) == chr(27):
            self.root_log_handler.info("User pressed ESC, exiting.")
            sys.exit(0)
        else:
            self.root_log_handler.info("Please enter Yes, No, or press Esc to exit.")
            self.get_input()
            

    def get_library_path(self, args):
        ip = None
        if bool(args.library_path):
            path = os.path.abspath(str(args.library[0]))
        else:
            path = ""
        while ip is None:
            src = "src/InputHandler.h"
            src_path = os.path.join(path, src)
            if not os.path.exists(path) or not os.path.exists(src_path):
                self.root_log_handler.info(
                    f"Invalid library path:\n{path}\nwould you like to select another?"
                )
                ip = self.get_input()
            if ip is True:
                self.root_log_handler.info(f"Enter a path:\n")
                path = input()
                if os.path.exists(os.path.abspath(path)):
                    src_path = os.path.join(path, src)
                    if os.path.exists(os.path.abspath(src_path)):
                        return path
                else:
                    ip = None
            elif ip is False:
                self.root_log_handler.info(f"User elected to exit.")
                sys.exit(0)

    def get_destination_path(self, args):
        ip = None
        if bool(args.destination):
            destination_path = os.path.abspath(str(args.destination[0]))
        else:
            destination_path = ""
        while ip is None:
            if not os.path.exists(destination_path):
                self.root_log_handler.info(
                    "The selected destination directory:\n<"
                    + destination_path
                    + ">\ndoes not exist, would you like to create it?"
                )
                ip = self.get_input()
            else:
                break
            if ip is True:
                try:
                    destination_path = os.path.abspath(input())
                    if not os.path.exists(os.path.abspath(destination_path)):
                        os.mkdir(destination_path)
                    break
                except Exception as e:
                    emsg = e.message
                    eargs = e.args
                    self.root_log_handler.warning(
                        f"Unable to create directory:\n{destination_path}\nException:\n{emsg}\n{eargs}\nExiting."
                    )
                    sys.exit(1)
            elif ip is False:
                self.root_log_handler.info(
                    f"User elected to not create the directory:\n{destination_path}\nExiting."
                )
                sys.exit(0)
        return destination_path

    def load_options_json(self, args):
        ip = None
        if bool(args.options):
            cli_options_path = os.path.abspath(str(args.options[0]))
        else:
            cli_options_path = ""
        filedata = None
        while ip is None:
            if ".json" not in cli_options_path or not os.path.exists(cli_options_path) and ip is None:
                pr = False
                if ".json" not in cli_options_path:
                    # no cliopt json
                    self.root_log_handler.info(
                        f"The path to the json is incorrect, did you forget the .json?"
                    )
                    pr = True
                if pr is False and not os.path.exists(cli_options_path):
                    self.root_log_handler.warning(
                        f"The path to the json does not exist."
                    )
                self.root_log_handler.info("Would you like to select another cli options json?")
                ip = self.get_input()
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
                                self.root_log_handler.warning(
                                    f"Invalid json format"
                                )
                            if filedata["type"] != "cli options":
                                # wrong json
                                self.root_log_handler.warning(
                                    f"Invalid json type"
                                )
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
                    self.root_log_handler.info("Enter the path: ")
                    cli_options_path = input()
                    ip = None                    
            
            if ip is False:
                self.root_log_handler.info(
                    f"The was a problem with the cli options json, exiting."
                )
                sys.exit(0)
        
        return filedata

    def load_config(self, args):
        ip = None
        filedata = None
        if bool(args.config):
            config_path = os.path.abspath(args.config[0])
        else:
            config_path = ""

        while ip is None:
            if (
                not os.path.exists(config_path)
                or ".h" not in config_path
                and ip is None
            ):
                pr = False
                if not os.path.exists(config_path):
                    self.root_log_handler.warning(
                        f"The path to config.h is incorrect:\n{config_path}"
                    )
                    pr = True
                if ".h" not in config_path and pr is False:
                    self.root_log_handler.warning("Did not find a header extension.")
                self.root_log_handler.info(
                    "Would you like to enter a new path to config.h?"
                )
                ip = self.get_input()

            if ip is True:
                config_path = input()
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
                    self.root_log_handler.warning(
                        f"The .h file at this path:\n{config_path}\nis not valid, would you like to select another?"
                    )
                    ip = self.get_input()

            if ip is False:
                self.root_log_handler.info("User elected to exit.")
                sys.exit(0)
        return filedata
