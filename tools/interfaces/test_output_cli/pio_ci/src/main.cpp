/**
   @file main.cpp
   @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
   @brief to test cli_gen_tool.py output
   @version 0.9
   @date 2023-01-02

   @copyright Copyright (c) 2022
*/

#include "setup.h"

void test(UserInput* _inputHandler)
{
  Serial.println(F("test"));
}

void testa(UserInput* _inputHandler)
{
  // your statements here
  Serial.println(F("testa"));
}

void testb(UserInput* _inputHandler)
{
  // your statements here
  Serial.println(F("testb"));
}

void testc(UserInput* _inputHandler)
{
  // your statements here
  Serial.println(F("testc"));
}

void testbb_return_values(UserInput* _inputHandler)
{
  // your statements here
  Serial.println(F("testbb"));
}

void setup() {
  delay(500); // startup delay for reprogramming
  Serial.begin(115200);
  while (!Serial);
  InputHandler_setup();
}

void loop() {
  InputHandler_loop();
}
