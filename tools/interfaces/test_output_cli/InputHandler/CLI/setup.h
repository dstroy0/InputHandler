/* Generated by InputHandler's /InputHandler/cli_gen_tool/cli_gen_tool.py version 1.0 */
/**
* @file setup.h
* @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
* @brief InputHandler autogenerated setup.h
* @version 1.0
* @date 2022-12-23
*
* @copyright Copyright (c) 2022
*/
/*
* Copyright (c) 2022 Douglas Quigg (dstroy0) <dquigg123@gmail.com>
* This program is free software; you can redistribute it and/or
* modify it under the terms of the GNU General Public License
* version 3 as published by the Free Software Foundation.
*/


#if !defined(__CLI_SETUP__)
    #define __CLI_SETUP__
    #include "InputHandler.h"
    #include "functions.h"
    #include "parameters.h"


char InputHandler_output_buffer[700] = {'\0'}; // output buffer size

const PROGMEM IH_pname pname = ""; // process name
const PROGMEM IH_eol peol = "\r\n"; // process end of line characters
const PROGMEM IH_input_cc pinputcc = "##"; // input control char sequence
const PROGMEM IH_wcc pwcc = "*"; // process wildcard char

// data delimiter sequences
const PROGMEM InputProcessDelimiterSequences pdelimseq = {
    2, // number of delimiter sequences
    {1, 1}, // delimiter sequence lens
    {" ", ","} // delimiter sequences
};

// start stop data delimiter sequences
const PROGMEM InputProcessStartStopSequences pststpseq = {
    1, // num start stop sequence pairs
    {2, 2}, // start stop sequence lens
    {"\"", "\""} // start stop sequence pairs
};

const PROGMEM InputProcessParameters input_prm[1] = {
    &pname,
    &peol,
    &pinputcc,
    &pwcc,
    &pdelimseq,
    &pststpseq};

// constructor
UserInput inputHandler(input_prm, InputHandler_output_buffer, buffsz(InputHandler_output_buffer));

void InputHandler_setup();
void InputHandler_loop();

#include "setup.cpp"
#endif
// end of file
