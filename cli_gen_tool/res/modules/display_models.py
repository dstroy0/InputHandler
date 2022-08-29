##
# @file display_models.py
# @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
# @brief MainWindow external methods
# @version 1.0
# @date 2022-08-28
# @copyright Copyright (c) 2022
# Copyright (C) 2022 Douglas Quigg (dstroy0) <dquigg123@gmail.com>
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 3 as published by the Free Software Foundation.


class displayModels(object):
    ## Display Labels mirror tree structure. Containers are parents; keys are parent/child labels
    _tree = {
        "process output": {
            "buffer size": {
                "type": "bytes",
                "tooltip": "Must be greater than zero for class output.",
            },
            "output stream": {
                "type": "Stream",
                "tooltip": "Set an output Stream that is legal for your platform.",
            },
        },
        "process parameters": {
            "process name": {
                "type": "text",
                "tooltip": "The process name prepends all terminal output.",
            },
            "end of line characters": {
                "type": "text/control char",
                "tooltip": "Set to the eol char sequence of your data.",
            },
            "input control char sequence": {
                "type": "text",
                "tooltip": "Enter this sequence before an unescaped control char (r,n,e,t,b,etc.)",
            },
            "wildcard char": {
                "type": "char",
                "tooltip": "Any single char; * by default.",
            },
            "data delimiter sequences": {
                "type": "char sequence",
                "tooltip": "The char or sequence of chars that separate input data.",
            },
            "start stop data delimiter sequences": {
                "type": "char sequence",
                "tooltip": "Regex-like start/stop input sequences, for inputting long strings of data.",
            },
        },
        "builtin methods": {
            "outputToStream": {
                "type": "Enable/Disable",
                "tooltip": [
                    "",
                    "This will have no effect if you have not designated an output Stream and set a buffer size in 'process output'.",
                ],
            },
            "defaultFunction": {
                "type": "Enable/Disable",
                "tooltip": ["No default function.", "Default function enabled."],
            },
            "listCommands": {
                "type": "Enable/Disable",
                "tooltip": [
                    "No listCommands command",
                    "listCommands available to user.",
                ],
            },
            "listSettings": {
                "type": "Enable/Disable",
                "tooltip": [
                    "No listSettings command",
                    "listSettings available to user.",
                ],
            },
        },
        "config": {
            "library settings": {
                "UI_MAX_COMMANDS_IN_TREE": {
                    "type": "auto",
                    "tooltip": "This macro's associated variable(s) are auto sized by InputHandler::IH to uint8_t, uint16_t, or uint32_t",
                },
                "UI_MAX_ARGS_PER_COMMAND": {
                    "type": "auto",
                    "tooltip": "This macro's associated variable(s) are auto sized by InputHandler::IH to uint8_t, uint16_t, or uint32_t",
                },
                "UI_MAX_TREE_DEPTH_PER_COMMAND": {
                    "type": "auto",
                    "tooltip": "This macro's associated variable(s) are auto sized by InputHandler::IH to uint8_t, uint16_t, or uint32_t",
                },
                "UI_MAX_NUM_CHILD_COMMANDS": {
                    "type": "auto",
                    "tooltip": "This macro's associated variable(s) are auto sized by InputHandler::IH to uint8_t, uint16_t, or uint32_t",
                },
                "UI_MAX_CMD_LEN": {
                    "type": "auto",
                    "tooltip": "This macro's associated variable(s) are auto sized by InputHandler::IH to uint8_t, uint16_t, or uint32_t",
                },
                "UI_MAX_NUM_DELIM_SEQ": {
                    "type": "auto",
                    "tooltip": "This macro's associated variable(s) are auto sized by InputHandler::IH to uint8_t, uint16_t, or uint32_t",
                },
                "UI_MAX_NUM_START_STOP_SEQ": {
                    "type": "auto",
                    "tooltip": "This macro's associated variable(s) are auto sized by InputHandler::IH to uint8_t, uint16_t, or uint32_t",
                },
                "UI_MAX_INPUT_LEN": {
                    "type": "auto",
                    "tooltip": "This macro's associated variable(s) are auto sized by InputHandler::IH to uint8_t, uint16_t, or uint32_t",
                },
                "UI_MAX_PER_CMD_MEMCMP_RANGES": {
                    "type": "auto",
                    "tooltip": "This macro's associated variable(s) are auto sized by InputHandler::IH to uint8_t, uint16_t, or uint32_t",
                },
                "UI_ECHO_ONLY": {
                    "type": "Enable/Disable",
                    "tooltip": [
                        "This functionality is optional. It alters the library output significantly.",
                        "Library output altered.",
                    ],
                },
            },
            "progmem settings": {
                "UI_INPUT_TYPE_STRINGS_PGM_LEN": {
                    "type": "constant bytes",
                    "tooltip": "Number of PROGMEM bytes this object uses.",
                },
                "UI_EOL_SEQ_PGM_LEN": {
                    "type": "constant bytes",
                    "tooltip": "Number of PROGMEM bytes this object uses.",
                },
                "UI_DELIM_SEQ_PGM_LEN": {
                    "type": "constant bytes",
                    "tooltip": "Number of PROGMEM bytes this object uses.",
                },
                "UI_START_STOP_SEQ_PGM_LEN": {
                    "type": "constant bytes",
                    "tooltip": "Number of PROGMEM bytes this object uses.",
                },
                "UI_PROCESS_NAME_PGM_LEN": {
                    "type": "constant bytes",
                    "tooltip": "Number of PROGMEM bytes this object uses.",
                },
                "UI_INPUT_CONTROL_CHAR_SEQ_PGM_LEN": {
                    "type": "constant bytes",
                    "tooltip": "Number of PROGMEM bytes this object uses.",
                },
            },
            "debug methods": {
                "DEBUG_GETCOMMANDFROMSTREAM": {
                    "type": "Enable/Disable",
                    "tooltip": [
                        "",
                        "Output debugging information from InputHandler::getCommandFromStream()",
                    ],
                },
                "DEBUG_READCOMMANDFROMBUFFER": {
                    "type": "Enable/Disable",
                    "tooltip": [
                        "",
                        "Output debugging information from InputHandler::readCommandFromBuffer",
                    ],
                },
                "DEBUG_GET_TOKEN": {
                    "type": "Enable/Disable",
                    "tooltip": "Output debugging information from InputHandler::getToken()",
                },
                "DEBUG_SUBCOMMAND_SEARCH": {
                    "type": "Enable/Disable",
                    "tooltip": [
                        "",
                        "Output debugging information from InputHandler::subCommandSearch()",
                    ],
                },
                "DEBUG_ADDCOMMAND": {
                    "type": "Enable/Disable",
                    "tooltip": [
                        "",
                        "Output debugging information from InputHandler::addCommand()",
                    ],
                },
                "DEBUG_LAUNCH_LOGIC": {
                    "type": "Enable/Disable",
                    "tooltip": [
                        "",
                        "Output debugging information from InputHandler::launchLogic()",
                    ],
                },
                "DEBUG_LAUNCH_FUNCTION": {
                    "type": "Enable/Disable",
                    "tooltip": [
                        "",
                        "Output debugging information from InputHandler::launchFunction()",
                    ],
                },
                "DEBUG_INCLUDE_FREERAM": {
                    "type": "Enable/Disable",
                    "tooltip": [
                        "",
                        "Output debugging information from InputHandler::freeRam()",
                    ],
                },
            },
            "optional methods": {
                "DISABLE_listSettings": {
                    "type": "Enable/Disable",
                    "tooltip": [
                        "InputHandler::listSettings() enabled",
                        "InputHandler::listSettings() disabled",
                    ],
                },
                "DISABLE_listCommands": {
                    "type": "Enable/Disable",
                    "tooltip": [
                        "InputHandler::listCommands() enabled",
                        "InputHandler::listCommands() disabled",
                    ],
                },
                "DISABLE_getCommandFromStream": {
                    "type": "Enable/Disable",
                    "tooltip": [
                        "InputHandler::getCommandFromStream() enabled",
                        "InputHandler::getCommandFromStream() disabled",
                    ],
                },
                "DISABLE_nextArgument": {
                    "type": "Enable/Disable",
                    "tooltip": [
                        "InputHandler::nextArgument() enabled",
                        "InputHandler::nextArgument() disabled",
                    ],
                },
                "DISABLE_getArgument": {
                    "type": "Enable/Disable",
                    "tooltip": [
                        "InputHandler::getArgument() enabled",
                        "InputHandler::getArgument() disabled",
                    ],
                },
                "DISABLE_outputIsAvailable": {
                    "type": "Enable/Disable",
                    "tooltip": [
                        "InputHandler::outputIsAvailable() enabled",
                        "InputHandler::outputIsAvailable() disabled",
                    ],
                },
                "DISABLE_outputIsEnabled": {
                    "type": "Enable/Disable",
                    "tooltip": [
                        "InputHandler::outputIsEnabled() enabled",
                        "InputHandler::outputIsEnabled() disabled",
                    ],
                },
                "DISABLE_outputToStream": {
                    "type": "Enable/Disable",
                    "tooltip": [
                        "InputHandler::outputToStream() enabled",
                        "InputHandler::outputToStream() disabled",
                    ],
                },
                "DISABLE_clearOutputBuffer": {
                    "type": "Enable/Disable",
                    "tooltip": [
                        "InputHandler::clearOutputBuffer() enabled",
                        "InputHandler::clearOutputBuffer() disabled",
                    ],
                },
                "DISABLE_readCommandFromBufferErrorOutput": {
                    "type": "Enable/Disable",
                    "tooltip": [
                        "Error information output on detect.",
                        "No error output.",
                    ],
                },
                "DISABLE_ui_out": {
                    "type": "Enable/Disable",
                    "tooltip": [
                        "Library capable of output",
                        "Library not capable of output",
                    ],
                },
            },
        },
    }
