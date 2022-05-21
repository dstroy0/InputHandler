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

    // function-like macros
    #define nprms(x) (sizeof(x) / sizeof((x)[0])) // gets the number of elements in an array
    #define buffsz(x) nprms(x)                    // gets the number of elements in an array
    #define nelems(x) nprms(x)                    // gets the number of elements in an array
    // end function-like macros
    
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
    #define UI_ESCAPED_CHAR_STRLEN 3       ///< sram buffer size in bytes for a single escaped char, used by UserInput methods
    /*
        Type macros
    */
    // InputProcessDelimiterSequences
    #define delim_lens_type uint8_t

    // InputProcessStartStopSequences
    #define start_stop_sequence_lens_type uint8_t

    // CommandParameters related macros
    #define max_command_type uint8_t // max number of commands
    #define command_length_type uint8_t
    #define command_id_group_type uint16_t // parent and this command id
    #define tree_depth_type uint8_t
    #define sub_commands_type uint8_t    
    #define num_args_group_type uint8_t

    // UserInput private member type
    #define input_type_match_flags_type bool

    // CommandRuntimeCalc
    #define memcmp_idx_type uint8_t  // if you want more than 255 commands with wcc change this to uint16_t
    #define num_memcmp_ranges_type uint8_t // if you want more than 255 memcmp ranges in one command (default is 5)
    #define memcmp_ranges_type uint8_t // if your commands are longer than 255, change this to uint16_t    
    
    // UI_ALL_WCC_CMD UserInput::_calcCmdMemcmpRanges and UserInput::_compareCommandToString specific (magic number!)
    #define UI_ALL_WCC_CMD ((memcmp_ranges_type)-1) // this should be the MAX of the containing array    

    // config error checking

    #if UI_MAX_ARGS > UINT8_MAX && UI_MAX_ARGS < UINT16_MAX
        #undef max_command_type
        #define max_command_type uint16_t
        #warning max_command_type type changed from uint8_t to uint16_t __FILE__ at __LINE__
    #elif UI_MAX_ARGS > UINT16_MAX && UI_MAX_ARGS < UINT32_MAX
        #undef max_command_type
        #define max_command_type uint32_t
        #warning max_command_type type changed from uint8_t to uint32_t __FILE__ at __LINE__
    #elif UI_MAX_ARGS > UINT32_MAX
        #error UI_MAX_ARGS cannot be greater than UINT32_MAX __FILE__ at __LINE__
    #endif // end UI_MAX_ARGS
    
    #if UI_MAX_DEPTH > UINT8_MAX && UI_MAX_DEPTH < UINT16_MAX
        #undef tree_depth_type
        #define tree_depth_type uint16_t
        #warning tree_depth_type type changed from uint8_t to uint16_t __FILE__ at __LINE__
    #elif UI_MAX_DEPTH > UINT16_MAX && UI_MAX_DEPTH < UINT32_MAX
        #undef tree_depth_type
        #define tree_depth_type uint32_t
        #warning tree_depth_type type changed from uint8_t to uint32_t __FILE__ at __LINE__
    #elif UI_MAX_DEPTH > UINT32_MAX
        #error UI_MAX_DEPTH cannot be greater than UINT32_MAX __FILE__ at __LINE__
    #endif // end UI_MAX_DEPTH

    #if UI_MAX_SUBCOMMANDS > UINT8_MAX && UI_MAX_SUBCOMMANDS < UINT16_MAX
        #undef sub_commands_type
        #define sub_commands_type uint16_t
        #warning tree_depth_type type changed from uint8_t to uint16_t __FILE__ at __LINE__
    #elif UI_MAX_SUBCOMMANDS > UINT16_MAX && UI_MAX_SUBCOMMANDS < UINT32_MAX
        #undef sub_commands_type
        #define sub_commands_type uint32_t
        #warning tree_depth_type type changed from uint8_t to uint32_t __FILE__ at __LINE__
    #elif UI_MAX_SUBCOMMANDS > UINT32_MAX
        #error UI_MAX_SUBCOMMANDS cannot be greater than UINT32_MAX __FILE__ at __LINE__
    #endif // end UI_MAX_SUBCOMMANDS

    #if UI_MAX_CMD_LEN > UINT8_MAX && UI_MAX_CMD_LEN < UINT16_MAX
        #undef command_length_type
        #define command_length_type uint16_t
        #warning command_length_type type changed from uint8_t to uint16_t __FILE__ at __LINE__
    #elif UI_MAX_CMD_LEN > UINT16_MAX && UI_MAX_CMD_LEN < UINT32_MAX
        #undef command_length_type
        #define command_length_type uint32_t
        #warning command_length_type type changed from uint8_t to uint32_t __FILE__ at __LINE__   
    #elif UI_MAX_CMD_LEN > UINT32_MAX
        #error UI_MAX_SUBCOMMANDS cannot be greater than UINT32_MAX __FILE__ at __LINE__
    #endif // end UI_MAX_CMD_LEN

    #if UI_MAX_DELIM_SEQ > UINT8_MAX && UI_MAX_DELIM_SEQ < UINT16_MAX
        #undef delim_lens_type
        #define delim_lens_type uint16_t
        #warning delim_lens_type type changed from uint8_t to uint16_t __FILE__ at __LINE__
    #elif UI_MAX_DELIM_SEQ > UINT16_MAX && UI_MAX_DELIM_SEQ < UINT32_MAX
        #undef delim_lens_type
        #define delim_lens_type uint32_t
        #warning delim_lens_type type changed from uint8_t to uint32_t __FILE__ at __LINE__
    #elif UI_MAX_DELIM_SEQ > UINT32_MAX
        #error UI_MAX_DELIM_SEQ cannot be greater than UINT32_MAX __FILE__ at __LINE__
    #endif // end UI_MAX_DELIM_SEQ

    #if UI_MAX_START_STOP_SEQ > UINT8_MAX && UI_MAX_START_STOP_SEQ < UINT16_MAX
        #undef delim_lens_type
        #define delim_lens_type uint16_t
        #warning delim_lens_type type changed from uint8_t to uint16_t __FILE__ at __LINE__
    #elif UI_MAX_START_STOP_SEQ > UINT16_MAX && UI_MAX_START_STOP_SEQ < UINT32_MAX
        #undef delim_lens_type
        #define delim_lens_type uint32_t
        #warning delim_lens_type type changed from uint8_t to uint32_t __FILE__ at __LINE__
    #elif UI_MAX_START_STOP_SEQ > UINT32_MAX
        #error UI_MAX_START_STOP_SEQ cannot be greater than UINT32_MAX __FILE__ at __LINE__
    #endif // end UI_MAX_START_STOP_SEQ

    #if UI_MAX_IN_LEN > (UINT16_MAX - 2U)
        #warning UI_MAX_IN_LEN is large, InputHandler makes copies of the original buffer so this can use a lot of RAM __FILE__ at __LINE__
    #elif UI_MAX_IN_LEN > (UINT32_MAX - 2U)
        #error UI_MAX_IN_LEN cannot be greater than (UINT32_MAX - 2U) __FILE__ at __LINE__
    #endif // end UI_MAX_IN_LEN

    #if UI_MAX_PER_CMD_MEMCMP_RANGES > UINT8_MAX && UI_MAX_PER_CMD_MEMCMP_RANGES < UINT16_MAX
        #undef num_memcmp_ranges_type
        #define num_memcmp_ranges_type uint16_t
        #warning num_memcmp_ranges_type changed from uint8_t to uint16_t __FILE__ at __LINE__
    #elif UI_MAX_PER_CMD_MEMCMP_RANGES > UINT16_MAX && UI_MAX_PER_CMD_MEMCMP_RANGES < UINT32_MAX
        #undef num_memcmp_ranges_type
        #define num_memcmp_ranges_type uint32_t
        #warning num_memcmp_ranges_type changed from uint8_t to uint32_t __FILE__ at __LINE__
    #elif UI_MAX_PER_CMD_MEMCMP_RANGES > UINT32_MAX
        #error UI_MAX_PER_CMD_MEMCMP_RANGES cannot be greater than (UINT32_MAX - 2U) __FILE__ at __LINE__
    #endif // end UI_MAX_PER_CMD_MEMCMP_RANGES
    // end config error checking

#endif // end include guard
// end of file
