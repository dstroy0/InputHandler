##
# @file dev_qol_var.py
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
import copy
import logging
from logging.handlers import RotatingFileHandler
from collections import OrderedDict
from PySide6.QtCore import QDir


# dev qol var
# these are here for ease of access, clarity, or both

## Library pathing
path = QDir()
path.cdUp()
lib_root_path = path.currentPath()
log_path = lib_root_path + "/logs/"

# log filesize
# kb = 2^10 == 1024 bytes
_KB = 2**10
# mb = 2^2^10 == 1048576 bytes
_MB = 2**2**10

file_log_level = logging.INFO  # file log level
stream_log_level = logging.INFO  # terminal log level
session_history_log_level = logging.INFO  # session history widget log level (F1)

_log_filename = "cli_gen_tool.log"
_log_format = "%(asctime)s - [%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(line:%(lineno)d) - %(message)s"
_log_formatter = logging.Formatter(_log_format)
# log filehandler
log_file_handler = RotatingFileHandler(
    log_path + _log_filename, "a", 10 * _MB, backupCount=5
)

## The line in /InputHandler/src/config/config.h that boolean define fields start.
config_file_boolean_define_fields_line_start = 71

## How long should the splash be displayed (in ms)
splashscreen_duration = 750

## Command parameters dicts are constructed using keys from this list.
command_parameters_dict_keys_list = [
    "functionName",
    "commandString",
    "commandLength",
    "parentId",
    "commandId",
    "commandHasWildcards",
    "commandDepth",
    "commandSubcommands",
    "commandArgumentHandling",
    "commandMinArgs",
    "commandMaxArgs",
    "commandArguments",
]



## Acceptable command argument types.
command_arg_types_list = [
    "UINT8_T",
    "UINT16_T",
    "UINT32_T",
    "INT16_T",
    "FLOAT",
    "CHAR",
    "STARTSTOP",
    "NOTYPE",
]



# end dev qol var
# end of file
