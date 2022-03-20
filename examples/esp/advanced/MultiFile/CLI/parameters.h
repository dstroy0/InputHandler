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
 * @brief Parameters struct for uc_help_
 * 
 */
const Parameters help_param[1] PROGMEM =
{ // func ptr
  uc_help,      // this is allowed to be NULL, if this is NULL and the terminating subcommand function ptr is also NULL nothing will launch (error)
  "help",       // command string
  4,            // command string characters
  0,            // command depth
  0,            // subcommands
  UI_ARG_HANDLING::no_args,      // argument handling
  0,            // minimum expected number of arguments
  0,            // maximum expected number of arguments
  /*
    UITYPE arguments
  */
  {
    UITYPE::NO_ARGS // use NO_ARGS if the function expects no arguments
  }
};
CommandConstructor uc_help_(help_param); //  uc_help_ has a command string, and function specified

/**
 * @brief Parameters struct for uc_settings_
 * 
 */
const Parameters settings_param[1] PROGMEM =
{
  uc_settings,      // function ptr
  "inputSettings",  // command string
  13,               // command string characters
  0,                // command depth
  0,                // subcommands
  UI_ARG_HANDLING::no_args,          // argument handling
  0,                // minimum expected number of arguments
  0,                // maximum expected number of arguments
  /*
    UITYPE arguments
  */
  {
    UITYPE::NO_ARGS // use NO_ARGS if the function expects no arguments
  }
};
CommandConstructor uc_settings_(settings_param); // uc_settings_ has a command string, and function specified

/**
 * @brief Parameters struct for uc_test_
 * 
 */
const Parameters type_test_param[1] PROGMEM = {
  uc_test_input_types, // function ptr
  "test",              // command string
  4,                   // string length
  0,                   // command depth
  0,                   // subcommands
  UI_ARG_HANDLING::type_arr,            // argument handling
  8,                   // minimum expected number of arguments
  8,                   // maximum expected number of arguments
  /*
    UITYPE arguments
  */
  {
    UITYPE::UINT8_T,    // 8-bit  uint
    UITYPE::UINT16_T,   // 16-bit uint
    UITYPE::UINT32_T,   // 32-bit uint
    UITYPE::INT16_T,    // 16-bit int
    UITYPE::FLOAT,      // 32-bit float
    UITYPE::CHAR,       // char
    UITYPE::C_STRING,   // c-string, pass without quotes if there are no spaces, or pass with quotes if there are
    UITYPE::NOTYPE      // special type, no type validation performed
  }
};
CommandConstructor uc_test_(type_test_param);

#endif