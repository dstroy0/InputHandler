/* Generated by cli_gen_tool version <1.0>; using InputHandler version <0.9a> */
/**
* @file CLI.h
* @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
* @brief InputHandler autogenerated CLI.h
* @version 1.0
* @date 2023-02-23
*
* @copyright Copyright (c) 2023
*/
/*
* Copyright (c) 2023 Douglas Quigg (dstroy0) <dquigg123@gmail.com>
*
* License: GNU GPL3
* This program is free software; you can redistribute it and/or
* modify it under the terms of the GNU General Public License
* version 3 as published by the Free Software Foundation.
*/


#if !defined(__CLI_SETUP__)
    #define __CLI_SETUP__
    #include "InputHandler.h"
    #include "InputHandler.cpp"
    #include "functions.h"
    #include "parameters.h"
    
using namespace InputHandler;
using namespace ih_t;

char InputHandler_output_buffer[1000] = {'\0'}; // output buffer size

const PROGMEM ProcessName pname = ""; // process name
const PROGMEM EndOfLineChar peol = "\r\n"; // process end of line characters
const PROGMEM ControlCharSeq pinputcc = "##"; // input control char sequence
const PROGMEM WildcardChar pwcc = "*"; // process wildcard char

// data delimiter sequences
const PROGMEM DelimiterSequences pdelimseq = {
    2, // number of delimiter sequences
    {0, 1}, // delimiter sequence lens
    {" ", ","} // delimiter sequences
};

// start stop data delimiter sequences
const PROGMEM StartStopSequences pststpseq = {
    1, // num start stop sequence pairs
    {1, 1}, // start stop sequence lens
    {"\"", "\""} // start stop sequence pairs
};

const PROGMEM InputParameters input_prm[1] = {
    &pname,
    &peol,
    &pinputcc,
    &pwcc,
    &pdelimseq,
    &pststpseq};

// constructor
UserInput inputHandler(input_prm, InputHandler_output_buffer, buffsz(InputHandler_output_buffer));

void InputHandler_setup()
{
  Serial.println(F("Setting up InputHandler..."));
  inputHandler.defaultFunction(unrecognized); // default function is called when user input has no match or is not valid
  inputHandler.addCommand(listCommands_);
  inputHandler.addCommand(listSettings_);
  inputHandler.addCommand(test_2_);
  inputHandler.begin(); // Required. Returns true on success.
  Serial.println(F("InputHandler setup complete."));
  inputHandler.listSettings(&inputHandler); // prints InputHandler settings
  inputHandler.listCommands(); // prints commands available to user
}

void InputHandler_loop()
{
  inputHandler.getCommandFromStream(Serial); // parse input
  inputHandler.outputToStream(Serial); // class output
}


#endif
// end of file
