#if !defined(__NMEAparser_H__)
#define __NMEAparser_H__

#include <InputHandler.h> // include for UserInput object

extern char output_buffer[]; // output buffer declared in NMEAparser.ino
extern UserInput sensorParser; // UserInput object declared in NMEAparser.ino
extern const Parameters sentence_param[], sentence_error_param[];


#define NMEA_SENTENCE_FIELDS_BUFFER_SIZE 128 // class NMEA sentence fields token buffer len
#define NMEA_SENTENCE_MAX_NUM_FIELDS 32 // ???
#define NMEA_SENTENCE_STREAM_INPUT_BUFFER_SIZE 85 // Stream object input wrapper buffer len

const Parameters *zdc[] = {
    sentence_param,
    sentence_error_param
};

class NMEAparse
{
public:

    void emptyBuffer()
    {
        for (size_t i = 0; i < NMEA_SENTENCE_FIELDS_BUFFER_SIZE; ++i)
        {
            _NMEA_sentence_fields_buffer[i] = '\0';
        }
    }

    void parse(uint8_t *buffer, size_t size) // input wrapper
    {
        NMEAparse::emptyBuffer();
        // NMEA buffer size is larger than input size and 
        // the buffer is null terminated to avoid encoding errors
        if (size < NMEA_SENTENCE_FIELDS_BUFFER_SIZE) 
        {
            NMEAparse::_parseSentence(buffer, size);            
        }        
    }

    void parse(Stream &stream) // input wrapper
    {
        if (NMEAparse::_getSentenceFromStream(stream))
        {
            NMEAparse::_parseSentence(_NMEA_sentence_fields_buffer, NMEA_SENTENCE_FIELDS_BUFFER_SIZE);
        }
    }

private:

    uint8_t _NMEA_sentence_fields_buffer[NMEA_SENTENCE_FIELDS_BUFFER_SIZE]{}; // char buffer  
    char *_ptrs[32]; // NMEA field ptrs size?
    size_t _ptrs_index = 0;
    
    // 2 char following '*'
    int _checksum(const char *s) // NMEA checksum validation
    {
        int c = 0;
        while (*s)
        {
            c ^= *s++;
        }
        return c;
    } 

    bool _getSentenceFromStream(Stream &stream) // called from NMEAparse(Stream& stream)
    {
        sensorParser.getCommandFromStream(stream, NMEA_SENTENCE_STREAM_INPUT_BUFFER_SIZE, 2, zdc);

        return true;
    }

    void _parseSentence(uint8_t *buffer, size_t size)
    {

    }
};

#endif