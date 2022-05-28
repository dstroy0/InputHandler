/**
   @file noedit.h
   @authors Douglas Quigg (dstroy0 dquigg123@gmail.com) and Brendan Doherty (2bndy5 2bndy5@gmail.com)
   @brief InputHandler library C includes, do not edit
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
    #include "config.h" // user config file
    #include "advanced_config.h" // advanced and debugging toggleable options

    /*
        DO NOT EDIT the sections below unless you know what will happen, incorrect entry
        can introduce undefined behavior.
    */

    // function-like macros
    #define nprms(x) (sizeof(x) / sizeof((x)[0])) ///< gets the number of elements in an array
    #define buffsz(x) nprms(x)                    ///< gets the number of elements in an array
    #define nelems(x) nprms(x)                    ///< gets the number of elements in an array
    #define S(x) #x                               ///< gnu direct # stringify macro
    #define STR(x) S(x)                           ///< gnu indirect # stringify macro
    // end function-like macros

    // file location directive    
    #define LOC __FILE__ : __LINE__ ///< direct non-stringified file and line macro
    #define LOCATION STR(LOC)       ///< indirect stringified file and line macro
    // end file location directive

    // portability directives
    #if defined(ARDUINO_SAMD_VARIANT_COMPLIANCE) ///< SAMD portability
        #include <avr/dtostrf.h>       // implement dtostrf
        #include "utility/vsnprintf.h" // implement vsnprintf
        #define vsnprintf_P vsnprintf  // this platform does not use vsnprintf_P
        #undef pgm_read_dword          // use a different macro for pgm_read_dword
        ///< PROGMEM fix macro
        #define pgm_read_dword(addr) ({     \
            typeof(addr) _addr = (addr);    \
            *(const unsigned long*)(_addr); \
        })
    #endif

    #if defined(__MBED_CONFIG_DATA__) ///< MBED portability
        #include <avr/dtostrf.h>       // implement dtostrf
        #include "utility/vsnprintf.h" // implement vsnprintf
        #define vsnprintf_P vsnprintf  // this platform does not use vsnprintf_P
        #undef pgm_read_dword          // use a different macro for pgm_read_dword
        ///< PROGMEM fix macro
        #define pgm_read_dword(addr) ({     \
            typeof(addr) _addr = (addr);    \
            *(const unsigned long*)(_addr); \
        })
    #endif

    #if defined(ARDUINO_SAM_DUE) ///< DUE portability
        #include <avr/dtostrf.h>       // implement dtostrf
        #include "utility/vsnprintf.h" // implement vsnprintf
        #define vsnprintf_P vsnprintf  // this platform does not use vsnprintf_P
        #undef pgm_read_dword          // use a different macro for pgm_read_dword
        ///< PROGMEM fix macro
        #define pgm_read_dword(addr) ({     \
            typeof(addr) _addr = (addr);    \
            *(const unsigned long*)(_addr); \
        })
    #endif

    #if defined(TEENSYDUINO) ///< teensy portability
        // pgm/ram section type conflict fix macros (fixes PROGMEM addressing)
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
    #define UI_ALL_WCC_CMD ((IH::ui_max_per_cmd_memcmp_ranges_t)-1) ///< UI_ALL_WCC_CMD is Type MAX

/**
 * @namespace IH
 * @brief "auto" type namespace
 *
 * auto type sizing macros, uses src/config.h as input
 */
namespace IH {

// CommandParameters related macros
typedef uint16_t cmd_id_grp_t;

// UserInput private member type
typedef bool input_type_match_flags_type;

// CommandRuntimeCalc
        // if you want more than 255 commands with wcc change this to uint16_t
//typedef uint8_t num_memcmp_ranges_type; // if you want more than 255 memcmp ranges in one command (default is 5)
//typedef uint8_t memcmp_ranges_type;     // if your commands are longer than 255, change this to uint16_t

// config error checking

