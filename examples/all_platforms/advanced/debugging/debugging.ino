/**
   @file debugging.ino
   @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
   @brief An example that demonstrates how to use built in methods to assist in debugging process settings and CommandParameters in source code
   @version 0.9
   @date 2022-04-30

   @copyright Copyright (c) 2022
*/

// enable DEBUG before including InputHandler.h
// #define DEBUG_ADDCOMMAND // ensure you have a large enough output buffer to include debugging, see src/config/advanced_config.h for all debug methods available

#define DEBUG_INCLUDE_FREERAM // freeRam() returns how much free heap there is, use inside of Serial.print()

#include <InputHandler.h>

/*
  output char buffer
  650 is large enough for default values
  if you are testing longer delimiters then it may ask you to increase
  the size of the output buffer if you try and use "inputSettings",
  this is the buffer it's asking you to increase
*/
char output_buffer[652] {}; // output buffer

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
  &pststpseq
};
UserInput inputHandler(output_buffer, buffsz(output_buffer), input_prm);

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
CommandConstructor help_(help_param); //  help_ has a command string, and function specified

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
CommandConstructor settings_(settings_param); // settings_ has a command string, and function specified

/**
   this command will be REJECTED because the command string and user defined string length are different
*/
const PROGMEM CommandParameters these_param_will_be_rejected[1] = {
  unrecognized,             // this is allowed to be NULL, if this is NULL and the terminating subcommand function ptr is also NULL nothing will launch (error)
  no_wildcards,             // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
  "REJECTED",               // command string
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
CommandConstructor rejected_(these_param_will_be_rejected); //  help_ has a command string, and function specified

void setup()
{
  delay(500); // startup delay for reprogramming

  Serial.begin(115200); //  set up Serial object (Stream object)
  while (!Serial)
    ; //  wait for user
  int pre, post, process;
  pre = freeRam();
  Serial.println(F("Set up InputHandler..."));
  inputHandler.defaultFunction(unrecognized); // set default function, called when user input has no match or is not valid
  inputHandler.addCommand(help_);             // lists user commands
  inputHandler.addCommand(settings_);
  inputHandler.addCommand(rejected_); // this command will be rejected by addCommand error checking, it will not show up in help
  inputHandler.begin(); // required.  returns true on success.
  post = freeRam();
  process = pre - post;
  Serial.print(F("end InputHandler setup, process using "));
  Serial.print(process);
  Serial.print(F(" bytes of ram; "));
  Serial.print(post);
  Serial.println(F(" bytes available."));

  // put the commands you want to test here before begin()

  Serial.println(F("Do you want to perform a memory-leak test? y/n"));
  while (!Serial.available())
  {
    delay(1);
  }
  bool perform_test = false;
  uint32_t iterations = 0;
  while (Serial.available())
  {
    char rc = Serial.read();
    if (rc == 'y')
    {
      perform_test = true;
    }
  }
  if (perform_test == true)
  {
    Serial.println(F("Pause autoscroll before entering how many iterations you want to perform, and copy the free ram."));
    Serial.println(F("How many iterations? 0-UINT32_MAX"));
    while (!Serial.available())
    {
      delay(1);
    }

    iterations = Serial.parseInt();

    Serial.print(F("pre-test free ram: "));
    Serial.println(freeRam());
    // temp testing
    for (size_t i = 0; i < iterations; ++i)
    {
      inputHandler.listSettings(&inputHandler);
      inputHandler.outputToStream(Serial); // class output

      inputHandler.listCommands();         // formats output_buffer with the command list
      inputHandler.outputToStream(Serial); // class output
      Serial.print(F("free ram: "));
      Serial.print(freeRam());
      Serial.print(F(" iteration: "));
      Serial.println(i);
    }
    Serial.print(F("post-test free ram: "));
    Serial.println(freeRam());
  }
}

void loop()
{
  inputHandler.getCommandFromStream(Serial); //  read commands from a stream
  inputHandler.outputToStream(Serial); // class output
}
