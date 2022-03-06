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

//struct CommandOptions
//{
//    void (*user_defined_function_to_call)(UserInput *);
//    char command[USER_INPUT_MAX_COMMAND_LENGTH] = {'\0'};
//    uint16_t command_length = 0;    // strlen_P() to get length
//    uint8_t argument_flag = no_arguments;
//    uint16_t min_num_args = 0;
//    uint16_t max_num_args = 0;
//    UITYPE arg_type_single = UITYPE::_LAST;
//    UITYPE _arg_type[USER_INPUT_MAX_NUMBER_OF_COMMAND_ARGUMENTS] = {UITYPE::_LAST};
//};

const CommandOptions opt PROGMEM = { uc_help,
                                     "help",
                                     4,
                                     no_arguments,
                                     0,                                                                      
                                     {UITYPE::_LAST}
                                   };

UserCommandParameters uc_help_(&opt);                  //  uc_help_ has a command string, and function specified


void setup()
{
  // uncomment as needed
  Serial.begin(115200); //  set up Serial object (Stream object)

  while (!Serial); //  wait for user

  inputHandler.DefaultFunction(uc_unrecognized); // set default function, called when user input has no match or is not valid
  inputHandler.AddCommand(uc_help_);             // lists commands available to the user

  uc_help(inputHandler);               // formats output_buffer with the command list
  inputHandler.OutputToStream(Serial); // class output
}

void loop()
{
  // uncomment as needed
  inputHandler.GetCommandFromStream(Serial); //  read commands from a stream, hardware or software should work

  inputHandler.OutputToStream(Serial); // class output

}
