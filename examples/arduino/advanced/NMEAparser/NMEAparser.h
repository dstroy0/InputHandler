/**
   @file NMEAparser.h
   @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
   @brief a class to assist in parsing NMEA 0183 strings
   @version 1.0
   @date 2022-04-02

   @copyright Copyright (c) 2022
*/
#if !defined(__NMEAparser_H__)
    #define __NMEAparser_H__

    #include <InputHandler.h>      // include for UserInput object
    #include "NMEAsentenceparam.h" // NMEA commands setup

    #define NMEA_SENTENCE_STREAM_INPUT_BUFFER_SIZE 85 // Stream object input wrapper buffer len
    #define NMEA_SENTENCE_MAX_EMPTY_FIELDS         32 // parseSentence input buffer size == input_len + (this * strlen(empty_field_ph))

// external objects
extern UserInput sensorParser;                                    // UserInput object declared in NMEAparser.ino
extern const Parameters sentence_param[], sentence_error_param[]; // zero delim commands declared in NMEAsentenceparam.h
// end external objects

const byte num_zdc = 2;                                                  // number of zero delim commands
const Parameters* zdc[num_zdc] = {sentence_param, sentence_error_param}; // zero delim command Parameters structure pointers

const char* empty_field_ph = "blank"; // empty sentence field placeholder (temporary)

class NMEAparse
{
public:
    void parseSentence(uint8_t* buffer, size_t len) // Buffer input wrapper
    {
        NMEAparse::_parseSentence(buffer, len);
    }

    void parseSentence(Stream& stream) // Stream input wrapper
    {
        // read stream
        char stream_buffer[NMEA_SENTENCE_STREAM_INPUT_BUFFER_SIZE] {};
        size_t idx = 0;
        while (stream.available() > 0)
        {
            stream_buffer[idx] = stream.read();
            idx++;
        }
        NMEAparse::parseSentence((uint8_t*)stream_buffer, idx); // pass stream buffer to NMEAparse::getSentence(uint8_t*, size_t)
    }

    // 2 char following '*','HEX','HEX'
    // send this function the char between $ and *
    int calcChecksum(const char* s) // NMEA checksum validation
    {
        int c = 0;
        while (*s)
        {
            c ^= *s++;
        }
        return c;
    }

private:
    void _parseSentence(uint8_t* buffer, size_t len)
    {
        // todo:
        // search for checksum, perform validation if found
        // checksum validation is performed on the string between the ! or $ and *

        // insert empty field ph into empty fields
        size_t fields_received = 0;
        size_t corrected_input_idx = 0;
        size_t corrected_input_size = len + (strlen(empty_field_ph) * NMEA_SENTENCE_MAX_EMPTY_FIELDS);
        char* corrected_input = new char[corrected_input_size]();
        for (size_t i = 0; i < len; ++i)
        {
            // if the char following a field sep ',' is another field sep
            // or a null
            // or a control char
            // or the checksum delimiter

            // i think an easier way to detect is if the char after ',' isdigit or isalpha
            if ((char)buffer[i] == ',' && ((char)buffer[i + 1] == ',' || (char)buffer[i + 1] == '*' || (char)buffer[i + 1] == '\0') || (iscntrl((char)buffer[i + 1]) == true))
            {
                corrected_input[corrected_input_idx] = (char)buffer[i];
                corrected_input_idx++;
                memcpy(corrected_input + corrected_input_idx, empty_field_ph, strlen(empty_field_ph));
                corrected_input_idx += strlen(empty_field_ph);
                if ((char)buffer[i + 1] == '*')
                {
                    corrected_input[corrected_input_idx] = ',';
                    corrected_input_idx++;
                }
            }
            else
            {
                corrected_input[corrected_input_idx] = (char)buffer[i];
                corrected_input_idx++;
            }
        }
        sensorParser.readCommandFromBuffer((uint8_t*)corrected_input, strlen(corrected_input), num_zdc, zdc);
    }
};

#endif
