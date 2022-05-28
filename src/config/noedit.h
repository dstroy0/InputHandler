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
    #include "config/config.h"
    #include "config/advanced_config.h"

    /*
        do not edit the sections below unless you know what will happen
    */

    // function-like macros
    #define nprms(x) (sizeof(x) / sizeof((x)[0])) // gets the number of elements in an array
    #define buffsz(x) nprms(x)                    // gets the number of elements in an array
    #define nelems(x) nprms(x)                    // gets the number of elements in an array
    #define S(x) #x                               // gnu direct # stringify macro
    #define STR(x) S(x)                           // gnu indirect # stringify macro
    // end function-like macros

    // file location directive    
    #define LOC __FILE__:__LINE__
    #define LOCATION STR(LOC)
    // end file location directive

    // portability directives
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

    // sizing macros
    #define UI_ESCAPED_CHAR_STRLEN 3 ///< sram buffer size in bytes for a single escaped char, used by UserInput methods

    /*
        "auto" Type macros
    */

    // UI_ALL_WCC_CMD UserInput::_calcCmdMemcmpRanges and UserInput::_compareCommandToString specific (magic number!)
    #define UI_ALL_WCC_CMD ((IH::memcmp_ranges_type)-1) // UI_ALL_WCC_CMD is Type MAX
/**
 * @namespace IH
 * @brief "auto" type namespace
 *
 * auto type sizing macros, uses src/config.h as input
 */
namespace IH {
// InputProcessDelimiterSequences
typedef uint8_t delim_lens_type;

// InputProcessStartStopSequences
typedef uint8_t start_stop_sequence_lens_type;

// CommandParameters related macros
// typedef uint8_t max_command_type; // max number of commands
typedef uint8_t command_length_type;
typedef uint16_t command_id_group_type; // parent and this command id
typedef uint8_t tree_depth_type;
typedef uint8_t sub_commands_type;
typedef uint8_t num_args_group_type;

// UserInput private member type
typedef bool input_type_match_flags_type;

// CommandRuntimeCalc
typedef uint8_t memcmp_idx_type;        // if you want more than 255 commands with wcc change this to uint16_t
typedef uint8_t num_memcmp_ranges_type; // if you want more than 255 memcmp ranges in one command (default is 5)
typedef uint8_t memcmp_ranges_type;     // if your commands are longer than 255, change this to uint16_t

// config error checking

    #if UI_MAX_COMMANDS <= UINT8_MAX
        typedef uint8_t max_command_type;
    #endif    
    #if UI_MAX_COMMANDS > UINT8_MAX && UI_MAX_COMMANDS < UINT16_MAX
        typedef uint16_t max_command_type; 
        #pragma message(" at " LOCATION)
        #warning UI_MAX_COMMANDS|max_command_type changed from uint8_t to uint16_t        
    #endif
    #if UI_MAX_COMMANDS > UINT16_MAX && UI_MAX_COMMANDS < UINT32_MAX
        typedef uint32_t max_command_type;
        #pragma message(" at " LOCATION)
        #warning UI_MAX_COMMANDS|max_command_type changed from uint8_t to uint32_t
    #endif
    #if UI_MAX_COMMANDS > UINT32_MAX
        #pragma message(" at " LOCATION)
        #warning UI_MAX_ARGS cannot be greater than UINT32_MAX
    #endif // end UI_MAX_COMMANDS


// end config error checking
} // end namespace IH
#endif // end include guard
// end of file
