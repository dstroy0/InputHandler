/* Generated by cli_gen_tool version <1.0>; using InputHandler version <0.9a> */
/**
* @file parameters.h
* @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
* @brief InputHandler autogenerated parameters.h
* @version 1.0
* @date 2023-02-24
*
* @copyright Copyright (c) 2023
*/
/*
* Copyright (c) 2023 Douglas Quigg (dstroy0) <dquigg123@gmail.com>
*
* License: GNU GPL3
* This program is free software; you can redistribute it and/or
* modify it under the terms of the GNU General Public License
* version 3 as published by the Free Software Foundation.
*/


#if !defined(__PARAMETERS_H__)
    #define __PARAMETERS_H__
    #include "cli.h"
    

/**
   @brief ih::Parameters struct for listCommands
*/
const PROGMEM ih::Parameters listCommands_param[1] = 
{
    listCommands, // function pointer
    ih::no_wildcards, // wildcard flag
    "listCommands", // command string
    12, // command string num characters
    0, // parent id
    0, // this command id (tree unique)
    0, // command depth
    0, // number of subcommands
    ih::UI_ARG_HANDLING::no_args, // argument handling
    0, // minimum expected number of arguments
    0, // maximum expected number of arguments
    /* UITYPE arguments */
    {ih::UITYPE::NO_ARGS}    
};
ih::Command listCommands_(listCommands_param); // listCommands_ command constructor

/**
   @brief ih::Parameters struct for listSettings
*/
const PROGMEM ih::Parameters listSettings_param[1] = 
{
    listSettings, // function pointer
    ih::no_wildcards, // wildcard flag
    "listSettings", // command string
    12, // command string num characters
    0, // parent id
    0, // this command id (tree unique)
    0, // command depth
    0, // number of subcommands
    ih::UI_ARG_HANDLING::no_args, // argument handling
    0, // minimum expected number of arguments
    0, // maximum expected number of arguments
    /* UITYPE arguments */
    {ih::UITYPE::NO_ARGS}    
};
ih::Command listSettings_(listSettings_param); // listSettings_ command constructor

#endif

// end of file
