class NMEAparse
{
public:
    char NMEA_sentence_buffer[85]{};
    char *ptrs[32]; // NMEA field ptrs size?
    size_t ptrs_index = 0;

    void parse(char *buffer, size_t size) // input wrapper
    {
        if (size < 85)
        {
            memcpy(NMEA_sentence_buffer, buffer, size);
        }
        _parseSentence(NMEA_sentence_buffer, 85);
    }

    void parse(Stream &stream) // input wrapper
    {
        if (NMEAparse::_getSentenceFromStream(stream))
        {
            NMEAparse::_parseSentence(NMEA_sentence_buffer, 85);
        }
    }

private:
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
        return true;
    }

    void _parseSentence(char *buffer, size_t size)
    {
    }
};