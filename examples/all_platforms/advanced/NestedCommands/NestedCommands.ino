/**
   @file NestedCommands.ino
   @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
   @brief An example that demonstrates nested subcommands
   @version 1.0
   @date 2022-04-17

   @copyright Copyright (c) 2022
*/

#include <InputHandler.h>

/*
  this output buffer is formatted by UserInput's methods
*/
char output_buffer[64] = {'\0'}; //  output buffer

// default constructor with output
UserInput inputHandler(output_buffer, buffsz(output_buffer));

/*
   default function, called if nothing matches or if there is an error
*/
void uc_unrecognized(UserInput *inputProcess)
{
  // error output
  inputProcess->outputToStream(Serial);
  Serial.println(F("error."));
}

void uc_nest_one(UserInput *inputProcess)
{
  inputHandler.outputToStream(Serial); // class output
  Serial.println(F("made it to uc_nest_one."));
}

void uc_nest_two(UserInput *inputProcess)
{
  inputHandler.outputToStream(Serial); // class output
  Serial.println(F("made it to uc_nest_two."));
}

const PROGMEM CommandParameters nested_prms[3] =
{
  { // root command
    uc_unrecognized,          // root command not allowed to be NULL
    no_wildcards,             // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
    "launch",                 // command string
    6,                        // command string characters
    root,                     // parent id
    root,                     // this command id
    root,                     // command depth
    2,                        // subcommands
    UI_ARG_HANDLING::no_args, // argument handling
    0,                        // minimum expected number of arguments
    0,                        // maximum expected number of arguments
    /*
      UITYPE arguments
    */
    {
      UITYPE::NO_ARGS // use NO_ARGS if the function expects no arguments
    }
  },
  { // subcommand depth one
    uc_nest_one,              // unique function
    no_wildcards,             // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
    "one",                    // command string
    3,                        // command string characters
    root,                     // parent id
    1,                        // this command id
    1,                        // command depth
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
  },
  { // subcommand depth one
    uc_nest_two,              // unique function
    no_wildcards,             // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
    "two",                    // command string
    3,                        // command string characters
    root,                     // parent id
    2,                        // this command id
    1,                        // command depth
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
  }
};
CommandConstructor uc_nested_example_(nested_prms, nprms(nested_prms), 1); //  uc_help_ has a command string, and function specified

void setup()
{
  delay(500);           // startup delay for reprogramming
  Serial.begin(115200); //  set up Serial object (Stream object)
  while (!Serial)
    ; //  wait for user

  Serial.println(F("Set up InputHandler..."));
  inputHandler.defaultFunction(uc_unrecognized); // set default function, called when user input has no match or is not valid
  inputHandler.addCommand(uc_nested_example_);   // nested commands example
  inputHandler.begin();                          // required.  returns true on success.
  inputHandler.listCommands();
  inputHandler.outputToStream(Serial); // class output
}

void loop()
{
  inputHandler.getCommandFromStream(Serial); //  read commands from a stream, hardware or software should work
  inputHandler.outputToStream(Serial);       // class output
}
