/**
   @file GetCommandFromStream.ino
   @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
   @brief An example that demonstrates how to retrieve type-valid arguments from a Stream
   @version 0.9
   @date 2022-04-16

   @copyright Copyright (c) 2022
*/

#include <InputHandler.h>

char output_buffer[650] {}; // output buffer
/*
  UserInput constructor settings
*/
const PROGMEM IH_pname pname = "_test_";   ///< default process name
const PROGMEM IH_eol peol = "\r\n";        ///< default process eol characters
const PROGMEM IH_input_cc pinputcc = "##"; ///< default input control character sequence
const PROGMEM IH_wcc pwcc = "*";           ///< default process wildcard character

const PROGMEM InputProcessDelimiterSequences pipdelimseq = {
  1,    ///< number of delimiter sequences
  {1},  ///< delimiter sequence lens
  {" "} ///< delimiter sequences
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
  &pipdelimseq,
  &pststpseq
};
UserInput inputHandler(input_prm, output_buffer, buffsz(output_buffer)); // UserInput constructor

// default function, called if nothing matches or if there is an error
void unrecognized(UserInput* inputProcess)
{
  // error output
  inputProcess->outputToStream(Serial);
}

// test all available input types
void test_input_types(UserInput* inputProcess)
{
  inputProcess->outputToStream(Serial);                                             // class output, doesn't have to output to the input stream
  char* str_ptr = inputProcess->nextArgument();                                     //  init str_ptr and point it at the next argument input by the user
  char* strtoul_ptr = 0;                                                            //  this is for strtoul
  uint32_t strtoul_result = strtoul(str_ptr, &strtoul_ptr, 10);                     // get the result in base10
  uint8_t eight_bit = (strtoul_result <= UINT8_MAX) ? (uint8_t)strtoul_result : 0U; // if the result is less than UINT8_MAX then set eight_bit, else eight_bit = 0

  str_ptr = inputProcess->nextArgument();
  strtoul_ptr = 0;
  strtoul_result = strtoul(str_ptr, &strtoul_ptr, 10);
  uint16_t sixteen_bit = (strtoul_result <= UINT16_MAX) ? (uint16_t)strtoul_result : 0U;

  str_ptr = inputProcess->nextArgument();
  strtoul_ptr = 0;
  uint32_t thirtytwo_bit = strtoul(str_ptr, &strtoul_ptr, 10);

  str_ptr = inputProcess->nextArgument();
  int sixteen_bit_int = atoi(str_ptr);

  str_ptr = inputProcess->nextArgument();
  float thirtytwo_bit_float = (float)atof(str_ptr);

  str_ptr = inputProcess->nextArgument();
  char _char = *str_ptr;

  str_ptr = inputProcess->nextArgument();
  char c_string[64] = {'\0'};
  snprintf_P(c_string, 64, PSTR("%s"), str_ptr);

  str_ptr = inputProcess->nextArgument();
  char unknown_string[64] = {'\0'};
  snprintf_P(unknown_string, 64, PSTR("%s"), str_ptr);

  char float_buffer[32] = {'\0'}; //  dtostrf buffer
  char out[512] = {'\0'};         //  function output buffer
  uint16_t string_pos = 0;        // function output buffer index

  // format out[] with all of the arguments received
  string_pos += snprintf_P(out + string_pos, 512,
                           PSTR("Test user input types:\n"
                                " uint8_t %u\n"
                                " uint16_t %u\n"
                                " uint32_t %lu\n"
                                " int %d\n"
                                " float %s\n"
                                " char %c\n"
                                " c-string %s\n"
                                " unknown-type %s\n"),
                           eight_bit,
                           sixteen_bit,
                           thirtytwo_bit,
                           sixteen_bit_int,
                           dtostrf(thirtytwo_bit_float, 2, 3, float_buffer),
                           _char,
                           c_string,
                           unknown_string);

  Serial.println(out);
}

/**
 * test enforces type-valid input
 */
const PROGMEM CommandParameters type_test_param[1] = {
  test_input_types,       // function ptr
  no_wildcards,              // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
  "test",                    // command string
  4,                         // string length
  root,                      // parent id
  root,                      // this command id
  root,                      // command depth
  0,                         // subcommands
  UI_ARG_HANDLING::type_arr, // argument handling
  8,                         // minimum expected number of arguments
  8,                         // maximum expected number of arguments
  /*
    UITYPE arguments
  */
  {
    UITYPE::UINT8_T,    // 8-bit  uint
    UITYPE::UINT16_T,   // 16-bit uint
    UITYPE::UINT32_T,   // 32-bit uint
    UITYPE::INT16_T,    // 16-bit int
    UITYPE::FLOAT,      // 32-bit float
    UITYPE::CHAR,       // char
    UITYPE::START_STOP, // regex-like start stop char sequences
    UITYPE::NOTYPE      // special type, no type validation performed
  }
};
CommandConstructor test_(type_test_param);

void setup()
{
  delay(500); // startup delay for reprogramming
  // uncomment as needed
  Serial.begin(115200); //  set up Serial object (Stream object)
  // Serial2.begin(115200);
  // Serial3.begin(115200);
  // Serial4.begin(115200);
  while (!Serial)
    ; //  wait for user

  Serial.println(F("Set up InputHandler..."));
  inputHandler.defaultFunction(unrecognized); // set default function, called when user input has no match or is not valid
  inputHandler.addCommand(test_);             // input type test
  inputHandler.begin();                          // required.  returns true on success.

  // comment this out if you're testing DISABLE_listSettings 
  inputHandler.listSettings(&inputHandler);
  inputHandler.outputToStream(Serial); // class output

  inputHandler.listCommands();         // formats output_buffer with the command list
  inputHandler.outputToStream(Serial); // class output
}

void loop()
{
  // uncomment as needed
  inputHandler.getCommandFromStream(Serial); //  read commands from a stream, hardware or software should work
  // inputHandler.getCommandFromStream(Serial2);  // Serial2
  // inputHandler.getCommandFromStream(Serial3);  // Serial3
  // inputHandler.getCommandFromStream(Serial4);  // Serial4

  // choose one stream to output to
  inputHandler.outputToStream(Serial); // class output

  // or output to multiple streams like this
  /*
    if(inputHandler.outputIsAvailable())
    {
    Serial.println(output_buffer);
    Serial2.println(output_buffer);
    Serial3.println(output_buffer);
    Serial4.println(output_buffer);

    // and clear the output buffer when you are finished
    inputHandler.clearOutputBuffer();
    }
  */
}