/**
   @file debugging.ino
   @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
   @brief An example that demonstrates how to use built in methods to assist in debugging process settings and CommandParameters in source code
   @version 0.9
   @date 2022-04-30

   @copyright Copyright (c) 2022
*/

/*    
    Optional and debugging methods are switched on/off or altered by #defining their switch
    before including the library.
*/
// disable OPTIONAL methods before including InputHandler.h
// #define DISABLE_listSettings // uncomment to DISABLE UserInput::listSettings(); see src/config/advanced_config.h for all the methods you can disable this way

// enable DEBUGGING methods before including InputHandler.h
#define DEBUG_INCLUDE_FREERAM // freeRam returns how much free heap there is, use inside of Serial.print()

/*
    Copy the library folder "InputHandler" to your sketch folder and then edit the config for project specific settings
    
    cue the compiler to look for the local copy of the libary first by using "" around the #include
    #include "InputHandler.h"
    
    This makes it so you can easily make project specific configurations.

    users: edit library settings in src/config/config.h
    advanced users: types are set in src/config/noedit.h inside of the namespace IH using preprocessor macros.
*/
#include "InputHandler.h"

/*
  output char buffer
  650 is large enough for default values
  if you are testing longer delimiters then it may ask you to increase
  the size of the output buffer if you try and use "inputSettings",
  this is the buffer it's asking you to increase
*/
char output_buffer[650] {}; // output buffer

const PROGMEM IH_pname pname = "_test_";   ///< test process name
const PROGMEM IH_eol peol = "\r\n";        ///< test process eol characters
const PROGMEM IH_input_cc pinputcc = "##"; ///< test input control character sequence
const PROGMEM IH_wcc pwcc = "*";           ///< test process wildcard character

// process input-data delimiter sequences
const PROGMEM InputProcessDelimiterSequences pipdelimseq = {
    1,    ///< number of delimiter sequences
    {1},  ///< delimiter sequence lens
    {" "} ///< delimiter sequences
};

// process input-data start-stop delimiter sequences
const PROGMEM InputProcessStartStopSequences pststpseq = {
    1,           ///< num start stop sequence pairs
    {1, 1},      ///< start stop sequence lens
    {"\"", "\""} ///< start stop sequence pairs
};

// process-wide user-defined input characteristics
const PROGMEM InputProcessParameters input_prm[1] = {
    &pname,
    &peol,
    &pinputcc,
    &pwcc,
    &pipdelimseq,
    &pststpseq};
UserInput inputHandler(input_prm, output_buffer, buffsz(output_buffer));

/*
   builtin function wrappers
*/
// default function
void unrecognized(UserInput* inputProcess)
{
    // error output
    inputProcess->outputToStream(Serial);
}
// lists process-wide settings and pertinent InputHandler_config.h settings
void settings(UserInput* inputProcess)
{
    inputProcess->listSettings(inputProcess);
}
// lists user-defined commands
void help(UserInput* inputProcess)
{
    inputProcess->listCommands();
}

/**
   help lists all commands in the process available to the user
   if you use the help function and do not see your command, it was rejected by the process, or,
   not added with addCommand
*/
const PROGMEM CommandParameters help_param[1] = {
    help,                     // this is allowed to be NULL, if this is NULL and the terminating subcommand function ptr is also NULL nothing will launch (error)
    no_wildcards,             // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
    "help",                   // command string
    4,                        // command string characters
    root,                     // parent id
    root,                     // this command id
    root,                     // command depth
    0,                        // subcommands
    UI_ARG_HANDLING::no_args, // argument handling
    0,                        // minimum expected number of arguments
    0,                        // maximum expected number of arguments
    /* UITYPE arguments */
    {UITYPE::NO_ARGS} // use NO_ARGS if the function expects no arguments
};
CommandConstructor help_(help_param); //  help_ CommandConstructor object

/**
   inputSettings lists process-wide settings, very useful to check and see that your custom
   delimiter sequences are present, and that all other settings are correct to work with
   your input
*/
const PROGMEM CommandParameters settings_param[1] = {
    settings,                 // function ptr
    no_wildcards,             // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
    "inputSettings",          // command string
    13,                       // command string characters
    root,                     // parent id
    root,                     // this command id
    root,                     // command depth
    0,                        // subcommands
    UI_ARG_HANDLING::no_args, // argument handling
    0,                        // minimum expected number of arguments
    0,                        // maximum expected number of arguments
    /* UITYPE arguments */
    {UITYPE::NO_ARGS} // use NO_ARGS if the function expects no arguments
};
CommandConstructor settings_(settings_param); // settings_ CommandConstructor object

void setup()
{
    delay(500); // startup delay for reprogramming
    Serial.begin(115200); //  set up Serial object (Stream object)
    while (!Serial)
        ; //  wait for user

    Serial.println(F("Set up InputHandler..."));
    inputHandler.defaultFunction(unrecognized); // set default function, called when user input has no match or is not valid
    inputHandler.addCommand(help_);             // lists user commands
    inputHandler.addCommand(settings_);
    Serial.println(F("end InputHandler setup"));
    Serial.print(F("free ram: "));Serial.println(freeRam());

    inputHandler.begin(); // required.  returns true on success.

    inputHandler.listSettings(&inputHandler);
    inputHandler.outputToStream(Serial); // class output

    inputHandler.listCommands();         // formats output_buffer with the command list
    inputHandler.outputToStream(Serial); // class output
    
    Serial.print(F("free ram: "));Serial.println(freeRam());
}

void loop()
{
    inputHandler.getCommandFromStream(Serial); //  read commands from a stream, hardware or software should work
    inputHandler.outputToStream(Serial);       // class output
}
