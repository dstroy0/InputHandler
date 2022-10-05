/**
   @file noedit.h
   @authors Douglas Quigg (dstroy0 dquigg123@gmail.com) and Brendan Doherty (2bndy5 2bndy5@gmail.com)
   @brief InputHandler library C includes, do not edit
   @version 1.1
   @date 2022-05-28

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

    /*
        DO NOT EDIT the sections below unless you know what will happen, incorrect entry
        can introduce undefined behavior.
    */
    #include <Arduino.h>

    // function-like macros
    #define nprms(x) (sizeof(x) / sizeof((x)[0])) ///< gets the number of elements in an array 
    #define buffsz(x) nprms(x)                    ///< gets the number of elements in an array 
    #define nelems(x) nprms(x)                    ///< gets the number of elements in an array 
    #define S(s) #s                               ///< gnu direct # stringify macro 
    #define STR(s) S(s)                           ///< gnu indirect # stringify macro     
    // file location directive
    #define LOC                                                                                                                                                                              \
    __FILE__:                                                                                                                                                                                \
        __LINE__              ///< direct non-stringified file and line macro 
    #define LOCATION STR(LOC) ///< indirect stringified file and line macro 
    // end file location directive
    /**
     * @brief InputHandler MBED platform preprocessor setting; default is `#error`, on MBED platforms it is `#warn`
     * 
     * This is to remove some spurious `#error`'s being thrown by the MBED C preprocessor.
     * High probability of deprecation.
     * 
     */
    #define IH_MBED_PREPROC_COMPAT #error
    // end function-like macros

    // portability directives
    /**
     * @brief arduino samd compatibility
     * 
     */
    #if defined(ARDUINO_SAMD_VARIANT_COMPLIANCE) ///< SAMD portability 
        #include "utility/vsnprintf.h"           // implement vsnprintf
        #include <avr/dtostrf.h>                 // implement dtostrf

        #define vsnprintf_P vsnprintf // this platform does not use vsnprintf_P
        #undef pgm_read_dword         // use a different macro for pgm_read_dword
        ///< PROGMEM fix macro 
        #define pgm_read_dword(addr)                                                                                                                                                         \
            ({                                                                                                                                                                               \
                typeof(addr) _addr = (addr);                                                                                                                                                 \
                *(const unsigned long*)(_addr);                                                                                                                                              \
            })
    #endif

    /**
     * @brief arduino mbed compatibility
     * 
     */
    #if defined(__MBED_CONFIG_DATA__) ///< MBED portability 
        #undef IH_MBED_PREPROC_COMPAT // so special
        #define IH_MBED_PREPROC_COMPAT #warn
        #include "utility/vsnprintf.h" // implement vsnprintf
        #include <avr/dtostrf.h>       // implement dtostrf

        #define vsnprintf_P vsnprintf // this platform does not use vsnprintf_P
        #undef pgm_read_dword         // use a different macro for pgm_read_dword
        ///< PROGMEM fix macro 
        #define pgm_read_dword(addr)                                                                                                                                                         \
            ({                                                                                                                                                                               \
                typeof(addr) _addr = (addr);                                                                                                                                                 \
                *(const unsigned long*)(_addr);                                                                                                                                              \
            })
    #endif

    /**
     * @brief arduino sam compatibility
     * 
     */
    #if defined(ARDUINO_SAM_DUE)       ///< DUE portability 
        #include "utility/vsnprintf.h" // implement vsnprintf
        #include <avr/dtostrf.h>       // implement dtostrf

        #define vsnprintf_P vsnprintf // this platform does not use vsnprintf_P
        #undef pgm_read_dword         // use a different macro for pgm_read_dword
        ///< PROGMEM fix macro 
        #define pgm_read_dword(addr)                                                                                                                                                         \
            ({                                                                                                                                                                               \
                typeof(addr) _addr = (addr);                                                                                                                                                 \
                *(const unsigned long*)(_addr);                                                                                                                                              \
            })
    #endif

    /**
     * @brief teensy platform compatibility
     * 
     */
    #if defined(TEENSYDUINO) ///< teensy portability 
        // pgm/ram section type conflict fix macros (fixes PROGMEM addressing)
        #define QUO(x) #x
        #define QLINE(x, y)                                                                                                                                                                  \
            QUO(x)                                                                                                                                                                           \
            QUO(y)
        #define PFIX QLINE(.progmem.variable, __COUNTER__)
        #undef PROGMEM
        #define PROGMEM __attribute__((section(PFIX)))
    #endif
