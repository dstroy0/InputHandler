##
# @file display_models.py
# @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
# @brief MainWindow external methods
# @version 1.0
# @date 2023-05-22
# @copyright Copyright (c) 2023
# Copyright (C) 2023 Douglas Quigg (dstroy0) <dquigg123@gmail.com>
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 3 as published by the Free Software Foundation.


class DisplayModels(object):
    """display models and tooltips

    Args:
        object (object): base object specialization
    """

    ## Display Labels mirror data tree structure. Containers are parents; keys are parent/child labels
    _settings_tree_display = {
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
                    "Enabling this will direct class output to the Stream designated in 'process output'.",
                    "This will have no effect if you have not designated an output Stream and set a buffer size in 'process output'.",
                ],
            },
            "defaultFunction": {
                "type": "Enable/Disable",
                "tooltip": [
                    "No default function (called on unknown command or input error).",
                    "Default function enabled (called on unknown command or input error).",
                ],
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
                "IH_MAX_COMMANDS_PER_TREE": {
                    "type": "auto",
                    "tooltip": "This macro's associated variable(s) are auto sized by InputHandler::IH to uint8_t, uint16_t, or uint32_t",
                },
                "IH_MAX_ARGS_PER_COMMAND": {
                    "type": "auto",
                    "tooltip": "This macro's associated variable(s) are auto sized by InputHandler::IH to uint8_t, uint16_t, or uint32_t",
                },
                "IH_MAX_TREE_DEPTH_PER_COMMAND": {
                    "type": "auto",
                    "tooltip": "This macro's associated variable(s) are auto sized by InputHandler::IH to uint8_t, uint16_t, or uint32_t",
                },
                "IH_MAX_NUM_CHILD_COMMANDS_PER_ROOT": {
                    "type": "auto",
                    "tooltip": "This macro's associated variable(s) are auto sized by InputHandler::IH to uint8_t, uint16_t, or uint32_t",
                },
                "IH_MAX_CMD_STR_LEN": {
                    "type": "auto",
                    "tooltip": "This macro's associated variable(s) are auto sized by InputHandler::IH to uint8_t, uint16_t, or uint32_t",
                },
                "IH_MAX_NUM_PROC_DELIM_SEQ": {
                    "type": "auto",
                    "tooltip": "This macro's associated variable(s) are auto sized by InputHandler::IH to uint8_t, uint16_t, or uint32_t",
                },
                "IH_MAX_NUM_START_STOP_SEQ": {
                    "type": "auto",
                    "tooltip": "This macro's associated variable(s) are auto sized by InputHandler::IH to uint8_t, uint16_t, or uint32_t",
                },
                "IH_MAX_PROC_INPUT_LEN": {
                    "type": "auto",
                    "tooltip": "This macro's associated variable(s) are auto sized by InputHandler::IH to uint8_t, uint16_t, or uint32_t",
                },
                "IH_MAX_PER_ROOT_MEMCMP_RANGES": {
                    "type": "auto",
                    "tooltip": "This macro's associated variable(s) are auto sized by InputHandler::IH to uint8_t, uint16_t, or uint32_t",
                },
                "IH_ECHO_ONLY": {
                    "type": "Enable/Disable",
                    "tooltip": [
                        "This functionality is optional. It alters the library output significantly.",
                        "Library output altered.",
                    ],
                },
                "IH_VERBOSE": {
                    "type": "Enable/Disable",
                    "tooltip": [
                        "This functionality is optional. It alters the library output significantly.",
                        "Library output altered.",
                    ],
                },
            },
            "progmem settings": {
                "IH_INPUT_TYPE_STRINGS_PGM_LEN": {
                    "type": "constant bytes",
                    "tooltip": "Number of PROGMEM bytes this object uses.",
                },
                "IH_EOL_SEQ_PGM_LEN": {
                    "type": "constant bytes",
                    "tooltip": "Number of PROGMEM bytes this object uses.",
                },
                "IH_DELIM_SEQ_PGM_LEN": {
                    "type": "constant bytes",
                    "tooltip": "Number of PROGMEM bytes this object uses.",
                },
                "IH_START_STOP_SEQ_PGM_LEN": {
                    "type": "constant bytes",
                    "tooltip": "Number of PROGMEM bytes this object uses.",
                },
                "IH_PROCESS_NAME_PGM_LEN": {
                    "type": "constant bytes",
                    "tooltip": "Number of PROGMEM bytes this object uses.",
                },
                "IH_INPUT_CONTROL_CHAR_SEQ_PGM_LEN": {
                    "type": "constant bytes",
                    "tooltip": "Number of PROGMEM bytes this object uses.",
                },
            },
            "debug methods": {
                "DEBUG_GETCOMMANDFROMSTREAM": {
                    "type": "Enable/Disable",
                    "tooltip": [
                        "No debugging output from InputHandler::getCommandFromStream()",
                        "Output debugging information from InputHandler::getCommandFromStream()",
                    ],
                },
                "DEBUG_READCOMMANDFROMBUFFER": {
                    "type": "Enable/Disable",
                    "tooltip": [
                        "No debugging output from InputHandler::readCommandFromBuffer",
                        "Output debugging information from InputHandler::readCommandFromBuffer",
                    ],
                },
                "DEBUG_GET_TOKEN": {
                    "type": "Enable/Disable",
                    "tooltip": [
                        "No debugging output from InputHandler::getToken()",
                        "Output debugging information from InputHandler::getToken()",
                    ],
                },
                "DEBUG_SUBCOMMAND_SEARCH": {
                    "type": "Enable/Disable",
                    "tooltip": [
                        "No debugging output from InputHandler::subCommandSearch()",
                        "Output debugging information from InputHandler::subCommandSearch()",
                    ],
                },
                "DEBUG_ADDCOMMAND": {
                    "type": "Enable/Disable",
                    "tooltip": [
                        "No debugging output from InputHandler::addCommand()",
                        "Output debugging information from InputHandler::addCommand()",
                    ],
                },
                "DEBUG_LAUNCH_LOGIC": {
                    "type": "Enable/Disable",
                    "tooltip": [
                        "No debugging output from InputHandler::launchLogic()",
                        "Output debugging information from InputHandler::launchLogic()",
                    ],
                },
                "DEBUG_LAUNCH_FUNCTION": {
                    "type": "Enable/Disable",
                    "tooltip": [
                        "No debugging output from InputHandler::launchFunction()",
                        "Output debugging information from InputHandler::launchFunction()",
                    ],
                },
                "DEBUG_INCLUDE_FREERAM": {
                    "type": "Enable/Disable",
                    "tooltip": [
                        "No debugging output from InputHandler::freeRam()",
                        "Output debugging information from InputHandler::freeRam()",
                    ],
                },
            },
            "optional methods": {
                "DISABLE_listSettings": {
                    "type": "Enable/Disable",
                    "tooltip": [
                        "InputHandler::listSettings() enabled",
                        "InputHandler::listSettings() disabled, (THIS WILL OVERRIDE ANY OTHER SETTINGS RELATED TO InputHandler::listSettings()!)",
                    ],
                },
                "DISABLE_listCommands": {
                    "type": "Enable/Disable",
                    "tooltip": [
                        "InputHandler::listCommands() enabled",
                        "InputHandler::listCommands() disabled, (THIS WILL OVERRIDE ANY OTHER SETTINGS RELATED TO InputHandler::listCommands()!)",
                    ],
                },
                "DISABLE_getCommandFromStream": {
                    "type": "Enable/Disable",
                    "tooltip": [
                        "InputHandler::getCommandFromStream() enabled",
                        "InputHandler::getCommandFromStream() disabled, (THIS WILL OVERRIDE ANY OTHER SETTINGS RELATED TO InputHandler::getCommandFromStream()!)",
                    ],
                },
                "DISABLE_nextArgument": {
                    "type": "Enable/Disable",
                    "tooltip": [
                        "InputHandler::nextArgument() enabled",
                        "InputHandler::nextArgument() disabled, (THIS WILL OVERRIDE ANY OTHER SETTINGS RELATED TO InputHandler::nextArgument()!)",
                    ],
                },
                "DISABLE_getArgument": {
                    "type": "Enable/Disable",
                    "tooltip": [
                        "InputHandler::getArgument() enabled",
                        "InputHandler::getArgument() disabled, (THIS WILL OVERRIDE ANY OTHER SETTINGS RELATED TO InputHandler::getArgument()!)",
                    ],
                },
                "DISABLE_outputIsAvailable": {
                    "type": "Enable/Disable",
                    "tooltip": [
                        "InputHandler::outputIsAvailable() enabled",
                        "InputHandler::outputIsAvailable() disabled, (THIS WILL OVERRIDE ANY OTHER SETTINGS RELATED TO InputHandler::outputIsAvailable()!)",
                    ],
                },
                "DISABLE_outputIsEnabled": {
                    "type": "Enable/Disable",
                    "tooltip": [
                        "InputHandler::outputIsEnabled() enabled",
                        "InputHandler::outputIsEnabled() disabled, (THIS WILL OVERRIDE ANY OTHER SETTINGS RELATED TO InputHandler::outputIsEnabled()!)",
                    ],
                },
                "DISABLE_outputToStream": {
                    "type": "Enable/Disable",
                    "tooltip": [
                        "InputHandler::outputToStream() enabled",
                        "InputHandler::outputToStream() disabled, (THIS WILL OVERRIDE ANY OTHER SETTINGS RELATED TO InputHandler::outputToStream()!)",
                    ],
                },
                "DISABLE_clearOutputBuffer": {
                    "type": "Enable/Disable",
                    "tooltip": [
                        "InputHandler::clearOutputBuffer() enabled",
                        "InputHandler::clearOutputBuffer() disabled, (THIS WILL OVERRIDE ANY OTHER SETTINGS RELATED TO InputHandler::_clearOutputBuffer()!)",
                    ],
                },
                "DISABLE_readCommandFromBufferErrorOutput": {
                    "type": "Enable/Disable",
                    "tooltip": [
                        "Error information output on detect.",
                        "No error output or indication. (THIS WILL OVERRIDE ANY OTHER SETTINGS RELATED TO InputHandler::_readCommandFromBufferErrorOutput()!)",
                    ],
                },
                "DISABLE_ihout": {
                    "type": "Enable/Disable",
                    "tooltip": [
                        "Library capable of output and error indication.",
                        "Library not capable of output or error indication. (THIS WILL OVERRIDE ANY OTHER SETTINGS RELATED TO InputHandler::ihout()!)",
                    ],
                },
            },
        },
    }
    command_table_tooltip_dict = {
        "functionName": "functionName is the name of the function internal to the cli, it is a combination of your command string and this function's unique id.",
        "returnFunctionName": "returnFunctionName is blank unless your command has arguments; it is the name of the function that you copy into your code to do things with the arguments you collect for that function.",
        "commandString": "commandString is the string of characters that triggers the execution of designated command when received and processed.",
        "commandLength": "commandLength is the total number of characters in the command.",
        "parentId": "parentId is this command's parent ID.",
        "commandId": "commandId is this command's ID.",
        "commandHasWildcards": "commandHasWildcards is a boolean indicator of whether or not this command has wildcard characters in it.",
        "commandDepth": "commandDepth is this command's depth in the command tree.",
        "commandSubcommands": "commandSubcommands is the number of subcommands this command will have, regardless of their depth in the command tree.",
        "commandArgumentHandling": "commandArgumentHandling is the main indicator of how this command will handle incoming arguments.",
        "commandMinArgs": "commandMinArgs is the MINIMUM number of arguments you can send this command to trigger it.",
        "commandMaxArgs": "commandMaxArgs is the MAXIMUM number of arguments you can send this command before it will stop triggering.",
        "commandArguments": "commandArguments is the array of argument types this command expects.",
    }
    argument_table_tooltip_dict = {
        "UINT8_T": "8-bit unsigned integer",
        "UINT16_T": "16-bit unsigned integer",
        "UINT32_T": "32-bit unsigned integer",
        "INT16_T": "16-bit signed integer",
        "FLOAT": "32-bit float",
        "CHAR": "8-bit char",
        "START_STOP": "array of 8-bit char",
        "NOTYPE": "no type validation",
        "NO_ARGS": "no arguments expected",
    }
