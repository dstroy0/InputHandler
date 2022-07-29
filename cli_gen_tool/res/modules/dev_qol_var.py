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

## Automatically generated file docstring.
file_docs_format_string = """/* Generated by InputHandler's /InputHandler/cli_gen_tool/cli_gen_tool.py version {docs_version} */
/**
* @file {docs_filename}
* @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
* @brief {docs_brief}
* @version {docs_version}
* @date {docs_date}
*
* @copyright Copyright (c) {docs_year}
*/
/*
* Copyright (c) {docs_year} Douglas Quigg (dstroy0) <dquigg123@gmail.com>
* This program is free software; you can redistribute it and/or
* modify it under the terms of the GNU General Public License
* version 3 as published by the Free Software Foundation.
*/
"""

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
    "var": {"tool_version": str(version)},
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
        "var": {"outputToStream": False, "defaultFunction": False, "listCommands": False, "listSettings": False},
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


# file strings and filestring_db dict
setup_h_filestring = """
#if !defined(__CLI_SETUP__)
    #define __CLI_SETUP__
    #include "InputHandler.h"
    #include "functions.h"
    #include "parameters.h"

{outputbuffer}
const PROGMEM IH_pname pname = "{processname}"; // process name
const PROGMEM IH_eol peol = "{processeol}"; // process end of line characters
const PROGMEM IH_input_cc pinputcc = "{processinputcontrolchar}"; // input control char sequence
const PROGMEM IH_wcc pwcc = "{processwildcardchar}"; // process wildcard char

// data delimiter sequences
const PROGMEM InputProcessDelimiterSequences pdelimseq = {{
    {numdelimseq}, // number of delimiter sequences
    {delimseqlens}, // delimiter sequence lens
    {delimseqs} // delimiter sequences
}};

// start stop data delimiter sequences
const PROGMEM InputProcessStartStopSequences pststpseq = {{
    {numstartstoppairs}, // num start stop sequence pairs
    {startstopseqlens}, // start stop sequence lens
    {startstopseqs} // start stop sequence pairs
}};

const PROGMEM InputProcessParameters input_prm[1] = {{
    &pname,
    &peol,
    &pinputcc,
    &pwcc,
    &pdelimseq,
    &pststpseq}};

// constructor
{constructor}{setupprototype}{loopprototype}
// end of file
"""

setup_cpp_setup_function = """
void InputHandler_setup()
{{{setupfunctionentry}{defaultfunction}{commandlist}{begin}{options}
}}
"""

setup_cpp_loop_function = """
void InputHandler_loop()
{{{loopstatements}
}}
"""

setup_cpp_filestring = """
#include setup.h

{setupfunction}{loopfunction}

#endif

// end of file
"""

functions_h_filestring = """
#if !defined(__FUNCTIONS_H__)
    #define __FUNCTIONS_H__
    #include "InputHandler.h"
    
{functionprototypes}

#endif
// end of file
"""

functions_cpp_functionstring = """void {functionname}(UserInput* _{objectname})
{{
    {statements}
}}
"""
functions_cpp_filestring = """
#if !defined(__FUNCTIONS_CPP__)
    #define __FUNCTIONS_CPP__
    #include "functions.h"
    
{functions}

#endif
// end of file
"""

commandparameters_string = """
/**
   @brief CommandParameters struct for {functionname}
*/
const PROGMEM CommandParameters {functionname}_param[1] = 
{{
    {functionname}, // function pointer
    {wildcardflag}, // wildcard flag
    {commandstring}, // command string
    {lencommandstring}, // command string num characters
    {parentid}, // parent id
    {commandid}, // this command id (tree unique)
    {commanddepth}, // command depth
    {commandsubcommands}, // number of subcommands
    {argumenthandling}, // argument handling
    {minnumargs}, // minimum expected number of arguments
    {maxnumargs}, // maximum expected number of arguments
    /* UITYPE arguments */
    {argtypearray}    
}};
{commandconstructor}
"""

