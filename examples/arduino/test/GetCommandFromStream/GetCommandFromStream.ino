/**
   @file advancedGetCommandFromStream.ino
   @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
   @brief An example that uses all of the methods available
   @version 0.1
   @date 2022-02-17

   @copyright Copyright (c) 2022
*/

#include <InputHandler.h>

/*
  this output buffer is formatted by UserInput's methods
  you have to empty it out yourself with
  OutputToStream()
*/
char output_buffer[512] = {'\0'}; //  output buffer

/*
  UserInput constructor
*/
UserInput inputHandler(/* UserInput's output buffer */ output_buffer,
    /* size of UserInput's output buffer */ 512,
    /* username */ "user",
    /* end of line characters */ "\r\n",
    /* token delimiter */ " ",
    /* c-string delimiter */ "\"");

/*
   default function, called if nothing matches or if there is an error
*/
void uc_unrecognized(UserInput* inputProcess)
{
  // error output
  inputProcess->OutputToStream(Serial);
}

/*
   lists commands available to the user
*/
void uc_help(UserInput* inputProcess)
{
  inputProcess->ListCommands();
}
void uc_help(UserInput& inputProcess)
{
  inputProcess.ListCommands();
}

/*
   test all available input types
*/
void uc_test_input_types(UserInput* inputProcess)
{
  inputProcess->OutputToStream(Serial);                                             // class output, doesn't have to output to the input stream
  char* str_ptr = inputProcess->NextArgument();                                     //  init str_ptr and point it at the next argument input by the user
  char* strtoul_ptr = 0;                                                            //  this is for strtoul
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

  str_ptr = inputProcess->NextArgument();
  char unknown_string[64] = {'\0'};
  snprintf_P(unknown_string, 64, PSTR("%s"), str_ptr);

  char float_buffer[32] = {'\0'}; //  dtostrf buffer
  char out[164] = {'\0'};         //  function output buffer
  uint16_t string_pos = 0;        // function output buffer index

  /*
       format out[] with all of the arguments received
  */
  string_pos += snprintf_P(out + string_pos, 128,
                           PSTR("Test user input types:\n"
                                "uint8_t %u\n"
                                "uint16_t %u\n"
                                "uint32_t %lu\n"
                                "int %d\n"
                                "float %s\n"
                                "char %c\n"
                                "c-string %s\n"
                                "unknown-string %s\n"
                               ),
                           eight_bit,
                           sixteen_bit,
                           thirtytwo_bit,
                           sixteen_bit_int,
                           dtostrf(thirtytwo_bit_float, 2, 3, float_buffer),
                           _char,
                           c_string,
                           unknown_string);

  Serial.print(out);
}

//struct CommandOptions
//{
//    void (*user_defined_function_to_call)(UserInput *);
//    char command[USER_INPUT_MAX_COMMAND_LENGTH] = {'\0'};
//    uint16_t command_length = 0;
//    uint8_t argument_flag = no_arguments;
//    uint16_t num_args = 0;
//    //uint16_t max_num_args = 0;
//    UITYPE _arg_type[USER_INPUT_MAX_NUMBER_OF_COMMAND_ARGUMENTS] = {UITYPE::_LAST};
//};

const CommandOptions help_opt PROGMEM = { uc_help,
                                          "help",
                                          4,
                                          no_arguments,
                                          0,
{UITYPE::_LAST}
                                        };

UserCommandParameters uc_help_(&help_opt);                  //  uc_help_ has a command string, and function specified

const CommandOptions type_test_opt PROGMEM = { uc_test_input_types,
                                               "test",
                                               4,
                                               argument_type_array,
                                               8,
{ UITYPE::UINT8_T,
  UITYPE::UINT16_T,
  UITYPE::UINT32_T,
  UITYPE::INT16_T,
  UITYPE::FLOAT,
  UITYPE::CHAR,
  UITYPE::C_STRING,
  UITYPE::NOTYPE
}
                                             };
UserCommandParameters uc_test_(&type_test_opt);


void setup()
{
  // uncomment as needed
  Serial.begin(115200); //  set up Serial object (Stream object)

  while (!Serial); //  wait for user

  inputHandler.DefaultFunction(uc_unrecognized); // set default function, called when user input has no match or is not valid
  inputHandler.AddCommand(uc_help_);             // lists commands available to the user
  inputHandler.AddCommand(uc_test_);

  uc_help(inputHandler);               // formats output_buffer with the command list
  inputHandler.OutputToStream(Serial); // class output
}

void loop()
{
  // uncomment as needed
  inputHandler.GetCommandFromStream(Serial); //  read commands from a stream, hardware or software should work

  inputHandler.OutputToStream(Serial); // class output

}
