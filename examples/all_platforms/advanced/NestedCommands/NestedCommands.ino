/**
   @file NestedCommands.ino
   @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
   @brief An example that demonstrates subcommands
   @version 0.9
   @date 2022-03-18

   @copyright Copyright (c) 2022
*/

#include <InputHandler.h>

/*
  this output buffer is formatted by UserInput's methods
  you have to empty it out yourself with
  OutputToStream()
*/
char output_buffer[650] = {'\0'}; //  output buffer

const PROGMEM IH_pname pname = "_test_";         ///< default process name
const PROGMEM IH_eol peol = "\r\n";        ///< default process eol characters
const PROGMEM IH_input_cc pinputcc = "##"; ///< default input control character sequence
const PROGMEM IH_wcc pwcc = "*"; 

const PROGMEM InputProcessDelimiterSequences pdelimseq = {
  2,         ///< number of delimiter sequences
  {1, 1},    ///< delimiter sequence lens
  {" ", ","} ///< delimiter sequences
};

const PROGMEM InputProcessStartStopSequences pststpseq = {
  1,           ///< num start stop sequence pairs
  {1, 1},      ///< start stop sequence lens
  {"\"", "\""} ///< start stop sequence pairs
};

const PROGMEM InputProcessParameters input_prm[1] = {
  &pname,
  &peol,
  &pinputcc,
  &pwcc,
  &pdelimseq,
  &pststpseq
};
UserInput inputHandler(output_buffer, buffsz(output_buffer), input_prm);

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
