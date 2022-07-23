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
import datetime
import logging
from logging.handlers import RotatingFileHandler
from collections import OrderedDict
from PySide6.QtCore import QDir


# dev qol var
# these are here for ease of access, clarity, or both


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

_log_filename = "cli_gen_tool.log"
_log_format = "%(asctime)s - [%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(line:%(lineno)d) - %(message)s"
_log_formatter = logging.Formatter(_log_format)
# log filehandler
log_file_handler = RotatingFileHandler(
    log_path + _log_filename, "a", 10 * _MB, backupCount=5
)

## How long should the splash be displayed (in ms)
splashscreen_duration = 1000
## The first line of every file generated by this tool.
file_first_line = (
    "/* Generated by InputHandler's /InputHandler/cli_gen_tool/cli_gen_tool.py version "
    + str(version)
    + " */\n"
)

## Automatically generated file docstring.
file_docs_format_string = """/**
* @file {}
* @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
* @brief {}
* @version {}
* @date {}
*
* @copyright Copyright (c) {}
*/
/*
* Copyright (c) {} Douglas Quigg (dstroy0) <dquigg123@gmail.com>
* This program is free software; you can redistribute it and/or
* modify it under the terms of the GNU General Public License
* version 3 as published by the Free Software Foundation.
*/"""
## The format list for the docstring.
file_docs_format_list = [
    "filename_ph",
    "brief_ph",
    "version_ph",
    datetime.date.today(),
    str(datetime.date.today())[0:4],
    str(datetime.date.today())[0:4],
]

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
    "commands": {},
    "config": {
        "file_lines": [],
        "tree": {
            "root": "",
            "parents": {},
            "items": {
                "library settings": {},
                "progmem settings": {},
                "debug methods": {},
                "optional methods": {},
            },
        },
    },
    "process output": {"var": {"buffer size": 0}, "tree": {"root": "", "items": {}}},
    "process parameters": {
        "var": {
            "process name": "",
            "end of line characters": "\r\n",
            "input control char sequence": "##",
            "wildcard char": "*",
            "data delimiter sequences": {0: " ", 1: ","},
            "start stop data delimiter sequences": {0: '"', 1: '"'},
        },
        "tree": {
            "root": "",
            "parents": {},
            "items": {
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
    "parameters.h": copy.deepcopy(generated_filename_sub_dict),
    "functions.h": copy.deepcopy(generated_filename_sub_dict),
    "functions.cpp": copy.deepcopy(generated_filename_sub_dict),
}

## The line in /InputHandler/src/config/config.h that boolean define fields start.
config_file_boolean_define_fields_line_start = 71

## This offsets code preview line display; Positive values move text lines down, Negative values move text lines up.
code_preview_text_line_offset = 4

# TODO these should be in a dict, filestring_construction_db or something
## setup.h
setup_h_class_output_string = "({input_prm}, {outputbuffer}, buffsz({outputbuffer}))"
setup_h_constructor_string = "UserInput {objectname}{classoutput};"
setup_h_addcommand_string = "    {objectname}.addCommand({commandparametersname});\n"
setup_h_options_string_list = [
    "    {objectname}.listCommands(); // formats output_buffer with the command list\n",
    "    {objectname}.outputToStream({stream}); // class output\n",
]
setup_h_output_buffer_string = (
    "\nchar output_buffer[{buffersize}] = {bufferchar}; // output buffer size\n"
)
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

// start stop delimiter sequences
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
{constructor}

void InputHandler_setup()
{{
    Serial.println(F("{setupstring}"));
    {objectname}.defaultFunction(unrecognized); // set default function, called when user input has no match or is not valid
    {commandlist}
    {objectname}.begin();                       // required.  returns true on success.
    {options}
}}
#endif
// end of file
"""
# end setup.h

## functions.h
# prototypes only
function_prototype = "void {functionname}(UserInput* _{objectname});"
# TODO finish builtin prototypes dict
builtin_prototypes_dict = {"help": "", "unrecognized": ""}
functions_h_filestring = """
#if !defined(__FUNCTIONS_H__)
    #define __FUNCTIONS_H__
    #include "InputHandler.h"
    
{functionprototypes}

#endif
// end of file
"""
# end functions.h

## functions.cpp
# non-proto only
# TODO finish default function statements
builtin_function_statements_dict = {
    "outputToStream": "  _{objectname}->outputToStream({stream});"
}
function_string = """void {functionname}(UserInput* _{objectname})
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
# end functions.cpp

## parameters.h
# only CommandParameters and nests
commandparameters_string = """
/**
   @brief CommandParameters struct for {functionname}
*/
const PROGMEM CommandParameters {functionname}_param[1] = 
{{
    {functionname},                     // this is allowed to be NULL, if this is NULL and the terminating subcommand function ptr is also NULL nothing will launch (error)
    {wildcardflag},             // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
    {commandstring},                   // command string
    {lencommandstring},                        // command string characters
    {parentid},                     // parent id
    {commandid},                     // this command id
    {commanddepth},                     // command depth
    {commandsubcommands},                        // subcommands
    {argumenthandling}, // argument handling
    {minnumargs},                        // minimum expected number of arguments
    {maxnumargs},                        // maximum expected number of arguments
    /* UITYPE arguments */
    {argtypearray} // use NO_ARGS if the function expects no arguments    
}};
{commandconstructor}
"""

nested_commandparameters_child_string = (
    "    *{functionname}_param{comma} // pointer to {functionname}_param\n"
)

nested_commandparameters_string = """
/**
   @brief CommandParameters struct for {functionname}
*/
const PROGMEM CommandParameters {functionname}_param[1 /* root */ + {numberofchildren} /* child(ren) */] = 
{{
    {{
      {functionname},                     // this is allowed to be NULL, if this is NULL and the terminating subcommand function ptr is also NULL nothing will launch (error)
      {wildcardflag},             // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
      {commandstring},                   // command string
      {lencommandstring},                        // command string characters
      {parentid},                     // parent id
      {commandid},                     // this command id
      {commanddepth},                     // command depth
      {commandsubcommands},                        // subcommands
      {argumenthandling}, // argument handling
      {minnumargs},                        // minimum expected number of arguments
      {maxnumargs},                        // maximum expected number of arguments
      /* UITYPE arguments */
      {argtypearray} // use NO_ARGS if the function expects no arguments    
    }},
    {children}    
}};
{commandconstructor}
"""

commandconstructor_string = "CommandConstructor {functionname}_({functionname}_param); //  help has a command string, and function specified"

parameters_h_filestring = """
#if !defined(__PARAMETERS_H__)
    #define __PARAMETERS_H__
    #include "setup.h"
    
{parameters}

#endif
// end of file
"""
# end parameters.h

# end dev qol var
# end of file