// end portability directives

    /**
     * @brief Doxygen docs are being built if DOXYGEN_XML_BUILD is defined
     * 
     */
    #if defined(DOXYGEN_XML_BUILD)
        #define UI_ECHO_ONLY 1
        #define DEBUG_GETCOMMANDFROMSTREAM 1
        #define DEBUG_READCOMMANDFROMBUFFER 1
        #define DEBUG_GET_TOKEN 1
        #define DEBUG_SUBCOMMAND_SEARCH 1
        #define DEBUG_ADDCOMMAND 1
        #define DEBUG_LAUNCH_LOGIC 1
        #define DEBUG_LAUNCH_FUNCTION 1
        #define DEBUG_INCLUDE_FREERAM 1
        #define DISABLE_listSettings 1
        #define DISABLE_listCommands 1
        #define DISABLE_getCommandFromStream 1
        #define DISABLE_nextArgument 1
        #define DISABLE_getArgument 1
        #define DISABLE_outputIsAvailable 1
        #define DISABLE_outputIsEnabled 1
        #define DISABLE_outputToStream 1
        #define DISABLE_clearOutputBuffer 1
        #define DISABLE_readCommandFromBufferErrorOutput 1
        #define DISABLE_ui_out 1
    #endif
    
    #include "config.h" // user config file

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
 * "auto" type sizing macros, uses src/config.h as input
 *
 * The idea behind this namespace is to let users set config.h items to
 * whatever they want, sizing variables for the least amount of space, automatically.
 * The preprocessor evaluates the if macros in a way that will leave typedefs that
 * size type aliases to the minimum byte-width required automatically.  It also warns users
 * about the change.  The only hand-holding that happens is for type sizing, it's up
 * to you to make sure you have the resources for your settings.
 * A very convenient feature for users.
 */
namespace IH
{
// UserInput private member type (future bit array)
typedef bool input_type_match_flags_type;

// config error checking
    #if UI_MAX_COMMANDS_IN_TREE <= UINT8_MAX
typedef uint8_t ui_max_commands_in_tree_t;
typedef uint8_t cmd_id_grp_t;
    #endif
    #if UI_MAX_COMMANDS_IN_TREE > UINT8_MAX && UI_MAX_COMMANDS_IN_TREE <= UINT16_MAX
typedef uint16_t ui_max_commands_in_tree_t;
typedef uint16_t cmd_id_grp_t;
        #pragma message(" at " LOCATION)
        #warning UI_MAX_COMMANDS_IN_TREE|ui_max_commands_in_tree_t, cmd_id_grp_t changed from uint8_t to uint16_t
    #endif
    #if UI_MAX_COMMANDS_IN_TREE > UINT16_MAX && UI_MAX_COMMANDS_IN_TREE <= UINT32_MAX
typedef uint32_t ui_max_commands_in_tree_t;
typedef uint32_t cmd_id_grp_t;
        #pragma message(" at " LOCATION)
        #warning UI_MAX_COMMANDS_IN_TREE|ui_max_commands_in_tree_t, cmd_id_grp_t changed from uint8_t to uint32_t
    #endif
    #if UI_MAX_COMMANDS_IN_TREE > ((UINT32_MAX)-1)
        #pragma message(" at " LOCATION)
IH_MBED_PREPROC_COMPAT UI_MAX_COMMANDS_IN_TREE cannot be greater than UINT32_MAX
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
    #if UI_MAX_ARGS_PER_COMMAND > ((UINT32_MAX)-1)
        #pragma message(" at " LOCATION)
IH_MBED_PREPROC_COMPAT UI_MAX_ARGS_PER_COMMAND cannot be greater than UINT32_MAX
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
    #if UI_MAX_TREE_DEPTH_PER_COMMAND > ((UINT32_MAX)-1)
        #pragma message(" at " LOCATION)
IH_MBED_PREPROC_COMPAT UI_MAX_TREE_DEPTH_PER_COMMAND cannot be greater than UINT32_MAX
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
IH_MBED_PREPROC_COMPAT UI_MAX_NUM_CHILD_COMMANDS cannot be greater than UINT32_MAX
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
IH_MBED_PREPROC_COMPAT UI_MAX_CMD_LEN cannot be greater than UINT32_MAX
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
IH_MBED_PREPROC_COMPAT UI_MAX_NUM_DELIM_SEQ cannot be greater than UINT32_MAX
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
IH_MBED_PREPROC_COMPAT UI_MAX_NUM_START_STOP_SEQ cannot be greater than UINT32_MAX
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
IH_MBED_PREPROC_COMPAT UI_MAX_INPUT_LEN cannot be greater than UINT32_MAX
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
IH_MBED_PREPROC_COMPAT UI_MAX_PER_CMD_MEMCMP_RANGES cannot be greater than UINT32_MAX
    #endif // end UI_MAX_PER_CMD_MEMCMP_RANGES
// end config error checking

} // end namespace IH

