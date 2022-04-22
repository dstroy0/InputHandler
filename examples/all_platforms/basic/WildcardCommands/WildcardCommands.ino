/**
   @file WildcardCommands.ino
   @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
   @brief An example that demonstrates wildcard commands
   @version 1.0
   @date 2022-04-22

   @copyright Copyright (c) 2022
*/

#include <InputHandler.h>

/*
  this output buffer is formatted by UserInput's methods
*/
char output_buffer[650] = {'\0'}; //  output buffer

/*
    default constructor with output, default wildcard char is asterisk '*'
*/
UserInput inputHandler(output_buffer, buffsz(output_buffer));

/*
   default function, called if nothing matches or if there is an error
*/
void unrecognized(UserInput* inputProcess)
{
  // error output
  inputProcess->outputToStream(Serial);
}

/*
   lists the settings passed to UserInput's constructor, or default parameters
*/
void settings(UserInput* inputProcess)
{
  inputProcess->listSettings(inputProcess);
}

/*
   lists commands available to the user
*/
void help(UserInput* inputProcess)
{
  inputProcess->listCommands();
}

/*
   test all available input types
*/
void test_input_types(UserInput* inputProcess)
{
  inputProcess->outputToStream(Serial);                                             // class output, doesn't have to output to the input stream
  char* str_ptr = inputProcess->nextArgument();                                     //  init str_ptr and point it at the next argument input by the user
  char* strtoul_ptr = 0;                                                            //  this is for strtoul
  uint32_t strtoul_result = strtoul(str_ptr, &strtoul_ptr, 10);                     // get the result in base10
  uint8_t eight_bit = (strtoul_result <= UINT8_MAX) ? (uint8_t)strtoul_result : 0U; // if the result is less than UINT8_MAX then set eight_bit, else eight_bit = 0

  str_ptr = inputProcess->nextArgument();
  strtoul_ptr = 0;
  strtoul_result = strtoul(str_ptr, &strtoul_ptr, 10);
  uint16_t sixteen_bit = (strtoul_result <= UINT16_MAX) ? (uint16_t)strtoul_result : 0U;

  str_ptr = inputProcess->nextArgument();
  strtoul_ptr = 0;
  uint32_t thirtytwo_bit = strtoul(str_ptr, &strtoul_ptr, 10);

  str_ptr = inputProcess->nextArgument();
  int sixteen_bit_int = atoi(str_ptr);

  str_ptr = inputProcess->nextArgument();
  float thirtytwo_bit_float = (float)atof(str_ptr);

  str_ptr = inputProcess->nextArgument();
  char _char = *str_ptr;

  str_ptr = inputProcess->nextArgument();
  char c_string[64] = {'\0'};
  snprintf_P(c_string, 64, PSTR("%s"), str_ptr);

  str_ptr = inputProcess->nextArgument();
  char unknown_string[64] = {'\0'};
  snprintf_P(unknown_string, 64, PSTR("%s"), str_ptr);

  char float_buffer[32] = {'\0'}; //  dtostrf buffer
  char out[512] = {'\0'};         //  function output buffer
  uint16_t string_pos = 0;        // function output buffer index

  /*
       format out[] with all of the arguments received
  */
  string_pos += snprintf_P(out + string_pos, 512,
                           PSTR("Test user input types:\n"
                                " uint8_t %u\n"
                                " uint16_t %u\n"
                                " uint32_t %lu\n"
                                " int %d\n"
                                " float %s\n"
                                " char %c\n"
                                " c-string %s\n"
                                " unknown-type %s\n"),
                           eight_bit,
                           sixteen_bit,
                           thirtytwo_bit,
                           sixteen_bit_int,
                           dtostrf(thirtytwo_bit_float, 2, 3, float_buffer),
                           _char,
                           c_string,
                           unknown_string);

  Serial.println(out);
}

/**
   @brief CommandParameters struct for help_

*/
const PROGMEM CommandParameters help_param[1] = {
  help,                     // this is allowed to be NULL, if this is NULL and the terminating subcommand function ptr is also NULL nothing will launch (error)
  has_wildcards,            // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
  "****",                   // command string
  4,                        // command string characters
  root,                     // parent id
  root,                     // this command id
  root,                     // command depth
  0,                        // subcommands
  UI_ARG_HANDLING::no_args, // argument handling
  0,                        // minimum expected number of arguments
  0,                        // maximum expected number of arguments
  /*
    UITYPE arguments
  */
  {
    UITYPE::NO_ARGS // use NO_ARGS if the function expects no arguments
  }
};
CommandConstructor help_(help_param); //  help_ has a command string, and function specified

/**
   @brief CommandParameters struct for settings_

*/
const PROGMEM CommandParameters settings_param[1] = {
  settings,              // function ptr
  no_wildcards,             // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
  "inputSettings",          // command string
  13,                       // command string characters
  root,                     // parent id
  root,                     // this command id
  root,                     // command depth
  0,                        // subcommands
  UI_ARG_HANDLING::no_args, // argument handling
  0,                        // minimum expected number of arguments
  0,                        // maximum expected number of arguments
  /*
    UITYPE arguments
  */
  {
    UITYPE::NO_ARGS // use NO_ARGS if the function expects no arguments
  }
};
CommandConstructor settings_(settings_param); // settings_ has a command string, and function specified

/**
   @brief CommandParameters struct for test_

*/
const PROGMEM CommandParameters type_test_param[1] = {
  test_input_types,       // function ptr
  has_wildcards,              // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
  "***t",                    // command string
  4,                         // string length
  root,                      // parent id
  root,                      // this command id
  root,                      // command depth
  0,                         // subcommands
  UI_ARG_HANDLING::type_arr, // argument handling
  8,                         // minimum expected number of arguments
  8,                         // maximum expected number of arguments
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
    UITYPE::START_STOP, // regex-like start stop char sequences
    UITYPE::NOTYPE      // special type, no type validation performed
  }
};
CommandConstructor test_(type_test_param);

void setup()
{
  delay(500); // startup delay for reprogramming
  Serial.begin(115200); //  set up Serial object (Stream object)
  while (!Serial)
    ; //  wait for user

  Serial.println(F("Set up InputHandler..."));
  inputHandler.defaultFunction(unrecognized); // set default function, called when user input has no match or is not valid
  // help is an all wildcard command
  // if the input command is the same strlen as the command string in "help"
  // it will try to launch the function if there are NO OTHER matches
  // wildcard matches have a LOWER priority than a regular match
  // wildcard matches are handled on a FIRST MATCH basis
  // this means that only the first wildcard match will be acted upon
  // and ONLY if there were no other match hits
  // this also means that you cannot have ANY other ALL wildcard commands that are four char
  // in length, whichever one is scanned first by UserInput will match, and the other
  // command will NEVER BE REACHED.
  inputHandler.addCommand(help_);             // lists commands available to the user
  // settings does not contain any wildcard char
  inputHandler.addCommand(settings_);         // lists UserInput class settings
  // test is only looking for a 't' in the 4th position because the command string
  // is "***t" which means its memcmp range will be one char wide starting at the 
  // 4th position
  inputHandler.addCommand(test_);             // input type test
  inputHandler.begin();                          // required.  returns true on success.

  inputHandler.listSettings(&inputHandler);
  inputHandler.outputToStream(Serial); // class output

  inputHandler.listCommands();         // formats output_buffer with the command list
  inputHandler.outputToStream(Serial); // class output
}

void loop()
{
  inputHandler.getCommandFromStream(Serial); //  read commands from a stream, hardware or software should work
  inputHandler.outputToStream(Serial); // class output
}
