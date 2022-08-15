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
        "tool_version": str(version),
        "opt": {
            "save_filename": None,
            "log_filename": None,
            "recent_files": [],
            "input_config_file_path": "",
            "output_dir": "",
        },
    }

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

    ## listCommands parameters list
    LCcmdParam = [
        "listCommands",
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
        "parameters key": "",
        "is root command": True,
        "root command": None,
    }

    ## This dict contains all pertinent information about a CLI, widget objects are created at runtime.
    cliopt_model = {
        "type": "cli options",
        "var": {"num_commands": 0, "tool_version": str(version)},
        # each command tree will have a subdict in "command parameters index"
        "command parameters index": {},
        "commands": {
            "parameters": {},
            "QTreeWidgetItem": {"container": {}, "table": {}},
            "QTableView": {
                "models": {},
            },
        },
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
            "config.h": copy.deepcopy(generated_filename_sub_dict),
            "setup.h": copy.deepcopy(generated_filename_sub_dict),
            "setup.cpp": copy.deepcopy(generated_filename_sub_dict),
            "parameters.h": copy.deepcopy(generated_filename_sub_dict),
            "functions.h": copy.deepcopy(generated_filename_sub_dict),
            "functions.cpp": copy.deepcopy(generated_filename_sub_dict),
        }
    }

    ## the constructor
    def __init__(self, version) -> None:
        super(dataModels, self).__init__()
        dataModels.version = version


# end of file