    #if UI_MAX_COMMANDS_IN_TREE <= UINT8_MAX
        typedef uint8_t ui_max_commands_in_tree_t;
    #endif    
    #if UI_MAX_COMMANDS_IN_TREE > UINT8_MAX && UI_MAX_COMMANDS_IN_TREE <= UINT16_MAX
        typedef uint16_t ui_max_commands_in_tree_t; 
        #pragma message(" at " LOCATION)
        #warning UI_MAX_COMMANDS_IN_TREE|ui_max_commands_in_tree_t changed from uint8_t to uint16_t        
    #endif
    #if UI_MAX_COMMANDS_IN_TREE > UINT16_MAX && UI_MAX_COMMANDS_IN_TREE <= UINT32_MAX
        typedef uint32_t ui_max_commands_in_tree_t;
        #pragma message(" at " LOCATION)
        #warning UI_MAX_COMMANDS_IN_TREE|ui_max_commands_in_tree_t changed from uint8_t to uint32_t
    #endif
    #if UI_MAX_COMMANDS_IN_TREE > ((UINT32_MAX) - 1)
        #pragma message(" at " LOCATION)
        #error UI_MAX_COMMANDS_IN_TREE cannot be greater than UINT32_MAX
    #endif // end UI_MAX_COMMANDS_IN_TREE

    #if UI_MAX_ARGS_PER_COMMAND <= UINT8_MAX
        typedef uint8_t ui_max_args_t;
    #endif    
    #if UI_MAX_ARGS_PER_COMMAND > UINT8_MAX && UI_MAX_ARGS_PER_COMMAND <= UINT16_MAX
        typedef uint16_t ui_max_args_t; 
        #pragma message(" at " LOCATION)
        #warning UI_MAX_ARGS_PER_COMMAND|ui_max_args_t changed from uint8_t to uint16_t        
    #endif
    #if UI_MAX_ARGS_PER_COMMAND > UINT16_MAX && UI_MAX_ARGS_PER_COMMAND <= UINT32_MAX
        typedef uint32_t ui_max_args_t;
        #pragma message(" at " LOCATION)
        #warning UI_MAX_ARGS_PER_COMMAND|ui_max_args_t changed from uint8_t to uint32_t
    #endif
    #if UI_MAX_ARGS_PER_COMMAND > ((UINT32_MAX) - 1)
        #pragma message(" at " LOCATION)
        #error UI_MAX_ARGS_PER_COMMAND cannot be greater than UINT32_MAX
    #endif // end UI_MAX_ARGS_PER_COMMAND

    #if UI_MAX_TREE_DEPTH_PER_COMMAND <= UINT8_MAX
        typedef uint8_t ui_max_tree_depth_per_command_t;
    #endif    
    #if UI_MAX_TREE_DEPTH_PER_COMMAND > UINT8_MAX && UI_MAX_TREE_DEPTH_PER_COMMAND <= UINT16_MAX
        typedef uint16_t ui_max_tree_depth_per_command_t; 
        #pragma message(" at " LOCATION)
        #warning UI_MAX_TREE_DEPTH_PER_COMMAND|ui_max_args_t changed from uint8_t to uint16_t        
    #endif
    #if UI_MAX_TREE_DEPTH_PER_COMMAND > UINT16_MAX && UI_MAX_TREE_DEPTH_PER_COMMAND <= UINT32_MAX
        typedef uint32_t ui_max_tree_depth_per_command_t;
        #pragma message(" at " LOCATION)
        #warning UI_MAX_TREE_DEPTH_PER_COMMAND|ui_max_args_t changed from uint8_t to uint32_t
    #endif
    #if UI_MAX_TREE_DEPTH_PER_COMMAND > ((UINT32_MAX) - 1)
        #pragma message(" at " LOCATION)
        #error UI_MAX_TREE_DEPTH_PER_COMMAND cannot be greater than UINT32_MAX
    #endif // end UI_MAX_TREE_DEPTH_PER_COMMAND

