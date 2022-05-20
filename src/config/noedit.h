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
    #define UI_ESCAPED_CHAR_STRLEN 3       ///< sram buffer size in bytes for a single escaped char, used by UserInput methods
    /*
        Type macros
    */
    // CommandParameters related macros
    #define max_command_type uint8_t
    #define command_length_type uint16_t
    #define command_id_group_type uint16_t // affects progmem and ram
    #define tree_depth_type uint8_t
    #define sub_commands_type uint8_t    
    #define num_args_group_type uint8_t

    // UserInput private member type
    #define input_type_match_flags_type bool

    // CommandRuntimeCalc
    #define memcmp_idx_type uint8_t  // if you want more than 255 commands with wcc change this to uint16_t
    #define num_memcmp_ranges_type uint8_t // if you want more than 255 memcmp ranges in one command (default is 5)
    #define memcmp_ranges_type uint8_t // if your commands are longer than 255, change this to uint16_t

    
    // UserInput::_calcCmdMemcmpRanges and UserInput::_compareCommandToString specific (magic number!)
    #define UI_ALL_WCC_CMD ((memcmp_ranges_type)-1) // this should be the MAX of the containing array
    // end magic number

    // function-like macros
    #define nprms(x) (sizeof(x) / sizeof((x)[0])) // gets the number of elements in an array
    #define buffsz(x) nprms(x)                    // gets the number of elements in an array
    #define nelems(x) nprms(x)                    // gets the number of elements in an array
    // end function-like macros
    
    // portability directives
    #if !defined(UINT32_MAX)
        #define UINT32_MAX ((uint32_t)-1)
    #endif
    #if !defined(UINT16_MAX)
        #define UINT16_MAX ((uint16_t)-1) ///< max value of a sixteen bit unsigned integer
    #endif
    #if !defined(UINT8_MAX)
        #define UINT8_MAX ((uint8_t)-1) ///< max value of an eight bit unsigned integer
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
    
    #if UI_MAX_ARGS > 255
        #error UI_MAX_ARGS MAX == 255
    #endif
    #if UI_MAX_DEPTH > 255
        #error UI_MAX_DEPTH MAX == 255
    #endif
    #if UI_MAX_SUBCOMMANDS > 255
        #error UI_MAX_SUBCOMMANDS MAX == 255
    #endif
    #if UI_MAX_CMD_LEN > 65535
        #error UI_MAX_CMD_LEN MAX == 65535
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
    #if UI_MAX_PER_CMD_MEMCMP_RANGES > 255
        #error UI_MAX_PER_CMD_MEMCMP_RANGES MAX == 255
    #endif
    // end config error checking

#endif // end include guard
// end of file
