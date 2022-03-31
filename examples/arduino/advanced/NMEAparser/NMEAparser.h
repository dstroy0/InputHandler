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

extern char output_buffer[];   // output buffer declared in NMEAparser.ino
extern UserInput sensorParser; // UserInput object declared in NMEAparser.ino
extern const Parameters sentence_param[], sentence_error_param[];

#define NMEA_SENTENCE_FIELDS_BUFFER_SIZE 128      // class NMEA sentence fields token buffer len
#define NMEA_SENTENCE_MAX_NUM_FIELDS 32           // ???
#define NMEA_SENTENCE_STREAM_INPUT_BUFFER_SIZE 85 // Stream object input wrapper buffer len

// zero delimiter command Parameters struct pointers and array size
const byte num_zdc = 2;
const Parameters *zdc[num_zdc] = {sentence_param,
                                  sentence_error_param};

class NMEAparse
{
public:
    char *nextField()
    {
        if (_ptrs_index < NMEA_SENTENCE_MAX_NUM_FIELDS &&
            _ptrs_index < _ptrs_index_max)
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

    void getSentence(uint8_t *buffer, size_t size) // input wrapper
    {
        sensorParser.readCommandFromBuffer(buffer, size, num_zdc, zdc);
    }

    void getSentence(Stream &stream) // input wrapper
    {
        sensorParser.getCommandFromStream(stream, NMEA_SENTENCE_STREAM_INPUT_BUFFER_SIZE, num_zdc, zdc);
    }

    void parseSentence(uint8_t *buffer, size_t size)
    {
        NMEAparse::emptyOutputBuffer();
        // search for checksum, perform validation if found
        
        // _ptrs_index_max = get_tokens add 

        _ptrs_index = 0; // set ptrs index back to zero so that nextField() works
    }

    void parseErrorSentence(uint8_t *buffer, size_t size)
    {
        NMEAparse::emptyOutputBuffer(); // clear output

        _ptrs_index = 0; // set ptrs index back to zero so that nextField() works
    }

    // 2 char following '*'
    // send this function the char between $ and *
    int calcChecksum(const char *s) // NMEA checksum validation
    {
        int c = 0;
        while (*s)
        {
            c ^= *s++;
        }
        return c;
    }

private:
    uint8_t _NMEA_sentence_fields_buffer[NMEA_SENTENCE_FIELDS_BUFFER_SIZE]{}; // char buffer
    char *_ptrs[NMEA_SENTENCE_MAX_NUM_FIELDS];                                // NMEA field ptrs size?
    size_t _ptrs_index = 0;
    size_t _ptrs_index_max = NMEA_SENTENCE_MAX_NUM_FIELDS; // temp, needs to be sized in parse
};

#endif
