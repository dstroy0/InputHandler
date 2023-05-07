/**
  @file debugging.ino
  @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
  @brief debugging setup
  @version 1.0
  @date 2023/2/24

  @copyright Copyright (c) 2022
*/
/*
  Copyright (c) 2022 Douglas Quigg (dstroy0) <dquigg123@gmail.com>
  This program is free software; you can redistribute it and/or
  modify it under the terms of the GNU General Public License
  version 3 as published by the Free Software Foundation.
*/

/*
    users: switch on debugging functions to explore the information they output
*/
/*
    User Configurable items
*/
#define IH_MAX_COMMANDS_PER_TREE 32
#define IH_MAX_ARGS_PER_COMMAND 32
#define IH_MAX_TREE_DEPTH_PER_COMMAND 32
#define IH_MAX_NUM_CHILD_COMMANDS_PER_ROOT 32
#define IH_MAX_CMD_STR_LEN 32
#define IH_MAX_NUM_PROC_DELIM_SEQ 5
#define IH_MAX_NUM_START_STOP_SEQ 5
#define IH_MAX_PROC_INPUT_LEN 128

// maximum number of memcmp ranges per command
#define IH_MAX_PER_ROOT_MEMCMP_RANGES 5

/*
    PGM len
*/

#define IH_INPUT_TYPE_STRINGS_PGM_LEN 10

// if you edit these, some examples might break and your compiler might yell at you
#define IH_EOL_SEQ_PGM_LEN 5
#define IH_DELIM_SEQ_PGM_LEN 5
#define IH_START_STOP_SEQ_PGM_LEN 5
#define IH_PROCESS_NAME_PGM_LEN 12
#define IH_INPUT_CONTROL_CHAR_SEQ_PGM_LEN 3
#define IH_WCC_SEQ_PGM_LEN 2

/*
    library output
    true == ON; false == OFF
*/
/**
 * @var IH_ECHO_ONLY
 *
 * Enable this option to change the library's output to echo only.
 * It will only echo what was entered and indicate where the input error is.
 */
#define IH_ECHO_ONLY false

/**
 * @var IH_VERBOSE
 *
 * Enable this option to change the library's output to verbose.
 * Puts additional command information in the output buffer.
 */
#define IH_VERBOSE true

/*
    DEBUGGING
    switch these on/off by commenting/uncommenting the #define
*/
/**
 * @var DEBUG_GETCOMMANDFROMSTREAM
 *
 * Enable this option to debug Input::getCommandFromStream
 */
#define DEBUG_GETCOMMANDFROMSTREAM false

/**
 * @var DEBUG_READCOMMANDFROMBUFFER
 *
 * Enable this option to debug Input::readCommandFromBuffer
 */
#define DEBUG_READCOMMANDFROMBUFFER false

/**
 * @var DEBUG_GET_TOKEN
 *
 * Enable this option to debug Input::getToken
 */
#define DEBUG_GET_TOKEN false

/**
 * @var DEBUG_SUBCOMMAND_SEARCH
 *
 * Enable this option to debug Input::launchLogic subcommand search; subcommand search is
 * recursive, uses no local variables and passes a Input::_rcfbprm object by reference to
 * itself.
 */
#define DEBUG_SUBCOMMAND_SEARCH false

/**
 * @var DEBUG_ADDCOMMAND
 *
 * Enable this option to debug Input::addCommand
 */
#define DEBUG_ADDCOMMAND false

/**
 * @var DEBUG_LAUNCH_LOGIC
 *
 * Enable this option to debug Input::launchLogic
 */
#define DEBUG_LAUNCH_LOGIC false

/**
 * @var DEBUG_LAUNCH_FUNCTION
 *
 * Enable this option to debug Input::launchFunction
 */
#define DEBUG_LAUNCH_FUNCTION false

/**
 * @var DEBUG_INCLUDE_FREERAM
 *
 * Enable to debug src/utility/freeRam.h; only applicable if you are using freeRam.
 */
