#ifndef MOCK_ARDUINO_H
#define MOCK_ARDUINO_H

#include <iostream>
#include <vector>
#include <cstring>
#include <cstdarg>
#include <cmath>
#include <cstdint>
#include <cctype>
#include <climits>

// Mocking Arduino environment
#define PROGMEM
#define PSTR(s) s
#define strlen_P strlen
#define memcpy_P memcpy
#define memcmp_P memcmp
#define pgm_read_byte(addr) (*(const uint8_t*)(addr))
#define pgm_read_word(addr) (*(const uint16_t*)(addr))
#define pgm_read_dword(addr) (*(const uint32_t*)(addr))
#define vsnprintf_P vsnprintf
#define snprintf_P snprintf

typedef bool boolean;
typedef uint8_t byte;

class Stream {
public:
    virtual int available() = 0;
    virtual int read() = 0;
    virtual void println(const char* s) { std::cout << s << std::endl; }
    virtual void print(const char* s) { std::cout << s; }
};

class MockStream : public Stream {
    std::vector<uint8_t> buffer;
    size_t pos = 0;
public:
    void feed(const char* s) {
        for (const char* p = s; *p; ++p) buffer.push_back(*p);
    }
    int available() override { return (int)buffer.size() - (int)pos; }
    int read() override { return pos < buffer.size() ? buffer[pos++] : -1; }
};

#define abs(x) ((x) < 0 ? -(x) : (x))

#endif
