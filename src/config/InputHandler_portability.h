#if !defined(__INPUTHANDLER_PORTABILITY_H__)
#define __INPUTHANDLER_PORTABILITY_H__

// portability directives
//  max value of a sixteen bit unsigned integer
#if !defined(UINT16_MAX)
    #define UINT16_MAX 65535
#endif

//  max value of an eight bit unsigned integer
#if !defined(UINT8_MAX)
    #define UINT8_MAX 255
#endif

#if defined(ARDUINO_SAMD_VARIANT_COMPLIANCE)
    #include <avr/dtostrf.h>
    #include "utility/vsnprintf.h"
    #define vsnprintf_P vsnprintf
    #undef pgm_read_dword
    #define pgm_read_dword(addr) ({     \
        typeof(addr) _addr = (addr);    \
        *(const unsigned long*)(_addr); \
    })
#endif

#if defined(__MBED_CONFIG_DATA__)
    #include <avr/dtostrf.h>
    #include "utility/vsnprintf.h"
    #define vsnprintf_P vsnprintf
    #undef pgm_read_dword
    #define pgm_read_dword(addr) ({     \
        typeof(addr) _addr = (addr);    \
        *(const unsigned long*)(_addr); \
    })
#endif

#if defined(ARDUINO_SAM_DUE)
    #include <avr/dtostrf.h>
    #include "utility/vsnprintf.h"
    #define vsnprintf_P vsnprintf
    #undef pgm_read_dword
    #define pgm_read_dword(addr) ({     \
        typeof(addr) _addr = (addr);    \
        *(const unsigned long*)(_addr); \
    })
#endif

#if defined(TEENSYDUINO)
    // pgm/ram section type conflict fix
    #define QUO(x)      #x
    #define QLINE(x, y) QUO(x) \
    QUO(y)
    #define PFIX QLINE(.progmem.variable, __COUNTER__)
    #undef PROGMEM
    #define PROGMEM __attribute__((section(PFIX)))
#endif

#endif // include guard
// end of file
