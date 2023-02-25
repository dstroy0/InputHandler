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
  this output buffer is formatted by Input's methods
*/
char output_buffer[64] = {'\0'}; //  output buffer

// default constructor with output
const ih::InputParameters* defaultConstructor = NULL;
ih::Input inputHandler(defaultConstructor, output_buffer, buffsz(output_buffer));

/*
   default function, called if nothing matches or if there is an error
*/
void unrecognized(ih::Input* inputProcess)
{
    // error output
    inputProcess->outputToStream(Serial);
    Serial.println(F("error."));
}

void nest_one(ih::Input* inputProcess)
{
    inputHandler.outputToStream(Serial); // class output
    Serial.println(F("made it to nest_one."));
}

void nest_two(ih::Input* inputProcess)
{
    inputHandler.outputToStream(Serial); // class output
    Serial.println(F("made it to nest_two."));
}

const PROGMEM ih::Parameters nest_one_[1] = {
    // subcommand depth one
    nest_one,     // unique function
    ih::WC_FLAG::no_wildcards, // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
    "one",        // command string
    3,            // command string characters
    ih::CMD_ID::root,         // parent id
    1,            // this command id
    1,            // command depth
    0,            // subcommands
    ih::UI_ARG_HANDLING::no_args, // argument handling
    0,                        // minimum expected number of arguments
    0,                        // maximum expected number of arguments
    /* UITYPE arguments */
    {ih::UITYPE::NO_ARGS} // use NO_ARGS if the function expects no arguments
};

const PROGMEM ih::Parameters nest_two_[1] = {
    // subcommand depth one
    nest_two,     // unique function
    ih::WC_FLAG::no_wildcards, // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
    "two",        // command string
    3,            // command string characters
    ih::CMD_ID::root,         // parent id
    2,            // this command id
    1,            // command depth
    0,            // subcommands
    ih::UI_ARG_HANDLING::no_args, // argument handling
    0,                        // minimum expected number of arguments
    0,                        // maximum expected number of arguments
    /* UITYPE arguments */
    {ih::UITYPE::NO_ARGS} // use NO_ARGS if the function expects no arguments
};

const PROGMEM ih::Parameters nested_prms[1 /* root */ + 2 /* child(ren) */] = {
    {
        // root command
        unrecognized, // root command not allowed to be NULL
        ih::WC_FLAG::no_wildcards, // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
        "launch",     // command string
        6,            // command string characters
        ih::CMD_ID::root,         // parent id
        ih::CMD_ID::root,         // this command id
        ih::CMD_ID::root,         // command depth
        2,            // subcommands
        ih::UI_ARG_HANDLING::no_args, // argument handling
        0,                        // minimum expected number of arguments
        0,                        // maximum expected number of arguments
        /* UITYPE arguments */
        {ih::UITYPE::NO_ARGS} // use NO_ARGS if the function expects no arguments
    },
    *nest_one_, *nest_two_};
ih::Command nested_example_(nested_prms, nprms(nested_prms), 1);

void setup()
{
    delay(500);           // startup delay for reprogramming
    Serial.begin(115200); //  set up Serial object (Stream object)
    while (!Serial)
        ; //  wait for user

    Serial.println(F("Set up InputHandler..."));
    inputHandler.defaultFunction(
        unrecognized); // set default function, called when user input has no match or is not valid
    inputHandler.addCommand(nested_example_); // nested commands example
    inputHandler.begin();                     // required.  returns true on success.
    inputHandler.listCommands();
    inputHandler.outputToStream(Serial); // class output
}

void loop()
{
    inputHandler.getCommandFromStream(
        Serial); //  read commands from a stream, hardware or software should work
    inputHandler.outputToStream(Serial); // class output
}
