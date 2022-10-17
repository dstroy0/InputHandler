/**
   @file NMEAparser.ino
   @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
   @brief An example that demonstrates how to use InputHandler's public methods to parse NMEA 0183 sentences
   @version 0.9
   @date 2022-04-17

   @copyright Copyright (c) 2022
*/

/*
  go to parser/NMEAsentencefunc.cpp to edit the sentence functions and add more functionality than displaying
  the sentence fields

  to add a new message type, define the message in parser/NMEAsentenceparam.h as a CommandParameters struct
  syntactically identical to the other structs found there, and then add your struct name to
  sentence_param AND sentence_error_param
*/

/*
  https://www.nmea.org/content/newsm/news?show=VIEW&a=34

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
           0x2a   42    Checksum delimiter
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

    Lots of interesting NMEA 0183 information:
    https://gpsd.gitlab.io/gpsd/NMEA.html
*/

#include <InputHandler.h>
#include "parser/NMEAparser.h"

extern const CommandParameters sentence_param[], sentence_error_param[]; // zero delim commands

char output_buffer[512] {}; //  UserInput output buffer

const PROGMEM IH_pname pname = "";         ///< default process name
const PROGMEM IH_eol peol = "\r\n";        ///< default process eol characters
const PROGMEM IH_input_cc pinputcc = "##"; ///< default input control character sequence
const PROGMEM IH_wcc pwcc = "*";

const PROGMEM InputProcessDelimiterSequences pipdelimseq = {
  1,    ///< number of delimiter sequences
  {1},  ///< delimiter sequence lens
  {" "} ///< delimiter sequences
};

const PROGMEM InputProcessDelimiterSequences psensordelimseq = {
  1,    ///< number of delimiter sequences
  {1},  ///< delimiter sequence lens
  {","} ///< delimiter sequences
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

UserInput inputHandler(input_prm, output_buffer, buffsz(output_buffer));

const PROGMEM InputProcessParameters sensor_prm[1] = {
  &pname,
  &peol,
  &pinputcc,
  &pwcc,
  &psensordelimseq,
  &pststpseq
};
UserInput sensorParser(sensor_prm, output_buffer, buffsz(output_buffer));

NMEAparse NMEA;

// temp for testing
const char* gpbwc = "$GPBWC,081837,,,,,,T,,M,,N,*13\r\n";
const char* gpgsa = "$GPGSA,081837,,,,,,T,,M,,N,*13\r\n";

/*
   default function, called if nothing matches or if there is an error
*/
void unrecognized(UserInput* inputProcess)
{
  // error output
  inputProcess->outputToStream(Serial);
}

CommandConstructor NMEA_sentence(sentence_param, nprms(sentence_param), 2);
CommandConstructor NMEA_sentence_error(sentence_error_param, nprms(sentence_error_param), 2);

void setup()
{
  delay(500); // startup delay for reprogramming

  Serial.begin(115200); //  set up Serial object (Stream object)

  while (!Serial)
    ; //  wait for user

  Serial.println(F("Set up InputHandler..."));
  inputHandler.defaultFunction(unrecognized); // set default function, called when user input has no match or is not valid

  sensorParser.addCommand(NMEA_sentence);       // regular sentence
  sensorParser.addCommand(NMEA_sentence_error); // one or more field errors
  inputHandler.begin();                         // required.  returns true on success.
  sensorParser.begin();
  Serial.println(F("end InputHandler setup"));
  inputHandler.outputToStream(Serial); // class output

  // temp testing
  uint8_t buffer[36] {};

  memcpy(buffer, gpbwc, strlen(gpbwc));
  NMEA.parseSentence(buffer, strlen(gpbwc));
  sensorParser.outputToStream(Serial);
  memcpy(buffer, gpgsa, strlen(gpgsa));
  NMEA.parseSentence(buffer, strlen(gpgsa));
  sensorParser.outputToStream(Serial);
}

void loop()
{
  inputHandler.getCommandFromStream(Serial); //  read commands from a stream, hardware or software should work
  inputHandler.outputToStream(Serial);       // class output
  sensorParser.outputToStream(Serial);
  // NMEA.parseSentence(Serial2); // getSentence accepts a Stream obect or (uint8_t buffer, size_t size)
}
