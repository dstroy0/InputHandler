/**
   @file debugging.ino
   @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
   @brief An example that demonstrates how to use built in methods to assist in debugging process
   settings and CommandParameters in source code
   @version 1.0
   @date 2023/2/24

   @copyright Copyright (c) 2022
*/

/*
    users: edit library settings in src/config/config.h or below
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

#include "InputHandler.h"

/*
  output char buffer
  650 is large enough for default values
  if you are testing longer delimiters then it may ask you to increase
  the size of the output buffer if you try and use "inputSettings",
  this is the buffer it's asking you to increase
*/
char output_buffer[600] {}; // output buffer

const PROGMEM ih::ProcessName process_name = "_test_"; ///< test process name
const PROGMEM ih::EndOfLineChar process_eol = "\r\n"; ///< test process eol characters
const PROGMEM ih::ControlCharSeq process_ccseq = "##"; ///< test input control character sequence
const PROGMEM ih::WildcardChar process_wcc = "*"; ///< test process wildcard character

// process input-data delimiter sequences
const PROGMEM ih::DelimiterSequences process_delimseq = {
    1, ///< number of delimiter sequences
    {1}, ///< delimiter sequence lens
    {" "} ///< delimiter sequences
};

// process input-data start-stop delimiter sequences
const PROGMEM ih::StartStopSequences process_ststpseq = {
    1, ///< num start stop sequence pairs
    {1, 1}, ///< start stop sequence lens
    {"\"", "\""} ///< start stop sequence pairs
};

// process-wide user-defined input characteristics
const PROGMEM ih::InputParameters input_prm[1] = {&process_name, &process_eol, &process_ccseq, &process_wcc, &process_delimseq, &process_ststpseq};
ih::Input inputHandler(input_prm, output_buffer, buffsz(output_buffer));

/*
   builtin function wrappers
*/
// default function
void unrecognized(ih::Input* inputProcess)
{
    // error output
    inputProcess->outputToStream(Serial);
}
// lists process-wide settings and pertinent InputHandler_config.h settings
void settings(ih::Input* inputProcess) { inputProcess->listSettings(); }
// lists user-defined commands
void help(ih::Input* inputProcess) { inputProcess->listCommands(); }
// prints free ram
void getFreeRam(ih::Input* inputProcess)
{
    inputProcess->ihout(PSTR("free heap: %d"), freeRam());
    inputProcess->outputToStream(Serial);
}

/**
   help lists all commands in the process available to the user
   if you use the help function and do not see your command, it was rejected by the process, or,
   not added with addCommand
*/
const PROGMEM ih::Parameters help_param[1] = {
    help, // this is allowed to be NULL, if this is NULL and the terminating subcommand function ptr
          // is also NULL nothing will launch (error)
    ih::WC_FLAG::no_wildcards, // no_wildcards or has_wildcards, default WildCard Character (wcc) is
                               // '*'
    "help", // command string
    4, // command string characters
    ih::root, // parent id
    ih::root, // this command id
    ih::root, // command depth
    0, // subcommands
    ih::UI_ARG_HANDLING::no_args, // argument handling
    0, // minimum expected number of arguments
    0, // maximum expected number of arguments
    /* UITYPE arguments */
    {ih::UITYPE::NO_ARGS} // use NO_ARGS if the function expects no arguments
};
ih::Command help_(help_param); //  help_ CommandConstructor object

/**
   inputSettings lists process-wide settings, very useful to check and see that your custom
   delimiter sequences are present, and that all other settings are correct to work with
   your input
*/
const PROGMEM ih::Parameters settings_param[1] = {
    settings, // function ptr
    ih::WC_FLAG::no_wildcards, // no_wildcards or has_wildcards, default WildCard Character (wcc) is
                               // '*'
    "inputSettings", // command string
    13, // command string characters
    ih::root, // parent id
    ih::root, // this command id
    ih::root, // command depth
    0, // subcommands
    ih::UI_ARG_HANDLING::no_args, // argument handling
    0, // minimum expected number of arguments
    0, // maximum expected number of arguments
    /* UITYPE arguments */
    {ih::UITYPE::NO_ARGS} // use NO_ARGS if the function expects no arguments
};
ih::Command settings_(settings_param); // settings_ CommandConstructor object

/**
   freeRam prints available heap
*/
const PROGMEM ih::Parameters getFreeRam_param[1] = {
    getFreeRam, // function ptr
    ih::WC_FLAG::no_wildcards, // no_wildcards or has_wildcards, default WildCard Character (wcc) is
                               // '*'
    "freeRam", // command string
    7, // command string characters
    ih::root, // parent id
    ih::root, // this command id
    ih::root, // command depth
    0, // subcommands
    ih::UI_ARG_HANDLING::no_args, // argument handling
    0, // minimum expected number of arguments
    0, // maximum expected number of arguments
    /* UITYPE arguments */
    {ih::UITYPE::NO_ARGS} // use NO_ARGS if the function expects no arguments
};
ih::Command getFreeRam_(getFreeRam_param); // settings_ CommandConstructor object

void setup()
{
    delay(500); // startup delay for reprogramming
    Serial.begin(115200); //  set up Serial object (Stream object)
    while (!Serial)
        ; //  wait for user

    Serial.println(F("Set up InputHandler..."));
    getFreeRam(&inputHandler);
    inputHandler.defaultFunction(unrecognized); // set default function, called when user input has no match or is not valid
    inputHandler.addCommand(help_); // lists user commands
    inputHandler.addCommand(settings_);
    inputHandler.addCommand(getFreeRam_);
    Serial.println(F("end InputHandler setup"));
    getFreeRam(&inputHandler);

    Serial.println(F("before begin"));
    getFreeRam(&inputHandler);
    inputHandler.begin(); // required.  returns true on success.
    Serial.println(F("after begin"));
    getFreeRam(&inputHandler);

    inputHandler.listSettings();
    inputHandler.outputToStream(Serial); // class output

    inputHandler.listCommands(); // formats output_buffer with the command list
    inputHandler.outputToStream(Serial); // class output

    Serial.println(F("end setup()"));
    getFreeRam(&inputHandler);
}

void loop()
{
    inputHandler.getCommandFromStream(Serial); //  read commands from a stream, hardware or software should work
    inputHandler.outputToStream(Serial); // class output
}