    #if UI_MAX_NUM_CHILD_COMMANDS <= UINT8_MAX
        typedef uint8_t ui_max_num_child_commands_t;        
    #endif
    #if UI_MAX_NUM_CHILD_COMMANDS > UINT8_MAX && UI_MAX_NUM_CHILD_COMMANDS <= UINT16_MAX
        typedef uint16_t ui_max_num_child_commands_t;
        #pragma message(" at " LOCATION)
        #warning UI_MAX_NUM_CHILD_COMMANDS|ui_max_args_t changed from uint8_t to uint16_t
    #endif
    #if UI_MAX_NUM_CHILD_COMMANDS > UINT16_MAX && UI_MAX_NUM_CHILD_COMMANDS <= UINT32_MAX
        typedef uint32_t ui_max_num_child_commands_t;
        #pragma message(" at " LOCATION)
        #warning UI_MAX_NUM_CHILD_COMMANDS|ui_max_args_t changed from uint8_t to uint32_t
    #endif
    #if UI_MAX_NUM_CHILD_COMMANDS > ((UINT32_MAX)-1)
        #pragma message(" at " LOCATION)
        #error UI_MAX_NUM_CHILD_COMMANDS cannot be greater than UINT32_MAX
    #endif // end UI_MAX_NUM_CHILD_COMMANDS

    #if UI_MAX_CMD_LEN <= UINT8_MAX
        typedef uint8_t ui_max_cmd_len_t;
    #endif
    #if UI_MAX_CMD_LEN > UINT8_MAX && UI_MAX_CMD_LEN <= UINT16_MAX
        typedef uint16_t ui_max_cmd_len_t;
        #pragma message(" at " LOCATION)
        #warning UI_MAX_CMD_LEN|ui_max_cmd_len_t changed from uint8_t to uint16_t
    #endif
    #if UI_MAX_CMD_LEN > UINT16_MAX && UI_MAX_CMD_LEN <= UINT32_MAX
        typedef uint32_t ui_max_cmd_len_t;
        #pragma message(" at " LOCATION)
        #warning UI_MAX_CMD_LEN|ui_max_cmd_len_t changed from uint8_t to uint32_t
    #endif
    #if UI_MAX_CMD_LEN > ((UINT32_MAX)-1)
        #pragma message(" at " LOCATION)
        #error UI_MAX_CMD_LEN cannot be greater than UINT32_MAX
    #endif // end UI_MAX_CMD_LEN

    #if UI_MAX_NUM_DELIM_SEQ <= UINT8_MAX
        typedef uint8_t ui_max_num_delim_seq_t;
    #endif
    #if UI_MAX_NUM_DELIM_SEQ > UINT8_MAX && UI_MAX_NUM_DELIM_SEQ <= UINT16_MAX
        typedef uint16_t ui_max_num_delim_seq_t;
        #pragma message(" at " LOCATION)
        #warning UI_MAX_NUM_DELIM_SEQ|ui_max_num_delim_seq_t changed from uint8_t to uint16_t
    #endif
    #if UI_MAX_NUM_DELIM_SEQ > UINT16_MAX && UI_MAX_NUM_DELIM_SEQ <= UINT32_MAX
        typedef uint32_t ui_max_num_delim_seq_t;
        #pragma message(" at " LOCATION)
        #warning UI_MAX_NUM_DELIM_SEQ|ui_max_num_delim_seq_t changed from uint8_t to uint32_t
    #endif
    #if UI_MAX_NUM_DELIM_SEQ > ((UINT32_MAX)-1)
        #pragma message(" at " LOCATION)
        #error UI_MAX_NUM_DELIM_SEQ cannot be greater than UINT32_MAX
    #endif // end UI_MAX_NUM_DELIM_SEQ

