/**
   @file advancedGetCommandFromStream.ino
   @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
   @brief An example that uses all of the methods available
   @version 0.1
   @date 2022-03-16

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
    /* username */ "",
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
  Serial.println(F("error."));
}

void uc_nest_one(UserInput* inputProcess)
{
  Serial.println(F("made it to uc_nest_one."));
}

void uc_nest_two(UserInput* inputProcess)
{
  Serial.println(F("made it to uc_nest_two."));
}

const Parameters nested_prms[3] PROGMEM =
{
  { // root command
    uc_unrecognized,      // this is allowed to be NULL, if this is NULL and the terminating subcommand function ptr is also NULL nothing will launch
    "launch",       // command string
    6,            // command string characters
    0,            // command depth
    2,            // subcommands  
    no_arguments, // argument handling
    0,            // minimum expected number of arguments
    0,            // maximum expected number of arguments
    /*
      UITYPE arguments
    */
    {
      UITYPE::NO_ARGS // use NO_ARGS if the function expects no arguments
    }
  },
  { // subcommand depth one
    uc_nest_one,          // unique function
    "one",                // command string
    3,                    // command string characters
    1,                    // command depth
    0,                    // subcommands    
    no_arguments,         // argument handling
    0,                    // minimum expected number of arguments
    0,                    // maximum expected number of arguments
    /*
      UITYPE arguments
    */
    {
      UITYPE::NO_ARGS // use NO_ARGS if the function expects no arguments
    }
  }, 
  { // subcommand depth one
    uc_nest_two,          // unique function
    "two",                // command string
    3,                    // command string characters
    1,                    // command depth
    0,                    // subcommands
    no_arguments,         // argument handling
    0,                    // minimum expected number of arguments
    0,                    // maximum expected number of arguments
    /*
      UITYPE arguments
    */
    {
      UITYPE::NO_ARGS // use NO_ARGS if the function expects no arguments
    }
  }
};
CommandConstructor uc_nested_example_(nested_prms, _N_prms(nested_prms), 2); //  uc_help_ has a command string, and function specified

void setup()
{
  delay(500); // startup delay for reprogramming
  Serial.begin(115200); //  set up Serial object (Stream object)
  while (!Serial); //  wait for user

  Serial.println(F("Set up InputHandler..."));
  inputHandler.DefaultFunction(uc_unrecognized); // set default function, called when user input has no match or is not valid  
  inputHandler.AddCommand(uc_nested_example_);   // nested commands example
  inputHandler.ListCommands();
  inputHandler.OutputToStream(Serial); // class output  
}

void loop()
{
  inputHandler.GetCommandFromStream(Serial); //  read commands from a stream, hardware or software should work
  inputHandler.OutputToStream(Serial); // class output
}
