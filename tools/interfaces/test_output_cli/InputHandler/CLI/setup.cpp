/* Generated by InputHandler's /InputHandler/cli_gen_tool/cli_gen_tool.py version 1.0 */
/**
* @file setup.cpp
* @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
* @brief InputHandler autogenerated setup.cpp
* @version 1.0
* @date 2022-12-21
*
* @copyright Copyright (c) 2022
*/
/*
* Copyright (c) 2022 Douglas Quigg (dstroy0) <dquigg123@gmail.com>
* This program is free software; you can redistribute it and/or
* modify it under the terms of the GNU General Public License
* version 3 as published by the Free Software Foundation.
*/


#include setup.h


void InputHandler_setup()
{
  Serial.println(F("Setting up InputHandler..."));
  inputHandler.defaultFunction(unrecognized); // default function is called when user input has no match or is not valid
  inputHandler.addCommand(listCommands_);
  inputHandler.addCommand(listSettings_);
  inputHandler.begin(); // Required. Returns true on success.
}

void InputHandler_loop()
{
  inputHandler.outputToStream(Serial); // class output
}


#endif

// end of file