nested_commandparameters_string = """
/**
   @brief CommandParameters struct for {functionname}
*/
const PROGMEM CommandParameters {functionname}_param[1 /* root */ + {numberofchildren} /* child(ren) */] = 
{{
    {{
      {functionname}, // function pointer
      {wildcardflag}, // wildcard flag
      {commandstring}, // command string
      {lencommandstring}, // command string num characters
      {parentid}, // parent id
      {commandid}, // this command id (tree unique)
      {commanddepth}, // command depth
      {commandsubcommands}, // number of subcommands
      {argumenthandling}, // argument handling
      {minnumargs}, // minimum expected number of arguments
      {maxnumargs}, // maximum expected number of arguments
      /* UITYPE arguments */
      {argtypearray}   
    }},
    {children}    
}};
{commandconstructor}
"""

parameters_h_filestring = """
#if !defined(__PARAMETERS_H__)
    #define __PARAMETERS_H__
    #include "setup.h"
    
{parameters}

#endif
// end of file
"""
## contains file construction strings
filestring_db = {
    "setup": {
        "h": {
            "filestring components": {
                "outputbuffer": "\nchar {outputbuffername}[{buffersize}] = {bufferchar}; // output buffer size\n",                
                "classoutput": "({input_prm}, {outputbuffer}, buffsz({outputbuffer}))",
                "constructor": "UserInput {objectname}{classoutput};\n",
                "prototypes": {
                    "setup": "\nvoid InputHandler_setup();",
                    "loop": "\nvoid InputHandler_loop();"
                }                
            },
            "filestring": setup_h_filestring,
        }, # end setup h
        "cpp": {
            "filestring components": {
                "setup function": setup_cpp_setup_function,
                "loop function": setup_cpp_loop_function,
                "addCommand": {
                    "call": "\n  {objectname}.addCommand({commandparametersname});"
                },
                "defaultFunction": {
                    "call": "\n  {objectname}.defaultFunction({defaultfunctionname}); // default function is called when user input has no match or is not valid"
                },
                "listCommands": {
                    "call": "\n  {objectname}.listCommands(); // formats {outputbuffer} with the command list"
                },
                "listSettings": {
                    "call": "\n  {objectname}.listSettings(); // formats {outputbuffer} with the process settings (uses a lot of ram; for setting and testing)"
                },
                "outputToStream": {
                    "call": "\n  {objectname}.outputToStream({stream}); // class output"
                },
                "begin": {
                    "call": "\n  {objectname}.begin(); // Required. Returns true on success."
                },
                "setup function output":{
                    "stream": "\n  {stream}.println(F(\"{setupstring}\"));",
                    "buffer": "\n  if ((buffsz({outputbuffer})-outputIsAvailable()) > strlen(\"{setupstring}\")+1) {{\n    snprintf_P({outputbuffer} + outputIsAvailable(), \"{setupstring}\");\n  }}"
                }
            },
            "filestring": setup_cpp_filestring,
        }, # end setup cpp
    },  # end setup
    "functions": {
        "h": {
            "filestring components": {
                "function prototype": "\nvoid {functionname}(UserInput* _{objectname});"
            },
            "filestring": functions_h_filestring,
        },  # end functions h
        "cpp": {
            "filestring components": {
                "outputToStream": {
                    "call": "  _{objectname}->outputToStream({stream});"
                },
                "function": functions_cpp_functionstring,
            },
            "filestring": functions_cpp_filestring,
        },  # end functions cpp
    },  # end functions
    "parameters": {
        "h": {
            "filestring components": {
                "nested child": "    *{functionname}_param{comma} // pointer to {functionname}_param\n",
                "command constructor": "CommandConstructor {functionname}_({functionname}_param); //  help has a command string, and function specified",
                "parameters": commandparameters_string,
                "nested parameters": nested_commandparameters_string,
            },
            "filestring": parameters_h_filestring,
        }  # end parameters h
    },  # end parameters
}

# end dev qol var
# end of file