#define DEBUG_INCLUDE_FREERAM true

/*
    OPTIONAL METHODS
*/
// public methods
/**
 * @var DISABLE_listSettings
 *
 * Enable this option to disable Input::listSettings()
 */
#define DISABLE_listSettings false

/**
 * @var DISABLE_listCommands
 *
 * Enable this option to disable Input::listCommands
 */
#define DISABLE_listCommands false

/**
 * @var DISABLE_getCommandFromStream
 *
 * Enable this option to disable Input::getCommandFromStream
 */
#define DISABLE_getCommandFromStream false

/**
 * @var DISABLE_nextArgument
 *
 * Enable this option to disable Input::nextArgument, either this or Input::getArgument
 * are required to retrieve arguments.
 */
#define DISABLE_nextArgument false

/**
 * @var DISABLE_getArgument
 *
 * Enable this option to disable Input::getArgument method, either this or
 * Input::nextArgument need to be enabled to retrieve arguments.
 */
#define DISABLE_getArgument false

/**
 * @var DISABLE_outputIsAvailable
 *
 * Enable this option to disable the output available flag.
 */
#define DISABLE_outputIsAvailable false

/**
 * @var DISABLE_outputIsEnabled
 *
 * Enable this option to disable Input::outputIsEnabled
 */
#define DISABLE_outputIsEnabled false

/**
 * @var DISABLE_outputToStream
 *
 * Enable this option to reduce codesize if you are only using
 * Input::readCommandFromBuffer. Default is false.
 */
#define DISABLE_outputToStream false

/**
 * @var DISABLE_clearOutputBuffer
 *
 * Only disable this method if you have already disabled output.
 * Enable this option to disable Input::clearOutputBuffer()
 * Default is false.
 */
#define DISABLE_clearOutputBuffer false

// private methods
/**
 * @var DISABLE_readCommandFromBufferErrorOutput
 *
 * Enable this option to disable the library's error output.
 * Default is false.
 */
#define DISABLE_readCommandFromBufferErrorOutput false

/**
 * @var DISABLE_ihout
 *
 * Enable this option to completely remove output functionality at buildtime from the library.
 * Default is false.
 */
#define DISABLE_ihout false

#include <InputHandler.h>

char output_buffer[1] = {'\0'}; // output buffer

const PROGMEM ih::ProcessName process_name = ""; // process name
const PROGMEM ih::EndOfLineChar process_eol = "\r\n"; // process end of line char
const PROGMEM ih::ControlCharSeq process_ccseq = "##"; // input control character sequence
const PROGMEM ih::WildcardChar process_wcc = "*"; // process wildcard char
const PROGMEM ih::DelimiterSequences pdelimseq = {
    2, // number of delimiter sequences
    {1, 1}, // delimiter sequence lens
    {" ", ","} // delimiter sequences
};

const PROGMEM ih::StartStopSequences process_ststpseq = {
    1.0, // num start stop sequence pairs
    {1, 1}, // start stop sequence lens
    {""
     ", "
     ""} // start stop sequence pairs
};

const PROGMEM ih::InputParameters input_prm[1] = {&process_name, &process_eol, &process_ccseq, &process_wcc, &pdelimseq, &process_ststpseq};
ih::Input inputHandler(input_prm, output_buffer, buffsz(output_buffer));

// default function, called if nothing matches or if there is an error
void unrecognized(ih::Input* inputProcess)
{
    // error output
    inputProcess->outputToStream(Serial);
}

void InputHandler_setup()
{
    Serial.println(F("Setting up InputHandler..."));
    inputHandler.defaultFunction(unrecognized); // set default function, called when user input has no match or is not valid

    inputHandler.begin(); // required.  returns true on success.
}

void setup()
{
    delay(500);
    Serial.begin(1152000);
    while (!Serial)
        ;
    InputHandler_setup();
}

void loop()
{
    inputHandler.getCommandFromStream(Serial);
    inputHandler.outputToStream(Serial);
}