// optional method toggles
// LIBRARY OUTPUT
    #if !defined(UI_ECHO_ONLY)
        #define UI_VERBOSE
    #endif
  // end LIBRARY OUTPUT

    // DEBUGGING
    #if defined(DEBUG_GETCOMMANDFROMSTREAM)
        #define __DEBUG_GETCOMMANDFROMSTREAM__
    #endif
    #if defined(DEBUG_READCOMMANDFROMBUFFER)
        #define __DEBUG_READCOMMANDFROMBUFFER__
    #endif
    #if defined(DEBUG_GET_TOKEN)
        #define __DEBUG_GET_TOKEN__
    #endif
    #if defined(DEBUG_SUBCOMMAND_SEARCH)
        #define __DEBUG_SUBCOMMAND_SEARCH__
    #endif
    #if defined(DEBUG_ADDCOMMAND)
        #define __DEBUG_ADDCOMMAND__
    #endif
    #if defined(DEBUG_LAUNCH_LOGIC)
        #define __DEBUG_LAUNCH_LOGIC__
    #endif
    #if defined(DEBUG_LAUNCH_FUNCTION)
        #define __DEBUG_LAUNCH_FUNCTION__
    #endif
    #if defined(DEBUG_INCLUDE_FREERAM)
        #include "utility/freeRam.h"
    #endif
  // end DEBUGGING

    // OPTIONAL METHODS
    #if !defined(DISABLE_listSettings) // public methods
        #define ENABLE_listSettings
    #endif
    #if !defined(DISABLE_listCommands)
        #define ENABLE_listCommands
    #endif
    #if !defined(DISABLE_getCommandFromStream)
        #define ENABLE_getCommandFromStream
    #endif
    #if !defined(DISABLE_nextArgument)
        #define ENABLE_nextArgument
    #endif
    #if !defined(DISABLE_getArgument)
        #define ENABLE_getArgument
    #endif
    #if !defined(DISABLE_outputIsAvailable)
        #define ENABLE_outputIsAvailable
    #endif
    #if !defined(DISABLE_outputIsEnabled)
        #define ENABLE_outputIsEnabled
    #endif
    #if !defined(DISABLE_outputToStream)
        #define ENABLE_outputToStream
    #endif
    #if !defined(DISABLE_clearOutputBuffer)
        #define ENABLE_clearOutputBuffer
    #endif // end public methods
    #if !defined(DISABLE_readCommandFromBufferErrorOutput) // private methods
        #define ENABLE_readCommandFromBufferErrorOutput
    #endif
    #if !defined(DISABLE_ui_out) // disables all output, even if you have an output buffer defined
        #define ENABLE_ui_out
    #endif // end private methods
  // end OPTIONAL METHODS

// end optional method toggles

#endif // end include guard
// end of file
