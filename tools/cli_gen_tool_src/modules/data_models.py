##
# @file data_models.py
# @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
# @brief MainWindow external methods
# @version 1.0.0
# @date 2023-05-22
# @copyright Copyright (c) 2023
# Copyright (C) 2023 Douglas Quigg (dstroy0) <dquigg123@gmail.com>
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 3 as published by the Free Software Foundation.

from __future__ import absolute_import
import copy
from collections import OrderedDict


class DataModels(object):
    """app data models

    Args:
        object (object): base object specialization
    """

    ## the constructor
    def __init__(self, version: str) -> None:
        """the constructor

        Args:
            version (str): app version
        """
        super(DataModels, self).__init__()
        DataModels.version = version

    ## library version
    version = ""

    ## pio file structure
    pio_structure = {
        "project_directory": {
            "lib": {
                "CLI": {
                    "config": {
                        "files": ["config.h", "noedit.h"],
                        "utility": {"files": ["freeRam.h", "vsnprintf.h"]},
                    },
                    "files": [
                        "InputHandler.cpp",
                        "InputHandler.h",
                        "cli.h",
                        "functions.h",
                        "parameters.h",
                    ],
                },
                "files": ["README.md"],
            }
        }
    }

    ## arduino file structure
    arduino_structure = {
        "project_directory": {
            "CLI": {
                "config": {
                    "files": ["config.h", "noedit.h"],
                    "utility": {"files": ["freeRam.h", "vsnprintf.h"]},
                },
                "files": [
                    "InputHandler.cpp",
                    "InputHandler.h",
                    "cli.h",
                    "functions.h",
                    "parameters.h",
                ],
            },
            "files": ["README.md"],
        }
    }

    ## This is used to create the session json.
    default_session_model = {
        "type": "session",
        "tool version": str(version),
        "opt": {
            "save_file_path": None,
            "log_file_path": None,
            "recent_files": {
                "num_paths_to_keep": "5",
                "paths": [],
            },
            "inputhandler_config_file_path": None,
            "cli_output_dir": None,
            "log_level": None,
            "output": {
                "stream": "Serial",
                "buffer size": "700",
            },
            "builtin methods": {
                "outputToStream": True,
                "defaultFunction": True,
                "listCommands": True,
                "listSettings": True,
            },
        },
    }

    ## Command parameters dicts are constructed using keys from this list.
    command_parameters_dict_keys_list = [
        "functionName",
        "returnFunctionName",
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

    ## CommandParameters field settings
    command_parameters_input_field_settings_dict = {
        key: {
            "value": "",
            "enabled": True,
        }
        for (key) in command_parameters_dict_keys_list
    }

    wildcard_flag_strings = [
        "no_wildcards",
        "has_wildcards",
    ]

    arg_handling_strings = [
        "UI_ARG_HANDLING::no_args",
        "UI_ARG_HANDLING::one_type",
        "UI_ARG_HANDLING::type_arr",
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

    ## listCommands parameters list
    LCcmdParam = [
        "listCommands",
        "",
        "listCommands",
        "12",
        "0",
        "0",
        "no_wildcards",
        "0",
        "0",
        "UI_ARG_HANDLING::no_args",
        "0",
        "0",
        "{UITYPE::NO_ARGS}",
    ]
    listCommands = OrderedDict()
    listCommands = {
        "listCommands": dict(zip(command_parameters_dict_keys_list, LCcmdParam))
    }

    ## listSettings parameters list
    LScmdParam = [
        "listSettings",
        "",
        "listSettings",
        "12",
        "0",
        "0",
        "no_wildcards",
        "0",
        "0",
        "UI_ARG_HANDLING::no_args",
        "0",
        "0",
        "{UITYPE::NO_ARGS}",
    ]
    listSettings = OrderedDict()
    listSettings = {
        "listSettings": dict(zip(command_parameters_dict_keys_list, LScmdParam))
    }

    ## This dict is used inside of the "command parameters index" key of cliopt_model
    parameters_index_struct = {
        # key to this command's parameters
        "parameters key": "",
        # key to this commands root index
        "root index key": "",
        # key to this commands parent index
        "parent index key": "",
        # key(s) to child indices
        "child index key list": [],
    }

    ## This dict contains all pertinent information about a CLI, widget objects are created at runtime.
    cliopt_model = {
        "type": "cli options",
        "var": {
            "tool version": str(version),
        },
        "config": {
            "var": {
                "library settings": {},
                "progmem settings": {},
                "debug methods": {},
                "optional methods": {},
            },
        },
        "process output": {
            "var": {"buffer size": "0", "output stream": None},
        },
        "builtin methods": {
            "var": {
                "outputToStream": False,
                "defaultFunction": False,
                "listCommands": False,
                "listSettings": False,
            },
        },
        "process parameters": {
            "var": {
                "process name": "",
                "end of line characters": "\r\n",
                "input control char sequence": "##",
                "wildcard char": "*",
                "data delimiter sequences": {"0": " ", "1": ","},
                "start stop data delimiter sequences": {"0": '\\"', "1": '\\"'},
            },
        },
        "commands": {
            "primary id key": "0",
            "number of commands": "0",
            "index": {},
            "parameters": {},
        },
    }

    ## This dict is ordered to preserve insert order for code preview display.
    generated_filename_dict = OrderedDict()
    ## This 'sub' dict is contained by each key in `generated_filename_dict`
    generated_filename_sub_dict = {
        "filename": "",
        "file_lines_list": [],
        "file_string": "",
    }
    ## This dict contains all generated files and associated widgets.
    generated_filename_dict = {
        "files": {
            "README.md": copy.deepcopy(generated_filename_sub_dict),
            "config.h": copy.deepcopy(generated_filename_sub_dict),
            "cli.h": copy.deepcopy(generated_filename_sub_dict),
            "parameters.h": copy.deepcopy(generated_filename_sub_dict),
            "functions.h": copy.deepcopy(generated_filename_sub_dict),
        }
    }

    minimum_file_len_dict = {
        "README.md": 0,
        "config.h": 0,
        "cli.h": 57,
        "parameters.h": 27,
        "functions.h": 27,
    }

    button_sub_dict = {"QPushButton": None, "text": None, "enabled": False}

    button_dict = {"buttons": {}}

    button_tree_state_dict = {
        "tree": None,
        "items selected": [],
        "item selected": None,
        "is expanded": None,
        "root item selected": None,
        "index of top level item": None,
        "current item index": None,
        "root item index": None,
        "child count": None,
        "table widget": None,
        "combobox widget": None,
    }


# end of file
