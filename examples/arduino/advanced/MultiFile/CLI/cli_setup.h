/**
   @file cli_setup.h
   @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
   @brief setup example for MultiFile.ino
   @version 0.9
   @date 2022-03-20

   @copyright Copyright (c) 2022
*/

#if !defined(__CLI_SETUP__)
#define __CLI_SETUP__

#include <InputHandler.h>
#include "functions.h"
#include "parameters.h"

/*
  this output buffer is formatted by UserInput's methods
  you have to empty it out yourself with
  OutputToStream()
*/
char output_buffer[512] = {'\0'}; //  output buffer

/*
  UserInput constructor one
*/
UserInput inputHandler(/* UserInput's output buffer */ output_buffer,
    /* size of UserInput's output buffer */ buffSZ(output_buffer),
    /* username */ "",
    /* end of line characters */ "\r\n",
    /* token delimiter */ " ",
    /* c-string delimiter */ "\"");

/*
  UserInput constructor two
  you can share one output buffer
*/
//UserInput sensorParser(/* UserInput's output buffer */ output_buffer,
//    /* size of UserInput's output buffer */ buffSZ(output_buffer),
//    /* username */ "sensor parser",
//    /* end of line characters */ "arbitrary",
//    /* token delimiter */ ",",
//    /* c-string delimiter */ "^");

void InputHandler_setup()
{
  Serial.println(F("Set up InputHandler..."));
  inputHandler.defaultFunction(uc_unrecognized); // set default function, called when user input has no match or is not valid
  inputHandler.addCommand(uc_help_);             // lists commands available to the user
  inputHandler.addCommand(uc_settings_);         // lists UserInput class settings
  inputHandler.addCommand(uc_test_);             // input type test
  inputHandler.begin();                          // required.  returns true on success.
  inputHandler.listCommands();               // formats output_buffer with the command list
  inputHandler.outputToStream(Serial); // class output
}

#endif