    #if UI_MAX_NUM_START_STOP_SEQ <= UINT8_MAX
        typedef uint8_t ui_max_num_start_stop_seq_t;
    #endif
    #if UI_MAX_NUM_START_STOP_SEQ > UINT8_MAX && UI_MAX_NUM_START_STOP_SEQ <= UINT16_MAX
        typedef uint16_t ui_max_num_start_stop_seq_t;
        #pragma message(" at " LOCATION)
        #warning UI_MAX_NUM_START_STOP_SEQ|ui_max_num_start_stop_seq_t changed from uint8_t to uint16_t
    #endif
    #if UI_MAX_NUM_START_STOP_SEQ > UINT16_MAX && UI_MAX_NUM_START_STOP_SEQ <= UINT32_MAX
        typedef uint32_t ui_max_num_start_stop_seq_t;
        #pragma message(" at " LOCATION)
        #warning UI_MAX_NUM_START_STOP_SEQ|ui_max_num_start_stop_seq_t changed from uint8_t to uint32_t
    #endif
    #if UI_MAX_NUM_START_STOP_SEQ > ((UINT32_MAX)-1)
        #pragma message(" at " LOCATION)
        #error UI_MAX_NUM_START_STOP_SEQ cannot be greater than UINT32_MAX
    #endif // end UI_MAX_NUM_START_STOP_SEQ

    #if UI_MAX_INPUT_LEN <= UINT8_MAX
        typedef uint8_t ui_max_input_len_t;
    #endif
    #if UI_MAX_INPUT_LEN > UINT8_MAX && UI_MAX_INPUT_LEN <= UINT16_MAX
        typedef uint16_t ui_max_input_len_t;
        #pragma message(" at " LOCATION)
        #warning UI_MAX_INPUT_LEN|ui_max_input_len_t changed from uint8_t to uint16_t
    #endif
    #if UI_MAX_INPUT_LEN > UINT16_MAX && UI_MAX_INPUT_LEN <= UINT32_MAX
        typedef uint32_t ui_max_input_len_t;
        #pragma message(" at " LOCATION)
        #warning UI_MAX_INPUT_LEN|ui_max_input_len_t changed from uint8_t to uint32_t
    #endif
    #if UI_MAX_INPUT_LEN > ((UINT32_MAX)-1)
        #pragma message(" at " LOCATION)
        #error UI_MAX_INPUT_LEN cannot be greater than UINT32_MAX
    #endif // end UI_MAX_INPUT_LEN

    #if UI_MAX_PER_CMD_MEMCMP_RANGES <= UINT8_MAX
        typedef uint8_t ui_max_per_cmd_memcmp_ranges_t;
        typedef uint8_t memcmp_idx_t;
    #endif
    #if UI_MAX_PER_CMD_MEMCMP_RANGES > UINT8_MAX && UI_MAX_PER_CMD_MEMCMP_RANGES <= UINT16_MAX
        typedef uint16_t ui_max_per_cmd_memcmp_ranges_t;
        typedef uint16_t memcmp_idx_t;
        #pragma message(" at " LOCATION)
        #warning UI_MAX_PER_CMD_MEMCMP_RANGES|ui_max_per_cmd_memcmp_ranges_t, memcmp_idx_t changed from uint8_t to uint16_t
    #endif
    #if UI_MAX_PER_CMD_MEMCMP_RANGES > UINT16_MAX && UI_MAX_PER_CMD_MEMCMP_RANGES <= UINT32_MAX
        typedef uint32_t ui_max_per_cmd_memcmp_ranges_t;
        typedef uint32_t memcmp_idx_t;
        #pragma message(" at " LOCATION)
        #warning UI_MAX_PER_CMD_MEMCMP_RANGES|ui_max_per_cmd_memcmp_ranges_t, memcmp_idx_t changed from uint8_t to uint32_t
    #endif
    #if UI_MAX_PER_CMD_MEMCMP_RANGES > ((UINT32_MAX)-1)
        #pragma message(" at " LOCATION)
        #error UI_MAX_PER_CMD_MEMCMP_RANGES cannot be greater than UINT32_MAX
    #endif // end UI_MAX_PER_CMD_MEMCMP_RANGES

// end config error checking
} // end namespace IH
#endif // end include guard
// end of file
