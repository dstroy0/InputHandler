/**
   @file GetCommandFromStream.ino
   @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
   @brief A basic InputHandler demonstration
   @version 1.0
   @date 2023/2/24

   @copyright Copyright (c) 2022
*/

#include <InputHandler.h>
using namespace ih; // InputHandler's namespace
/*
  Input constructor; default constructor with no class output
*/
Input inputHandler;

/*
   default function, called if nothing matches or if there is an error
*/
void unrecognized(Input* inputProcess) { Serial.println(F("made it to unrecognized")); }

/*
   test callback function
*/
void hello(Input* inputProcess) { Serial.println(F("hello")); }

/*
  command parameters
*/
const PROGMEM Parameters test_param[1] = {hello, // function name
    no_wildcards, // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
    "hello", // command string
    5, // string length
    root, // parent id
    root, // this command id
    root, // command depth
    0, // subcommands
    UI_ARG_HANDLING::no_args, // argument handling
    0, // minimum expected number of arguments
    0, // maximum expected number of arguments
    /* UITYPE arguments */
    {UITYPE::NO_ARGS}};
Command test(test_param);

void setup()
{
    delay(500); // startup delay for reprogramming (prevents restart)
    Serial.begin(115200); //  set up Serial
    while (!Serial)
        ; //  wait for user

    inputHandler.defaultFunction(unrecognized); // set default function, called when user input has no match or is not valid
    inputHandler.addCommand(test); // input type test
    if (inputHandler.begin()) // required.  returns true on success.
    {
        Serial.println(F("enter <hello> to test."));
    }
    else
    {
        Serial.println(F("there was an error starting InputHandler, please enable output for more "
                         "verbose error information"));
    }
}

void loop()
{
    inputHandler.getCommandFromStream(Serial); //  read commands from a stream, hardware or software serial should work
}
