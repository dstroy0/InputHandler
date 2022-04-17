/**
   @file ReadCommandFromBufferWebSerial.ino
   @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
   @brief An example that uses ReadCommandFromBuffer and WebSerial
   @version 0.9
   @date 2022-03-18

   @copyright Copyright (c) 2022
*/

#include <Arduino.h>
#include <WiFi.h>
#include <AsyncTCP.h>
#include <ESPAsyncWebServer.h>
#include <WebSerial.h>
#include <InputHandler.h>

AsyncWebServer server(80);

const char *ssid = "REPLACE_WITH_YOUR_SSID";         // Your WiFi SSID
const char *password = "REPLACE_WITH_YOUR_PASSWORD"; // Your WiFi Password

/*
  this output buffer is formatted by UserInput's methods
  you have to empty it out yourself with
  ClearOutputBuffer()
*/
char output_buffer[512] = {'\0'}; //  output buffer

/*
  UserInput constructor
*/
UserInput inputHandler(output_buffer, buffsz(output_buffer));

/*
   default function, called if nothing matches or if there is an error
*/
void uc_unrecognized(UserInput *inputProcess)
{
  // do your error output here
}
/*
   lists the settings passed to UserInput's constructor, or default parameters
*/
void uc_settings(UserInput *inputProcess)
{
  inputProcess->listSettings(inputProcess);
}

/*
   lists commands available to the user
*/
void uc_help(UserInput *inputProcess)
{
  inputProcess->listCommands();
}

/*
   test all available input types
*/
void uc_test_input_types(UserInput *inputProcess)
{
  inputProcess->outputToStream(Serial);                                             // class output, doesn't have to output to the input stream
  char *str_ptr = inputProcess->nextArgument();                                     //  init str_ptr and point it at the next argument input by the user
  char *strtoul_ptr = 0;                                                            //  this is for strtoul
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
  char out[256] = {'\0'};         //  function output buffer
  uint16_t string_pos = 0;        // function output buffer index

  /*
       format out[] with all of the arguments received
  */
  string_pos += snprintf_P(out + string_pos, 256,
                           PSTR("Test user input types:\n"
                                " uint8_t %lu\n"
                                " uint16_t %lu\n"
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

  memcpy(output_buffer, out, ((sizeof(out) < sizeof(output_buffer)) ? sizeof(out) : sizeof(output_buffer - 1)));
}

/**
   @brief CommandParameters struct for uc_help_

*/
const PROGMEM CommandParameters help_param[1] = {
    uc_help,                  // this is allowed to be NULL, if this is NULL and the terminating subcommand function ptr is also NULL nothing will launch (error)
    no_wildcards,             // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
    "help",                   // command string
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
    }};
CommandConstructor uc_help_(help_param); //  uc_help_ has a command string, and function specified

/**
   @brief CommandParameters struct for uc_settings_

*/
const PROGMEM CommandParameters settings_param[1] = {
    uc_settings,              // function ptr
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
    }};
CommandConstructor uc_settings_(settings_param); // uc_settings_ has a command string, and function specified

/**
   @brief CommandParameters struct for uc_test_

*/
const PROGMEM CommandParameters type_test_param[1] = {
    uc_test_input_types,       // function ptr
    no_wildcards,              // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
    "test",                    // command string
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
    }};
CommandConstructor uc_test_(type_test_param);

void setup_wifi()
{
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
  }
}

//WebSerial callback
void recvMsg(uint8_t *data, size_t len)
{
  //ReadCommandFromBuffer
  inputHandler.readCommandFromBuffer(data, len);
}

void setup()
{
  setup_wifi();

  inputHandler.defaultFunction(uc_unrecognized); // set default function, called when user input has no match or is not valid
  inputHandler.addCommand(uc_help_);             // lists commands available to the user
  inputHandler.addCommand(uc_settings_);         // lists UserInput class settings
  inputHandler.addCommand(uc_test_);             // input type test
  inputHandler.begin();                          // required.  returns true on success.
  inputHandler.listCommands(); // formats output_buffer with the command list

  // WebSerial is accessible at "<IP Address>/webserial" in browser
  WebSerial.begin(&server);       // WebSerial uses an async server object
  WebSerial.msgCallback(recvMsg); //  callback ISR
  server.begin();                 //  start async server
}

void loop()
{
  if (inputHandler.outputIsAvailable())
  {
    WebSerial.println(output_buffer);
    inputHandler.clearOutputBuffer();
  }
}
