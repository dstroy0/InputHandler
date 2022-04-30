/**
   @file cli_setup.h
   @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
   @brief setup example for MultiFile.ino
   @version 0.9
   @date 2022-03-20

   @copyright Copyright (c) 2022
*/

#if !defined(__CLI_SETUP__)
    #define __CLI_SETUP__

    #include <InputHandler.h>
    #include "functions.h"
    #include "parameters.h"

/*
  this output buffer is formatted by UserInput's methods
  you have to empty it out yourself with
  OutputToStream()
*/
char output_buffer[650] = {'\0'}; //  output buffer

const PROGMEM IH_pname pname = "_test_";   ///< default process name
const PROGMEM IH_eol peol = "\r\n";        ///< default process eol characters
const PROGMEM IH_input_cc pinputcc = "##"; ///< default input control character sequence
const PROGMEM IH_wcc pwcc = "*";

const PROGMEM InputProcessDelimiterSequences pdelimseq = {
    2,         ///< number of delimiter sequences
    {1, 1},    ///< delimiter sequence lens
    {" ", ","} ///< delimiter sequences
};

const PROGMEM InputProcessStartStopSequences pststpseq = {
    1,           ///< num start stop sequence pairs
    {1, 1},      ///< start stop sequence lens
    {"\"", "\""} ///< start stop sequence pairs
};

const PROGMEM InputProcessParameters input_prm[1] = {
    &pname,
    &peol,
    &pinputcc,
    &pwcc,
    &pdelimseq,
    &pststpseq};
UserInput inputHandler(output_buffer, buffsz(output_buffer), input_prm);

void InputHandler_setup()
{
    Serial.println(F("Set up InputHandler..."));
    inputHandler.defaultFunction(unrecognized); // set default function, called when user input has no match or is not valid
    inputHandler.addCommand(help_);             // lists commands available to the user    
    inputHandler.addCommand(test_);             // input type test
    inputHandler.begin();                          // required.  returns true on success.
    inputHandler.listCommands();                   // formats output_buffer with the command list
    inputHandler.outputToStream(Serial);           // class output
}

#endif