/**
   @file test_output_cli.ino
   @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
   @brief An example that demonstrates how to retrieve type-valid arguments from a Stream
   @version 0.9
   @date 2022-12-22

   @copyright Copyright (c) 2022
*/

#include "InputHandler/src/InputHandler.h"
#include "InputHandler/CLI/setup.h"

void setup() {
  delay(500); // startup delay for reprogramming
  Serial.begin(115200);
  while(!Serial);
  InputHandler_setup();
}

void loop() {
  InputHandler_loop();
}
