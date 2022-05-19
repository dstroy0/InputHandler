/**
   @file noedit.h
   @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
   @brief InputHandler library C includes
   @version 1.0
   @date 2022-05-16

   @copyright Copyright (c) 2022
*/
/*
 Copyright (C) 2022 Douglas Quigg (dstroy0) <dquigg123@gmail.com>

 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU General Public License
 version 3 as published by the Free Software Foundation.
 */

#if !defined(__INPUTHANDLER_NOEDIT_H__)
    #define __INPUTHANDLER_NOEDIT_H__

    #include <Arduino.h>
    #include "config.h"
    #include "advanced_config.h"

    /*
        do not edit the sections below unless you know what will happen
    */

    // sizing macros
    #define UI_MAX_PER_CMD_MEMCMP_RANGES 5 ///< UserInput::addCommand array sizing macro
    #define UI_ESCAPED_CHAR_STRLEN 3       ///< sram buffer size for a single escaped char, used by UserInput methods

    // alloc TYPE macros

    // UserInput::_calcCmdMemcmpRanges and UserInput::_compareCommandToString specific (magic number!)
    #define UI_ALL_WCC_CMD 255 // this should be the MAX of the containing array
    // end magic number

    // function-like macros
    #define nprms(x) (sizeof(x) / sizeof((x)[0])) // gets the number of elements in an array
    #define buffsz(x) nprms(x)                    // gets the number of elements in an array
    #define nelems(x) nprms(x)                    // gets the number of elements in an array
    // end function-like macros

    // portability directives
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
    // end portability directives

    // config error checking -- replace these with alloc sizing macros
    #if UI_MAX_ARGS > 255
        #error UI_MAX_ARGS MAX == 255
    #endif
    #if UI_MAX_DEPTH > 255
        #error UI_MAX_DEPTH MAX == 255
    #endif
    #if UI_MAX_SUBCOMMANDS > 255
        #error UI_MAX_SUBCOMMANDS MAX == 255
    #endif
    #if UI_MAX_CMD_LEN > 255
        #error UI_MAX_CMD_LEN MAX == 255
    #endif
    #if UI_MAX_DELIM_SEQ > 255
        #error UI_MAX_DELIM_SEQ MAX == 255
    #endif
    #if UI_MAX_START_STOP_SEQ > 255
        #error UI_MAX_START_STOP_SEQ MAX == 255
    #endif
    #if UI_MAX_IN_LEN > 65533
        #error UI_MAX_IN_LEN MAX exceeded
    #endif
    // end config error checking

#endif // end include guard
// end of file
