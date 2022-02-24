/**
   @file advancedGetCommandFromStream.ino
   @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
   @brief An example that uses all of the methods available
   @version 0.1
   @date 2022-02-17

   @copyright Copyright (c) 2022
*/

#include <InputHandler.h>

char output_buffer[512] = {'\0'}; //  output buffer
UserInput inputHandler(output_buffer, 512, _default_username);

/*
   default function, called if nothing matches or if there is an error
*/
void uc_unrecognized(UserInput *inputProcess)
{
  inputProcess->OutputToStream(Serial);
  Serial.println(F("made it to uc_unrecognized"));
}

/*
   lists the settings passed to UserInput's constructor, or default parameters
*/
void uc_settings(UserInput *inputProcess)
{
  inputProcess->ListUserInputSettings(inputProcess);
}

/*
   lists commands available to the user
*/
void uc_help(UserInput *inputProcess)
{
  inputProcess->ListUserCommands();
}

/*
   test all available input types
*/
void uc_test_input_types(UserInput *inputProcess)
{
  char *str_ptr = inputProcess->NextArgument();                                     //  init str_ptr and point it at the next argument input by the user
  char *strtoul_ptr = 0;                                                            //  this is for strtoul
  uint32_t strtoul_result = strtoul(str_ptr, &strtoul_ptr, 10);                     // get the result in base10
  uint8_t eight_bit = (strtoul_result <= UINT8_MAX) ? (uint8_t)strtoul_result : 0U; // if the result is less than UINT8_MAX then set eight_bit, else eight_bit = 0

  str_ptr = inputProcess->NextArgument();
  strtoul_ptr = 0;
  strtoul_result = strtoul(str_ptr, &strtoul_ptr, 10);
  uint16_t sixteen_bit = (strtoul_result <= UINT16_MAX) ? (uint16_t)strtoul_result : 0U;

  str_ptr = inputProcess->NextArgument();
  strtoul_ptr = 0;
  uint32_t thirtytwo_bit = strtoul(str_ptr, &strtoul_ptr, 10);

  str_ptr = inputProcess->NextArgument();
  int sixteen_bit_int = atoi(str_ptr);

  str_ptr = inputProcess->NextArgument();
  float thirtytwo_bit_float = (float)atof(str_ptr);

  str_ptr = inputProcess->NextArgument();
  char _char = *str_ptr;

  str_ptr = inputProcess->NextArgument();
  char c_string[64] = {'\0'};
  snprintf_P(c_string, 64, PSTR("%s"), str_ptr);

  char float_buffer[32] = {'\0'}; //  dtostrf buffer
  char out[128] = {'\0'};         //  function output buffer
  uint16_t string_pos = 0;        // function output buffer index

  /*
       format out[] with all of the arguments received
  */
  string_pos += snprintf_P(out + string_pos, 128,
                           PSTR("Test user input types:\n"
                                "uint8_t %u\nuint16_t %u\nuint32_t %lu\nint %d\nfloat %s\nchar %c\nc-string %s\n"),
                           eight_bit,
                           sixteen_bit,
                           thirtytwo_bit,
                           sixteen_bit_int,
                           dtostrf(thirtytwo_bit_float, 2, 3, float_buffer),
                           _char,
                           c_string);
  Serial.print(out);
}

/*
   UserInput UserCallbackFunctionParameters
   These objects are what you use to specify the command string, function to launch, and types of input if any

   The command string is stored in PROGMEM if applicable

   The following are the available input types
   _UITYPE::UINT8_T == an eight bit unsigned integer
   _UITYPE::UINT16_T == a sixteen bit unsigned integer
   _UITYPE::UINT32_T == a thirty-two bit unsigned integer
   _UITYPE::INT16_T == a sixteen bit signed integer
   _UITYPE::FLOAT == a thirty-two bit signed floating point number
   _UITYPE::CHAR == a character value
   _UITYPE::C_STRING == a string of character values, absent of '\0' and enclosed with single quotation marks "c-string"
                               depending on the method used, if it is ReadCommand then very long c-strings can be sent and read
                               using GetCommandFromStream input c-string length is limited by input_buffer size
*/
UserCallbackFunctionParameters uc_help_("help", uc_help);                   //  uc_help_ has a command string, and function specified
UserCallbackFunctionParameters uc_settings_("inputSettings", uc_settings); // uc_settings_ has a command string, and function specified
// this command will accept seven arguments of the type specified, in order, it will not run the function unless all arguments are valid
const _UITYPE uc_test_arguments[] PROGMEM = {_UITYPE::UINT8_T,
                                             _UITYPE::UINT16_T,
                                             _UITYPE::UINT32_T,
                                             _UITYPE::INT16_T,
                                             _UITYPE::FLOAT,
                                             _UITYPE::CHAR,
                                             _UITYPE::C_STRING
                                            };
UserCallbackFunctionParameters uc_test_("test", uc_test_input_types, 7, uc_test_arguments);

void setup()
{
  Serial.begin(115200); //  set up Serial

  inputHandler.SetDefaultHandler(uc_unrecognized); // set default function, called when user input has no match or is not valid
  inputHandler.AddUserCommand(uc_help_);          // lists commands available to the user
  inputHandler.AddUserCommand(uc_settings_);      // lists UserInput class settings
  inputHandler.AddUserCommand(uc_test_);          // input type test
  inputHandler.ListUserCommands();                 //  lists commands available to the user
}

void loop()
{
  //  inputHandler.ReadCommand(data, len);  // read commands from a char buffer
  // inputHandler.GetCommandFromStream(Serial2);  // read commands from as many streams as you like using the same object
  inputHandler.GetCommandFromStream(Serial); //  read commands from a stream, hardware or software should work
  inputHandler.OutputToStream(Serial);  // class output, doesn't have to output to the input stream
}