/**
   @file Parameters.h
   @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
   @brief Parameters and CommandConstructor objects for MultiFile.ino
   @version 0.9
   @date 2022-03-20

   @copyright Copyright (c) 2022
*/

#if !defined(__CLI_PARAMETERS__)
    #define __CLI_PARAMETERS__

    #include "cli_setup.h"

/**
   @brief CommandParameters struct for help_

*/
const PROGMEM ih::Parameters help_param[1] = {
    help, // this is allowed to be NULL, if this is NULL and the terminating subcommand function ptr is also NULL nothing will launch (error)
    ih::WC_FLAG::no_wildcards, // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
    "help", // command string
    4, // command string characters
    ih::CMD_ID::root, // parent id
    ih::CMD_ID::root, // this command id
    ih::CMD_ID::root, // command depth
    0, // subcommands
    ih::UI_ARG_HANDLING::no_args, // argument handling
    0, // minimum expected number of arguments
    0, // maximum expected number of arguments
    /* UITYPE arguments */
    {ih::UITYPE::NO_ARGS} // use NO_ARGS if the function expects no arguments
};
ih::Command help_(help_param); //  help has a command string, and function specified

/**
   @brief CommandParameters struct for test_

*/
const PROGMEM ih::Parameters type_test_param[1] = {test_input_types, // function ptr
    ih::WC_FLAG::no_wildcards, // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
    "test", // command string
    4, // string length
    ih::CMD_ID::root, // parent id
    ih::CMD_ID::root, // this command id
    ih::CMD_ID::root, // command depth
    0, // subcommands
    ih::UI_ARG_HANDLING::type_arr, // argument handling
    8, // minimum expected number of arguments
    8, // maximum expected number of arguments
    /* UITYPE arguments */
    {
        ih::UITYPE::UINT8_T, // 8-bit  uint
        ih::UITYPE::UINT16_T, // 16-bit uint
        ih::UITYPE::UINT32_T, // 32-bit uint
        ih::UITYPE::INT16_T, // 16-bit int
        ih::UITYPE::FLOAT, // 32-bit float
        ih::UITYPE::CHAR, // char
        ih::UITYPE::START_STOP, // regex-like start stop char sequences
        ih::UITYPE::NOTYPE // special type, no type validation performed
    }};
ih::Command test_(type_test_param);

#endif