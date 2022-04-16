/**
   @file GetCommandFromStream.ino
   @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
   @brief A basic InputHandler demonstration
   @version 0.9
   @date 2022-04-68

   @copyright Copyright (c) 2022
*/

#include <InputHandler.h>

/*
  UserInput constructor
*/
UserInput inputHandler;

/*
   default function, called if nothing matches or if there is an error
*/
void uc_unrecognized(UserInput *inputProcess)
{
  Serial.println(F("made it to uc_unrecognized"));
}

/*
   test callback function
*/
void uc_hello_(UserInput *inputProcess)
{
  Serial.println(F("hello"));
}

/*
  command parameters
*/
const PROGMEM CommandParameters type_test_param[1] =
{
  uc_hello_,                // function name
  no_wildcards,             // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
  "hello",                  // command string
  5,                        // string length
  root,                     // parent id
  root,                     // this command id
  root,                     // command depth
  0,                        // subcommands
  UI_ARG_HANDLING::no_args, // argument handling
  0,                        // minimum expected number of arguments
  0,                        // maximum expected number of arguments
  /* UITYPE arguments */
  { UITYPE::NO_ARGS }
};
CommandConstructor uc_test_(type_test_param);

void setup()
{
  delay(500);           // startup delay for reprogramming (prevents restart)
  Serial.begin(115200); //  set up Serial
  while (!Serial)
    ; //  wait for user

  inputHandler.defaultFunction(uc_unrecognized); // set default function, called when user input has no match or is not valid
  inputHandler.addCommand(uc_test_);             // input type test
  if (inputHandler.begin())                      // required.  returns true on success.
  {
    Serial.println(F("enter <hello> to test."));
  }
  else
  {
    Serial.println(F("there was an error, please enable output for more verbose error information"));
  }
}

void loop()
{
  inputHandler.getCommandFromStream(Serial); //  read commands from a stream, hardware or software serial should work
}
