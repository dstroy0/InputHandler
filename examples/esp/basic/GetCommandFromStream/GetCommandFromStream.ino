/**
   @file GetCommandFromStream.ino
   @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
   @brief A basic UserInput example
   @version 0.1
   @date 2022-02-22

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
void uc_unrecognized(UserInput* inputProcess)
{
  Serial.println(F("made it to uc_unrecognized"));
}

/*
   test callback function
*/
void uc_hello_(UserInput* inputProcess)
{
  Serial.println(F("hello"));
}

/*
  command parameters
*/
const Parameters type_test_param[1] PROGMEM =
{
  uc_hello_,    // function name
  "hello",      // command string
  5,            // string length
  0,            // command depth
  0,            // subcommands
  no_arguments, // argument handling
  0,            // minimum expected number of arguments
  0,            // maximum expected number of arguments
  /*
    UITYPE arguments
  */
  {
    UITYPE::NO_ARGS
  }
};
CommandConstructor uc_test_(type_test_param);

void setup()
{
  delay(500); // startup delay for reprogramming (prevents restart)
  Serial.begin(115200); //  set up Serial
  while (!Serial); //  wait for user

  inputHandler.DefaultFunction(uc_unrecognized); // set default function, called when user input has no match or is not valid
  inputHandler.AddCommand(uc_test_);             // input type test

  Serial.println(F("enter <hello> to test."));
}

void loop()
{
  inputHandler.GetCommandFromStream(Serial); //  read commands from a stream, hardware or software serial should work
}