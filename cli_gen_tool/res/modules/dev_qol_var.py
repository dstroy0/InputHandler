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


## lib version
version = 0.1  # save serialization
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

## This is used to create the session json.
default_session_structure = {
    "type": "session",
    "tool_version": str(version),
    "opt": {
        "save_filename": None,
        "log_filename": None,
        "recent_files": {},
        "input_config_file_path": "",
        "output_dir": "",
        "window_size": "",
    },
}

## This dict contains all pertinent information about a CLI, widget objects are created at runtime.
command_line_interface_options_structure = {
    "type": "cli options",
    "var": {"num_commands": 0, "tool_version": str(version)},
    # each command tree will have a subdict in "command parameters index"
    "command parameters index": {},
    "commands": {},
    "config": {
        "file_lines": [],
        "tree": {
            "root": "",
            "parents": {
                "library settings": {"QTreeWidgetItem": {}},
                "progmem settings": {"QTreeWidgetItem": {}},
                "debug methods": {"QTreeWidgetItem": {}},
                "optional methods": {"QTreeWidgetItem": {}},
            },
            "items": {
                "library settings": {"QComboBox": {}, "QTreeWidgetItem": {}},
                "progmem settings": {"QComboBox": {}, "QTreeWidgetItem": {}},
                "debug methods": {"QComboBox": {}, "QTreeWidgetItem": {}},
                "optional methods": {"QComboBox": {}, "QTreeWidgetItem": {}},
            },
        },
    },
    "process output": {
        "var": {"buffer size": 0, "output stream": None},
        "tree": {
            "root": "",
            "items": {
                "buffer size": {"QTreeWidgetItem": {}},
                "output stream": {"QTreeWidgetItem": {}},
            },
        },
    },
    "builtin methods": {
        "var": {
            "outputToStream": False,
            "defaultFunction": False,
            "listCommands": False,
            "listSettings": False,
        },
        "tree": {
            "root": "",
            "items": {
                "defaultFunction": {"QTreeWidgetItem": {}, "QComboBox": {}},
                "listCommands": {"QTreeWidgetItem": {}, "QComboBox": {}},
                "listSettings": {"QTreeWidgetItem": {}, "QComboBox": {}},
                "outputToStream": {"QTreeWidgetItem": {}, "QComboBox": {}},
            },
        },
    },
    "process parameters": {
        "var": {
            "process name": "",
            "end of line characters": "\r\n",
            "input control char sequence": "##",
            "wildcard char": "*",
            "data delimiter sequences": {0: " ", 1: ","},
            "start stop data delimiter sequences": {0: '\\"', 1: '\\"'},
        },
        "tree": {
            "root": "",
            "parents": {},
            "items": {
                "process name": {"QTreeWidgetItem": {}},
                "end of line characters": {"QTreeWidgetItem": {}},
                "input control char sequence": {"QTreeWidgetItem": {}},
                "wildcard char": {"QTreeWidgetItem": {}},
                "data delimiter sequences": {
                    "QTreeWidgetItem": "",
                    "QTableWidget": "",
                    "QTableWidgetItems": {
                        "input cells": {},
                        "add row": {"item": "", "button": ""},
                        "remove row buttons": {"items": {}, "buttons": {}},
                    },
                },
                "start stop data delimiter sequences": {
                    "QTreeWidgetItem": "",
                    "QTableWidget": "",
                    "QTableWidgetItems": {
                        "input cells": {},
                        "add row": {"item": "", "button": ""},
                        "remove row buttons": {"items": {}, "buttons": {}},
                    },
                },
            },
        },
    },
}

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

## This dict is ordered to preserve insert order for code preview display.
generated_filename_dict = OrderedDict()
## This 'sub' dict is contained by each key in `generated_filename_dict`
generated_filename_sub_dict = {
    "filename": "",
    "file_lines_list": [],
    "tree_item": {},
    "contents_item": {},
    "text_widget": {0: "", 1: ""},
}
## This dict contains all generated files and associated widgets.
generated_filename_dict = {
    "config.h": copy.deepcopy(generated_filename_sub_dict),
    "setup.h": copy.deepcopy(generated_filename_sub_dict),
    "setup.cpp": copy.deepcopy(generated_filename_sub_dict),
    "parameters.h": copy.deepcopy(generated_filename_sub_dict),
    "functions.h": copy.deepcopy(generated_filename_sub_dict),
    "functions.cpp": copy.deepcopy(generated_filename_sub_dict),
}

# end dev qol var
# end of file
