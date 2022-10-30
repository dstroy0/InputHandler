##
# @file data_models.py
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
from collections import OrderedDict


class dataModels(object):
    ## library version
    version = ""
    ## This is used to create the session json.
    default_session_model = {
        "type": "session",
        "tool version": str(version),
        "opt": {
            "save_filename": None,
            "log_filename": None,
            "recent_files": [],
            "input_config_file_path": "",
            "output_dir": "",
            "log_levels": {
                "session": "",
                "file": "",
                "stream": "",
                "root": "",
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

    ## This dict can is used inside of the "command parameters index" key of cliopt_model
    parameters_index_struct = {
        # key to this command's parameters
        "parameters key": "",
        # key to this commands root index
        "root index key": "",
        # key(s) to child indices
        "child index key list": [],
    }

    ## This dict contains all pertinent information about a CLI, widget objects are created at runtime.
    cliopt_model = {
        "type": "cli options",
        "var": {
            "primary id key": 0,
            "number of commands": 0,
            "tool version": str(version),
        },
        "commands": {
            "index": {},
            "parameters": {},
            "QTreeWidgetItem": {"root": "", "container": {}, "table": {}},
            "QTableView": {
                "models": {},
            },
        },
        "config": {
            "file lines": [],
            "var": {
                "library settings": {
                    "UI_MAX_COMMANDS_IN_TREE": 0,
                    "UI_MAX_ARGS_PER_COMMAND": 0,
                    "UI_MAX_TREE_DEPTH_PER_COMMAND": 0,
                    "UI_MAX_NUM_CHILD_COMMANDS": 0,
                    "UI_MAX_CMD_LEN": 0,
                    "UI_MAX_NUM_DELIM_SEQ": 0,
                    "UI_MAX_NUM_START_STOP_SEQ": 0,
                    "UI_MAX_INPUT_LEN": 0,
                    "UI_MAX_PER_CMD_MEMCMP_RANGES": 0,
                    "UI_ECHO_ONLY": False,
                },
                "progmem settings": {
                    "UI_INPUT_TYPE_STRINGS_PGM_LEN": 0,
                    "UI_EOL_SEQ_PGM_LEN": 0,
                    "UI_DELIM_SEQ_PGM_LEN": 0,
                    "UI_START_STOP_SEQ_PGM_LEN": 0,
                    "UI_PROCESS_NAME_PGM_LEN": 0,
                    "UI_INPUT_CONTROL_CHAR_SEQ_PGM_LEN": 0,
                },
                "debug methods": {
                    "DEBUG_GETCOMMANDFROMSTREAM": False,
                    "DEBUG_READCOMMANDFROMBUFFER": False,
                    "DEBUG_GET_TOKEN": False,
                    "DEBUG_SUBCOMMAND_SEARCH": False,
                    "DEBUG_ADDCOMMAND": False,
                    "DEBUG_LAUNCH_LOGIC": False,
                    "DEBUG_LAUNCH_FUNCTION": False,
                    "DEBUG_INCLUDE_FREERAM": False,
                },
                "optional methods": {
                    "DISABLE_listSettings": False,
                    "DISABLE_listCommands": False,
                    "DISABLE_getCommandFromStream": False,
                    "DISABLE_nextArgument": False,
                    "DISABLE_getArgument": False,
                    "DISABLE_outputIsAvailable": False,
                    "DISABLE_outputIsEnabled": False,
                    "DISABLE_outputToStream": False,
                },
            },
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
        "files": {
            "README.md": copy.deepcopy(generated_filename_sub_dict),
            "config.h": copy.deepcopy(generated_filename_sub_dict),
            "setup.h": copy.deepcopy(generated_filename_sub_dict),
            "setup.cpp": copy.deepcopy(generated_filename_sub_dict),
            "parameters.h": copy.deepcopy(generated_filename_sub_dict),
            "functions.h": copy.deepcopy(generated_filename_sub_dict),
            "functions.cpp": copy.deepcopy(generated_filename_sub_dict),
        }
    }

    minimum_file_len_dict = {
        "README.md": 0,
        "config.h": 0,
        "setup.h": 57,
        "setup.cpp": 31,
        "parameters.h": 27,
        "functions.h": 27,
        "functions.cpp": 23,
    }

    ## the constructor
    def __init__(self, version) -> None:
        super(dataModels, self).__init__()
        dataModels.version = version


# end of file
