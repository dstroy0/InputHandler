/**
   @file test_output_cli.ino
   @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
   @brief to test cli_gen_tool.py output
   @version 0.9
   @date 2022-01-04

   @copyright Copyright (c) 2022
*/

#include "CLI/src/CLI.h"
using namespace InputHandler;
void test(UserInput* _inputHandler)
{
  // your statements here
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

void testd(UserInput* _inputHandler)
{
  // your statements here
  Serial.println(F("testd"));
}

void teste(UserInput* _inputHandler)
{
  // your statements here
  Serial.println(F("teste"));
}

void testf(UserInput* _inputHandler)
{
  // your statements here
  Serial.println(F("testf"));
}

void testg(UserInput* _inputHandler)
{
  // your statements here
  Serial.println(F("testg"));
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
