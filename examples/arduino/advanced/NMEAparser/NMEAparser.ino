/**
   @file NMEAparser.ino
   @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
   @brief An example that demonstrates how to use InputHandler to parse NMEA sentences
   @version 0.9
   @date 2022-03-30

   @copyright Copyright (c) 2022
*/

/*
  https://en.wikipedia.org/wiki/NMEA_0183

  Message structure

    All transmitted data are printable ASCII characters between 0x20 (space) to 0x7e (~)
    Data characters are all the above characters except the reserved characters (See next line)
    Reserved characters are used by NMEA0183 for the following uses:

    ASCII   Hex   Dec   Use
     <CR>  0x0d   13    Carriage return
     <LF>  0x0a   10    Line feed, end delimiter
      !    0x21   33    Start of encapsulation sentence delimiter
      $    0x24   36    Start delimiter
      *    0x2a   42    Checksum delimiter
      ,    0x2c   44    Field delimiter
      \    0x5c   92    TAG block delimiter
      ^    0x5e   94    Code delimiter for HEX representation of ISO/IEC 8859-1 (ASCII) characters
      ~    0x7e  126    Reserved

    Messages have a maximum length of 82 characters, including the $ or ! starting character and the ending <LF>
    The start character for each message can be either a $ (For conventional field delimited messages) or ! (for messages that have special encapsulation in them)
    The next five characters identify the talker (two characters) and the type of message (three characters).
    All data fields that follow are comma-delimited.
    Where data is unavailable, the corresponding field remains blank (it contains no character before the next delimiter
    The first character that immediately follows the last data field character is an asterisk, but it is only included if a checksum is supplied.
    The asterisk is immediately followed by a checksum represented as a two-digit hexadecimal number. The checksum is the bitwise exclusive OR of ASCII 
    codes of all characters between the $ and *, not inclusive. According to the official specification, the checksum is optional for most data sentences, but is compulsory for RMA, RMB, and RMC (among others).
    <CR><LF> ends the message.
*/

#include <InputHandler.h>
#include "NMEAparser.h"

NMEAparse NMEA;

char output_buffer[256] = {'\0'}; //  UserInput output buffer
UserInput inputHandler(/* UserInput's output buffer */ output_buffer,
    /* size of UserInput's output buffer */ buffsz(output_buffer),
    /* username */ "",
    /* end of line characters */ "\r\n",
    /* token delimiter */ " ",
    /* c-string delimiter */ "");

UserInput sensorParser(/* UserInput's output buffer */ output_buffer,
    /* size of UserInput's output buffer */ buffsz(output_buffer),
    /* username */ "",
    /* end of line characters */ "\r\n",
    /* token delimiter */ " ",
    /* c-string delimiter */ "");

/*
   default function, called if nothing matches or if there is an error
*/
void uc_unrecognized(UserInput* inputProcess)
{
  // error output
  inputProcess->outputToStream(Serial);
}

/*
   test all available input types
*/
void uc_test_input_types(UserInput *inputProcess)
{
  inputProcess->outputToStream(Serial);                                             // class output, doesn't have to output to the input stream
  char *str_ptr = inputProcess->nextArgument();                                     //  init str_ptr and point it at the next argument input by the user
  char *strtoul_ptr = 0;                                                            //  this is for strtoul
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

  /*
       format out[] with all of the arguments received
  */
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

void NMEA_parse_test(UserInput *inputProcess)
{

}

/**
   @brief Parameters struct for NMEA sentence error

*/
const PROGMEM Parameters sentence_error_param[1] = {
  NMEA_parse_test,           // function ptr
  "!",                       // command string
  1,                         // string length
  root,                      // parent id
  root,                      // this command id
  root,                      // command depth
  0,                         // subcommands
  UI_ARG_HANDLING::one_type, // argument handling
  0,                         // minimum expected number of arguments
  32,                         // maximum expected number of arguments
  /*
    UITYPE arguments
  */
  {    
    UITYPE::NOTYPE    // special type, no type validation performed
  }

  // reference to nested sentence decomposer params
};
CommandConstructor NMEA_sentence_error(sentence_error_param);

/**
   @brief Parameters struct for NMEA sentence
*/
const PROGMEM Parameters sentence_param[1] = {
  NMEA_parse_test,           // function ptr
  "$",                       // command string
  1,                         // string length
  root,                      // parent id
  root,                      // this command id
  root,                      // command depth
  0,                         // subcommands
  UI_ARG_HANDLING::one_type, // argument handling
  0,                         // minimum expected number of arguments
  32,                         // maximum expected number of arguments
  /*
    UITYPE arguments
  */
  {    
    UITYPE::NOTYPE    // special type, no type validation performed
  }

  // reference to nested sentence decomposer params
};
CommandConstructor NMEA_sentence(sentence_param);



void setup()
{
  delay(500); // startup delay for reprogramming
  
  Serial.begin(115200); //  set up Serial object (Stream object)
 
  while (!Serial); //  wait for user

  Serial.println(F("Set up InputHandler..."));
  inputHandler.defaultFunction(uc_unrecognized); // set default function, called when user input has no match or is not valid
 
  sensorParser.addCommand(NMEA_sentence); // regular sentence
  sensorParser.addCommand(NMEA_sentence_error); // one or more field errors
  inputHandler.begin();                          // required.  returns true on success.  
  sensorParser.begin();
  
  inputHandler.outputToStream(Serial); // class output
}

void loop()
{  
  inputHandler.getCommandFromStream(Serial); //  read commands from a stream, hardware or software should work    
  inputHandler.outputToStream(Serial); // class output

  NMEA.parse(Serial2);
}
