/**
   @file NMEAparser.h
   @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
   @brief a class to assist in parsing NMEA 183 ASCII strings
   @version 1.0
   @date 2022-03-31

   @copyright Copyright (c) 2022
*/
#if !defined(__NMEAparser_H__)
    #define __NMEAparser_H__

    #include <InputHandler.h> // include for UserInput object
    #include "NMEAsentenceparam.h"

extern char output_buffer[];                                      // output buffer declared in NMEAparser.ino
extern UserInput sensorParser;                                    // UserInput object declared in NMEAparser.ino
extern const Parameters sentence_param[], sentence_error_param[]; // zero delim command

    #define NMEA_SENTENCE_FIELDS_BUFFER_SIZE       128 // class NMEA sentence fields token buffer len
    #define NMEA_SENTENCE_MAX_NUM_FIELDS           32  // ???
    #define NMEA_SENTENCE_STREAM_INPUT_BUFFER_SIZE 85  // Stream object input wrapper buffer len

    #define NMEA_SENTENCE_MAX_EMPTY_FIELDS 32 // parseSentence input buffer size == input_len + (this * strlen(empty_field_ph))

// zero delimiter command Parameters struct pointers and array size
const byte num_zdc = 2;
const Parameters* zdc[num_zdc] = {sentence_param,
                                  sentence_error_param};

const char* empty_field_ph = "blank"; // empty sentence field placeholder

class NMEAparse
{
public:
    char* nextField()
    {
        if (_ptrs_index < NMEA_SENTENCE_MAX_NUM_FIELDS && _ptrs_index < _ptrs_index_max)
        {
            _ptrs_index++;
            return _ptrs[_ptrs_index];
        }
        return NULL; // else return NULL
    }

    void emptyOutputBuffer()
    {
        _ptrs_index = 0;
        for (size_t i = 0; i < NMEA_SENTENCE_FIELDS_BUFFER_SIZE; ++i)
        {
            _NMEA_sentence_fields_buffer[i] = '\0';
        }
    }

    void getSentence(uint8_t* buffer, size_t size) // input wrapper
    {
        sensorParser.readCommandFromBuffer(buffer, size, num_zdc, zdc);
    }

    void getSentence(Stream& stream) // input wrapper
    {
        sensorParser.getCommandFromStream(stream, NMEA_SENTENCE_STREAM_INPUT_BUFFER_SIZE, num_zdc, zdc);
    }

    void parseSentence(uint8_t* buffer, size_t size)
    {
        NMEAparse::emptyOutputBuffer();

        // search for checksum, perform validation if found

        // checksum validation is performed on the string between the ! or $ and *

        // insert empty field ph into empty fields
        size_t fields_received = 0;
        size_t corrected_input_idx = 0;
        size_t corrected_input_size = size + (strlen(empty_field_ph) * NMEA_SENTENCE_MAX_EMPTY_FIELDS);
        char* corrected_input = new char[corrected_input_size]();
        for (size_t i = 0; i < size; ++i)
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
            }
            else
            {
                corrected_input[corrected_input_idx] = (char)buffer[i];
                corrected_input_idx++;
            }
        }

        Serial.println((char*)buffer);
        Serial.println(corrected_input);

        // set up getTokensParam
        char _null_ = '\0';
        // delimiter string literal array
        const char* delimiters[] = {
            ","};
        // delimiter length string literal array
        size_t delimiter_lens[] = {
            1};
        UserInput::getTokensParam gtprm = {
            (uint8_t*)corrected_input,           // input data uint8_t array
            corrected_input_size,                // input len
            (char*)_NMEA_sentence_fields_buffer, // pointer to char array, size of len + 1
            NMEA_SENTENCE_FIELDS_BUFFER_SIZE,    // the size of token_buffer
            _ptrs,                               // token_buffer pointers
            _ptrs_index,                         // index of token_buffer pointer array
            _ptrs_index_max,                     // _data_pointers_[MAX], _data_pointers_index_[MAX]
            delimiters,                          // delimiter string literal array, const char**
            delimiter_lens,                      // delimiter strlen array
            buffsz(delimiter_lens),              // delimiters[MAX], delimiter_lens[MAX]
            NULL,                                // const char* c-string delimiter
            0,                                   // c-string delim len
            _null_,                              // token_buffer sep char, _null_ == '\0'
            NULL                                 // control character sequence
        };
        // feed corrected_input to getTokens
        // fields_received = getTokens(gtprm);

        // free corrected_input (delete[])

        _ptrs_index = 0; // set ptrs index back to zero so that nextField() works
    }

    void parseErrorSentence(uint8_t* buffer, size_t size)
    {
        NMEAparse::emptyOutputBuffer(); // clear output

        _ptrs_index = 0; // set ptrs index back to zero so that nextField() works
    }

    // 2 char following '*'
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
    uint8_t _NMEA_sentence_fields_buffer[NMEA_SENTENCE_FIELDS_BUFFER_SIZE] {}; // char buffer
    char* _ptrs[NMEA_SENTENCE_MAX_NUM_FIELDS];                                 // NMEA field ptrs size?
    uint8_t _ptrs_index = 0;
    size_t _ptrs_index_max = NMEA_SENTENCE_MAX_NUM_FIELDS; // temp, needs to be sized in parse
};

#endif
