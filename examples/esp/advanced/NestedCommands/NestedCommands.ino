/**
   @file NestedCommands.ino
   @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
   @brief An example that demonstrates subcommands
   @version 0.9
   @date 2022-03-18

   @copyright Copyright (c) 2022
*/

#include <InputHandler.h>

/*
  this output buffer is formatted by UserInput's methods
  you have to empty it out yourself with
  OutputToStream()
*/
char output_buffer[512] = {'\0'}; //  output buffer

/*
  UserInput constructor
*/
UserInput inputHandler(/* UserInput's output buffer */ output_buffer,
    /* size of UserInput's output buffer */ buffSZ(output_buffer),
    /* username */ "",
    /* end of line characters */ "\r\n",
    /* token delimiter */ " ",
    /* c-string delimiter */ "\"");

/*
   default function, called if nothing matches or if there is an error
*/
void uc_unrecognized(UserInput* inputProcess)
{
  // error output
  inputProcess->outputToStream(Serial);
  Serial.println(F("error."));
}

void uc_nest_one(UserInput* inputProcess)
{
  inputHandler.outputToStream(Serial); // class output
  Serial.println(F("made it to uc_nest_one."));
}

void uc_nest_two(UserInput* inputProcess)
{
  inputHandler.outputToStream(Serial); // class output
  Serial.println(F("made it to uc_nest_two."));
}

const PROGMEM Parameters nested_prms[3] =
    {
        {                          // root command
         uc_unrecognized,          // this is allowed to be NULL, if this is NULL and the terminating subcommand function ptr is also NULL nothing will launch
         "launch",                 // command string
         6,                        // command string characters
         root,                     // parent id
         root,                     // this command id
         root,                     // command depth
         2,                        // subcommands
         UI_ARG_HANDLING::no_args, // argument handling
         0,                        // minimum expected number of arguments
         0,                        // maximum expected number of arguments
         /*
           UITYPE arguments
         */
         {
             UITYPE::NO_ARGS // use NO_ARGS if the function expects no arguments
         }},
        {                          // subcommand depth one
         uc_nest_one,              // unique function
         "one",                    // command string
         3,                        // command string characters
         root,                     // parent id
         1,                        // this command id
         1,                        // command depth
         0,                        // subcommands
         UI_ARG_HANDLING::no_args, // argument handling
         0,                        // minimum expected number of arguments
         0,                        // maximum expected number of arguments
         /*
           UITYPE arguments
         */
         {
             UITYPE::NO_ARGS // use NO_ARGS if the function expects no arguments
         }},
        {                          // subcommand depth one
         uc_nest_two,              // unique function
         "two",                    // command string
         3,                        // command string characters
         root,                     // parent id
         2,                        // this command id
         1,                        // command depth
         0,                        // subcommands
         UI_ARG_HANDLING::no_args, // argument handling
         0,                        // minimum expected number of arguments
         0,                        // maximum expected number of arguments
         /*
           UITYPE arguments
         */
         {
             UITYPE::NO_ARGS // use NO_ARGS if the function expects no arguments
         }}};
CommandConstructor uc_nested_example_(nested_prms, _N_prms(nested_prms), 1); 

void setup()
{
  delay(500); // startup delay for reprogramming
  Serial.begin(115200); //  set up Serial object (Stream object)
  while (!Serial); //  wait for user

  Serial.println(F("Set up InputHandler..."));
  inputHandler.defaultFunction(uc_unrecognized); // set default function, called when user input has no match or is not valid  
  inputHandler.addCommand(uc_nested_example_);   // nested commands example
  inputHandler.begin();                          // required.  returns true on success.
  inputHandler.listCommands();
  inputHandler.outputToStream(Serial); // class output  
}

void loop()
{
  inputHandler.getCommandFromStream(Serial); //  read commands from a stream, hardware or software should work
  inputHandler.outputToStream(Serial); // class output
}
