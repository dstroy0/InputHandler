/**
   @file MultiFile.ino
   @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
   @brief An example that demonstrates multiple file setup
   @version 0.9
   @date 2022-03-20

   @copyright Copyright (c) 2022
*/

#include "CLI/cli_setup.h"

void setup()
{
  delay(500); // startup delay for reprogramming

  Serial.begin(115200); //  set up Serial object (Stream object)
  while (!Serial); //  wait for user

  InputHandler_setup(); // CLI/cli_setup.h
}

void loop()
{
  inputHandler.getCommandFromStream(Serial); //  read commands from a stream, hardware or software should work
  inputHandler.outputToStream(Serial); // class output
}
