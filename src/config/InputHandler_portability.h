/**
   @file InputHandler_portability.h
   @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
   @brief InputHandler library portability directives
   @version 1.0
   @date 2022-05-10

   @copyright Copyright (c) 2022
*/
/*
 Copyright (C) 2022 Douglas Quigg (dstroy0) <dquigg123@gmail.com>

 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU General Public License
 version 3 as published by the Free Software Foundation.
 */

#if !defined(__INPUTHANDLER_PORTABILITY_H__)
    #define __INPUTHANDLER_PORTABILITY_H__
/*
    portability directives
*/

    #if !defined(UINT16_MAX)
        #define UINT16_MAX 65535 ///< max value of a sixteen bit unsigned integer
    #endif

    #if !defined(UINT8_MAX)
        #define UINT8_MAX 255 ///< max value of an eight bit unsigned integer
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
        #define QUO(x) #x
        #define QLINE(x, y) \
            QUO(x)          \
            QUO(y)
        #define PFIX QLINE(.progmem.variable, __COUNTER__)
        #undef PROGMEM
        #define PROGMEM __attribute__((section(PFIX)))
    #endif

#endif // include guard
// end of file
