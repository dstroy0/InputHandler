/**
 * @file noedit.h
 * @authors Douglas Quigg (dstroy0 dquigg123@gmail.com) and Brendan Doherty (2bndy5
 * 2bndy5@gmail.com)
 * @brief InputHandler library C includes, do not edit.
 * This file sets up your platform to use InputHandler and
 * sizes certain library variables based on what is found in
 * [src/config.h](https://github.com/dstroy0/InputHandler/blob/main/src/config/config.h).
 * @version 1.1
 * @date 2022-10-10
 *
 * @copyright Copyright (c) 2022
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

    // clang-format off
    // function-like macros
    #define nprms(x) (sizeof(x) / sizeof((x)[0])) ///< gets the number of elements in an array
    #define buffsz(x) nprms(x)                    ///< gets the number of elements in an array
    #define nelems(x) nprms(x)                    ///< gets the number of elements in an array
    #define S(s) #s                               ///< gnu direct # stringify macro
    #define STR(s) S(s)                           ///< gnu indirect # stringify macro
    // file location directive
    #define LOC __FILE__:__LINE__  ///< direct non-stringified file and line macro
    #define LOCATION STR(LOC)      ///< indirect stringified file and line macro
    // end file location directive    
    // "auto" Type macro        
    #define UI_ALL_WCC_CMD /** @cond */ ((IH::max_per_root_memcmp_ranges)-1) /** @endcond */ ///< UI_ALL_WCC_CMD MAX is equal to IH::max_per_root_memcmp_ranges - 1
    // end function-like macros
    // sizing macros
    #define UI_ESCAPED_CHAR_STRLEN /** @cond */ 3 /** @endcond */ ///< sram buffer size in bytes for a single escaped char
// clang-format on

    #if defined(DOXYGEN_XML_BUILD)
        /**
         * @brief Preprocessor directives and includes.
         *
         * Go to your platform's implementation to see what needs to be changed
         * to make the library work on your platform.
         *
         * [portability
         * directives](https://github.com/dstroy0/InputHandler/blob/main/src/config/noedit.h#:~:text=IH_PORTABILITY_DIRECTIVES)
         *
         */
        #define IH_PORTABILITY_DIRECTIVES
    #endif

    /** @cond */
    // portability directives
    #if defined(ARDUINO_SAMD_VARIANT_COMPLIANCE) // SAMD portability
        #include "utility/vsnprintf.h"           // implement vsnprintf
        #include <avr/dtostrf.h>                 // implement dtostrf

        #define vsnprintf_P vsnprintf // this platform does not use vsnprintf_P
        #undef pgm_read_dword         // use a different macro for pgm_read_dword
        // PROGMEM fix macro
        #define pgm_read_dword(addr)                                                               \
            ({                                                                                     \
                typeof(addr) _addr = (addr);                                                       \
                *(const unsigned long*)(_addr);                                                    \
            })

    #elif defined(__MBED_CONFIG_DATA__) // MBED portability
        #include "utility/vsnprintf.h"  // implement vsnprintf
        #include <avr/dtostrf.h>        // implement dtostrf

        #define vsnprintf_P vsnprintf // this platform does not use vsnprintf_P
        #undef pgm_read_dword         // use a different macro for pgm_read_dword
        // PROGMEM fix macro
        #define pgm_read_dword(addr)                                                               \
            ({                                                                                     \
                typeof(addr) _addr = (addr);                                                       \
                *(const unsigned long*)(_addr);                                                    \
            })

    #elif defined(ARDUINO_SAM_DUE)     // DUE portability
        #include "utility/vsnprintf.h" // implement vsnprintf
        #include <avr/dtostrf.h>       // implement dtostrf

        #define vsnprintf_P vsnprintf // this platform does not use vsnprintf_P
        #undef pgm_read_dword         // use a different macro for pgm_read_dword
        // PROGMEM fix macro
        #define pgm_read_dword(addr)                                                               \
            ({                                                                                     \
                typeof(addr) _addr = (addr);                                                       \
                *(const unsigned long*)(_addr);                                                    \
            })

    #elif defined(TEENSYDUINO) // teensy portability
        // pgm/ram section type conflict fix macros (fixes PROGMEM addressing)
        #define QUO(x) #x
        #define QLINE(x, y)                                                                        \
            QUO(x)                                                                                 \
            QUO(y)
        #define PFIX QLINE(.progmem.variable, __COUNTER__)
        #undef PROGMEM
        #define PROGMEM __attribute__((section(PFIX)))
    #endif
// end portability directives
/** @endcond */

    #include "config.h" // user config file

// clang-format off

// clang-format on

/**
 * @brief "auto" type namespace
 *
 * The source of macros in this namespace is src/config.h.
 * [config src](https://github.com/dstroy0/InputHandler/blob/main/src/config/config.h)
 * [namespace
 * src](https://github.com/dstroy0/InputHandler/blob/main/src/config/noedit.h#:~:text=namespace%20IH)
 *
 *
 * The idea behind this namespace is to let users set config.h items to
 * whatever they want, sizing variables for the least amount of space, automatically.
 * The preprocessor evaluates the if macros in a way that will leave typedefs that
 * size type aliases to the minimum byte-width required automatically.  It also warns users
 * about the change.  The only hand-holding that happens is for type sizing, it's up
 * to you to make sure you have the resources for your settings.
 * A very convenient feature for users.
 *
 *
 */
namespace IH
{
// UserInput private member type (future bit array)
typedef bool type_match_flags; ///< UserInput private member type (future bit array)

// UserInput variable sizing
    #if (IH_MAX_COMMANDS_PER_TREE <= UINT8_MAX) || defined(DOXYGEN_XML_BUILD)
/**
 * @brief User influenced typedef.
 *
 * @link IH_MAX_COMMANDS_PER_TREE @endlink is set by the user.
 *
 * @code{.c}
 * #if (IH_MAX_COMMANDS_PER_TREE <= UINT8_MAX)
 * typedef uint8_t max_cmds_per_tree;
 * #elif (IH_MAX_COMMANDS_PER_TREE > UINT8_MAX && IH_MAX_COMMANDS_PER_TREE <= UINT16_MAX)
 * typedef uint16_t max_cmds_per_tree;
 * #elif (IH_MAX_COMMANDS_PER_TREE > UINT16_MAX && IH_MAX_COMMANDS_PER_TREE <= UINT32_MAX)
 * typedef uint32_t max_cmds_per_tree;
 * #else
 * // no typedef; compile failure
 * #endif
 * @endcode
 */
typedef uint8_t max_cmds_per_tree;

/**
 * @brief User influenced typedef.
 *
 * @link IH_MAX_COMMANDS_PER_TREE @endlink is set by the user.
 *
 * @code{.c}
 * #if (IH_MAX_COMMANDS_PER_TREE <= UINT8_MAX)
 * typedef uint8_t cmd_id_grp;
 * #elif (IH_MAX_COMMANDS_PER_TREE > UINT8_MAX && IH_MAX_COMMANDS_PER_TREE <= UINT16_MAX)
 * typedef uint16_t cmd_id_grp;
 * #elif (IH_MAX_COMMANDS_PER_TREE > UINT16_MAX && IH_MAX_COMMANDS_PER_TREE <= UINT32_MAX)
 * typedef uint32_t cmd_id_grp;
 * #else
 * // no typedef; compile failure
 * #endif
 * @endcode
 */
typedef uint8_t cmd_id_grp;
    #elif (IH_MAX_COMMANDS_PER_TREE > UINT8_MAX && IH_MAX_COMMANDS_PER_TREE <= UINT16_MAX)
typedef uint16_t max_cmds_per_tree;
typedef uint16_t cmd_id_grp;
        #pragma message(" at " LOCATION)
        #warning IH_MAX_COMMANDS_PER_TREE|max_cmds_per_tree, cmd_id_grp changed from uint8_t to uint16_t
    #elif (IH_MAX_COMMANDS_PER_TREE > UINT16_MAX && IH_MAX_COMMANDS_PER_TREE <= UINT32_MAX)
typedef uint32_t max_cmds_per_tree;
typedef uint32_t cmd_id_grp;
        #pragma message(" at " LOCATION)
        #warning IH_MAX_COMMANDS_PER_TREE|max_cmds_per_tree, cmd_id_grp changed from uint8_t to uint32_t
    #elif (IH_MAX_COMMANDS_PER_TREE > ((UINT32_MAX)-1))
        #pragma message(" at " LOCATION)
        #warning IH_MAX_COMMANDS_PER_TREE greater than UINT32_MAX; behavior undefined, compilation should fail.
    #endif // end IH_MAX_COMMANDS_PER_TREE

    #if (IH_MAX_ARGS_PER_COMMAND <= UINT8_MAX) || defined(DOXYGEN_XML_BUILD)
/**
 * @brief User influenced typedef.
 *
 * @link IH_MAX_ARGS_PER_COMMAND @endlink is set by the user.
 * @code{.c}
 * #if (IH_MAX_ARGS_PER_COMMAND <= UINT8_MAX)
 * typedef uint8_t max_args_per_cmd;
 * #elif (IH_MAX_ARGS_PER_COMMAND > UINT8_MAX && IH_MAX_ARGS_PER_COMMAND <= UINT16_MAX)
 * typedef uint16_t max_args_per_cmd;
 * #elif (IH_MAX_ARGS_PER_COMMAND > UINT16_MAX && IH_MAX_ARGS_PER_COMMAND <= UINT32_MAX)
 * typedef uint32_t max_args_per_cmd;
 * #else
 * // no typedef; compile failure
 * #endif
 * @endcode
 */
typedef uint8_t max_args_per_cmd;
    #elif (IH_MAX_ARGS_PER_COMMAND > UINT8_MAX && IH_MAX_ARGS_PER_COMMAND <= UINT16_MAX)
typedef uint16_t max_args_per_cmd;
        #pragma message(" at " LOCATION)
        #warning IH_MAX_ARGS_PER_COMMAND|max_args_per_cmd changed from uint8_t to uint16_t
    #elif (IH_MAX_ARGS_PER_COMMAND > UINT16_MAX && IH_MAX_ARGS_PER_COMMAND <= UINT32_MAX)
typedef uint32_t max_args_per_cmd;
        #pragma message(" at " LOCATION)
        #warning IH_MAX_ARGS_PER_COMMAND|max_args_per_cmd changed from uint8_t to uint32_t
    #elif IH_MAX_ARGS_PER_COMMAND > ((UINT32_MAX)-1)
        #pragma message(" at " LOCATION)
        #warning IH_MAX_ARGS_PER_COMMAND greater than UINT32_MAX; behavior undefined, compilation should fail.
    #endif // end IH_MAX_ARGS_PER_COMMAND

    #if (IH_MAX_TREE_DEPTH_PER_COMMAND <= UINT8_MAX) || defined(DOXYGEN_XML_BUILD)
/**
 * @brief User influenced typedef.
 *
 * @link IH_MAX_TREE_DEPTH_PER_COMMAND @endlink is set by the user.
 *
 * @code{.c}
 * #if (IH_MAX_TREE_DEPTH_PER_COMMAND <= UINT8_MAX)
 * typedef uint8_t max_tree_depth_per_cmd;
 * #elif (IH_MAX_TREE_DEPTH_PER_COMMAND > UINT8_MAX && IH_MAX_TREE_DEPTH_PER_COMMAND <= UINT16_MAX)
 * typedef uint16_t max_tree_depth_per_cmd;
 * #elif (IH_MAX_TREE_DEPTH_PER_COMMAND > UINT16_MAX && IH_MAX_TREE_DEPTH_PER_COMMAND <= UINT32_MAX)
 * typedef uint32_t max_tree_depth_per_cmd;
 * #else
 * // no typedef; compile failure
 * #endif
 * @endcode
 */
typedef uint8_t max_tree_depth_per_cmd;
    #elif (IH_MAX_TREE_DEPTH_PER_COMMAND > UINT8_MAX && IH_MAX_TREE_DEPTH_PER_COMMAND <= UINT16_MAX)
typedef uint16_t max_tree_depth_per_cmd;
        #pragma message(" at " LOCATION)
        #warning IH_MAX_TREE_DEPTH_PER_COMMAND|max_args_per_cmd changed from uint8_t to uint16_t
    #elif (                                                                                        \
        IH_MAX_TREE_DEPTH_PER_COMMAND > UINT16_MAX && IH_MAX_TREE_DEPTH_PER_COMMAND <= UINT32_MAX)
typedef uint32_t max_tree_depth_per_cmd;
        #pragma message(" at " LOCATION)
        #warning IH_MAX_TREE_DEPTH_PER_COMMAND|max_args_per_cmd changed from uint8_t to uint32_t
    #elif (IH_MAX_TREE_DEPTH_PER_COMMAND > ((UINT32_MAX)-1))
        #pragma message(" at " LOCATION)
        #warning IH_MAX_TREE_DEPTH_PER_COMMAND cannot be greater than UINT32_MAX
    #endif // end IH_MAX_TREE_DEPTH_PER_COMMAND

    #if (IH_MAX_NUM_CHILD_COMMANDS_PER_ROOT <= UINT8_MAX) || defined(DOXYGEN_XML_BUILD)
/**
 * @brief User influenced typedef.
 *
 * @link IH_MAX_NUM_CHILD_COMMANDS_PER_ROOT @endlink is set by the user.
 *
 * @code{.c}
 * #if (IH_MAX_NUM_CHILD_COMMANDS_PER_ROOT <= UINT8_MAX)
 * typedef uint8_t max_num_child_cmds;
 * #elif (IH_MAX_NUM_CHILD_COMMANDS_PER_ROOT > UINT8_MAX && IH_MAX_NUM_CHILD_COMMANDS_PER_ROOT <=
 * UINT16_MAX) typedef uint16_t max_num_child_cmds; #elif
 * (IH_MAX_NUM_CHILD_COMMANDS_PER_ROOT > UINT16_MAX && IH_MAX_NUM_CHILD_COMMANDS_PER_ROOT <=
 * UINT32_MAX) typedef uint32_t max_num_child_cmds; #else
 * // no typedef; compile failure
 * #endif
 * @endcode
 */
typedef uint8_t max_num_child_cmds;
    #elif (IH_MAX_NUM_CHILD_COMMANDS_PER_ROOT > UINT8_MAX                                          \
        && IH_MAX_NUM_CHILD_COMMANDS_PER_ROOT <= UINT16_MAX)
typedef uint16_t max_num_child_cmds;
        #pragma message(" at " LOCATION)
        #warning IH_MAX_NUM_CHILD_COMMANDS_PER_ROOT|max_args_per_cmd changed from uint8_t to uint16_t
    #elif (IH_MAX_NUM_CHILD_COMMANDS_PER_ROOT > UINT16_MAX                                         \
        && IH_MAX_NUM_CHILD_COMMANDS_PER_ROOT <= UINT32_MAX)
typedef uint32_t max_num_child_cmds;
        #pragma message(" at " LOCATION)
        #warning IH_MAX_NUM_CHILD_COMMANDS_PER_ROOT|max_args_per_cmd changed from uint8_t to uint32_t
    #elif (IH_MAX_NUM_CHILD_COMMANDS_PER_ROOT > ((UINT32_MAX)-1))
        #pragma message(" at " LOCATION)
        #warning IH_MAX_NUM_CHILD_COMMANDS_PER_ROOT cannot be greater than UINT32_MAX
    #endif // end IH_MAX_NUM_CHILD_COMMANDS_PER_ROOT

    #if (IH_MAX_CMD_STR_LEN <= UINT8_MAX) || defined(DOXYGEN_XML_BUILD)
/**
 * @brief User influenced typedef.
 *
 * @link IH_MAX_CMD_STR_LEN @endlink is set by the user.
 *
 * @code{.c}
 * #if (IH_MAX_CMD_STR_LEN <= UINT8_MAX)
 * typedef uint8_t max_cmd_str_len;
 * #elif (IH_MAX_CMD_STR_LEN > UINT8_MAX && IH_MAX_CMD_STR_LEN <= UINT16_MAX)
 * typedef uint16_t max_cmd_str_len;
 * #elif (IH_MAX_CMD_STR_LEN > UINT16_MAX && IH_MAX_CMD_STR_LEN <= UINT32_MAX)
 * typedef uint32_t max_cmd_str_len;
 * #else
 * // no typedef; compile failure
 * #endif
 * @endcode
 */
typedef uint8_t max_cmd_str_len;
    #endif
    #if (IH_MAX_CMD_STR_LEN > UINT8_MAX && IH_MAX_CMD_STR_LEN <= UINT16_MAX)
typedef uint16_t max_cmd_str_len;
        #pragma message(" at " LOCATION)
        #warning IH_MAX_CMD_STR_LEN|max_cmd_str_len changed from uint8_t to uint16_t
    #endif
    #if (IH_MAX_CMD_STR_LEN > UINT16_MAX && IH_MAX_CMD_STR_LEN <= UINT32_MAX)
typedef uint32_t max_cmd_str_len;
        #pragma message(" at " LOCATION)
        #warning IH_MAX_CMD_STR_LEN|max_cmd_str_len changed from uint8_t to uint32_t
    #endif
    #if (IH_MAX_CMD_STR_LEN > ((UINT32_MAX)-1))
        #pragma message(" at " LOCATION)
        #warning IH_MAX_CMD_STR_LEN cannot be greater than UINT32_MAX
    #endif // end IH_MAX_CMD_STR_LEN

    #if (IH_MAX_NUM_PROC_DELIM_SEQ <= UINT8_MAX) || defined(DOXYGEN_XML_BUILD)
/**
 * @brief User influenced typedef.
 *
 * @link IH_MAX_NUM_PROC_DELIM_SEQ @endlink is set by the user.
 *
 * @code{.c}
 * #if (IH_MAX_NUM_PROC_DELIM_SEQ <= UINT8_MAX)
 * typedef uint8_t max_num_delim_seq;
 * #elif (IH_MAX_NUM_PROC_DELIM_SEQ > UINT8_MAX && IH_MAX_NUM_PROC_DELIM_SEQ <= UINT16_MAX)
 * typedef uint16_t max_num_delim_seq;
 * #elif (IH_MAX_NUM_PROC_DELIM_SEQ > UINT16_MAX && IH_MAX_NUM_PROC_DELIM_SEQ <= UINT32_MAX)
 * typedef uint32_t max_num_delim_seq;
 * #else
 * // no typedef; compile failure
 * #endif
 * @endcode
 */
typedef uint8_t max_num_delim_seq;
    #elif (IH_MAX_NUM_PROC_DELIM_SEQ > UINT8_MAX && IH_MAX_NUM_PROC_DELIM_SEQ <= UINT16_MAX)
typedef uint16_t max_num_delim_seq;
        #pragma message(" at " LOCATION)
        #warning IH_MAX_NUM_PROC_DELIM_SEQ|max_num_delim_seq changed from uint8_t to uint16_t
    #elif (IH_MAX_NUM_PROC_DELIM_SEQ > UINT16_MAX && IH_MAX_NUM_PROC_DELIM_SEQ <= UINT32_MAX)
typedef uint32_t max_num_delim_seq;
        #pragma message(" at " LOCATION)
        #warning IH_MAX_NUM_PROC_DELIM_SEQ|max_num_delim_seq changed from uint8_t to uint32_t
    #elif (IH_MAX_NUM_PROC_DELIM_SEQ > ((UINT32_MAX)-1))
        #pragma message(" at " LOCATION)
        #warning IH_MAX_NUM_PROC_DELIM_SEQ cannot be greater than UINT32_MAX
    #endif // end IH_MAX_NUM_PROC_DELIM_SEQ

    #if (IH_MAX_NUM_START_STOP_SEQ <= UINT8_MAX) || defined(DOXYGEN_XML_BUILD)
/**
 * @brief User influenced typedef.
 *
 * @link IH_MAX_NUM_START_STOP_SEQ @endlink is set by the user.
 *
 * @code{.c}
 * #if (IH_MAX_NUM_START_STOP_SEQ <= UINT8_MAX)
 * typedef uint8_t max_num_start_stop_seq;
 * #elif (IH_MAX_NUM_START_STOP_SEQ > UINT8_MAX && IH_MAX_NUM_START_STOP_SEQ <= UINT16_MAX)
 * typedef uint16_t max_num_start_stop_seq;
 * #elif (IH_MAX_NUM_START_STOP_SEQ > UINT16_MAX && IH_MAX_NUM_START_STOP_SEQ <= UINT32_MAX)
 * typedef uint32_t max_num_start_stop_seq;
 * #else
 * // no typedef; compile failure
 * #endif
 * @endcode
 */
typedef uint8_t max_num_start_stop_seq;
    #elif (IH_MAX_NUM_START_STOP_SEQ > UINT8_MAX && IH_MAX_NUM_START_STOP_SEQ <= UINT16_MAX)
typedef uint16_t max_num_start_stop_seq;
        #pragma message(" at " LOCATION)
        #warning IH_MAX_NUM_START_STOP_SEQ|max_num_start_stop_seq changed from uint8_t to uint16_t
    #elif (IH_MAX_NUM_START_STOP_SEQ > UINT16_MAX && IH_MAX_NUM_START_STOP_SEQ <= UINT32_MAX)
typedef uint32_t max_num_start_stop_seq;
        #pragma message(" at " LOCATION)
        #warning IH_MAX_NUM_START_STOP_SEQ|max_num_start_stop_seq changed from uint8_t to uint32_t
    #elif (IH_MAX_NUM_START_STOP_SEQ > ((UINT32_MAX)-1))
        #pragma message(" at " LOCATION)
        #warning IH_MAX_NUM_START_STOP_SEQ cannot be greater than UINT32_MAX
    #endif // end IH_MAX_NUM_START_STOP_SEQ

    #if (IH_MAX_PROC_INPUT_LEN <= UINT8_MAX) || defined(DOXYGEN_XML_BUILD)
/**
 * @brief User influenced typedef.
 *
 * @link IH_MAX_PROC_INPUT_LEN @endlink is set by the user.
 *
 * @code{.c}
 * #if (IH_MAX_PROC_INPUT_LEN <= UINT8_MAX)
 * typedef uint8_t max_proc_input_len;
 * #elif (IH_MAX_PROC_INPUT_LEN > UINT8_MAX && IH_MAX_PROC_INPUT_LEN <= UINT16_MAX)
 * typedef uint16_t max_proc_input_len;
 * #elif (IH_MAX_PROC_INPUT_LEN > UINT16_MAX && IH_MAX_PROC_INPUT_LEN <= UINT32_MAX)
 * typedef uint32_t max_proc_input_len;
 * #else
 * // no typedef; compile failure
 * #endif
 * @endcode
 */
typedef uint8_t max_proc_input_len;
    #elif (IH_MAX_PROC_INPUT_LEN > UINT8_MAX && IH_MAX_PROC_INPUT_LEN <= UINT16_MAX)
typedef uint16_t max_proc_input_len;
        #pragma message(" at " LOCATION)
        #warning IH_MAX_PROC_INPUT_LEN|max_proc_input_len changed from uint8_t to uint16_t
    #elif (IH_MAX_PROC_INPUT_LEN > UINT16_MAX && IH_MAX_PROC_INPUT_LEN <= UINT32_MAX)
typedef uint32_t max_proc_input_len;
        #pragma message(" at " LOCATION)
        #warning IH_MAX_PROC_INPUT_LEN|max_proc_input_len changed from uint8_t to uint32_t
    #elif (IH_MAX_PROC_INPUT_LEN > ((UINT32_MAX)-1))
        #pragma message(" at " LOCATION)
        #warning IH_MAX_PROC_INPUT_LEN cannot be greater than UINT32_MAX
    #endif // end IH_MAX_PROC_INPUT_LEN

    #if (IH_MAX_PER_ROOT_MEMCMP_RANGES <= UINT8_MAX) || defined(DOXYGEN_XML_BUILD)
/**
 * @brief User influenced typedef.
 *
 * @link IH_MAX_PER_ROOT_MEMCMP_RANGES @endlink is set by the user.
 *
 * @code{.c}
 * #if (IH_MAX_PER_ROOT_MEMCMP_RANGES <= UINT8_MAX)
 * typedef uint8_t max_per_root_memcmp_ranges;
 * #elif (IH_MAX_PER_ROOT_MEMCMP_RANGES > UINT8_MAX && IH_MAX_PER_ROOT_MEMCMP_RANGES <= UINT16_MAX)
 * typedef uint16_t max_per_root_memcmp_ranges;
 * #elif (IH_MAX_PER_ROOT_MEMCMP_RANGES > UINT16_MAX && IH_MAX_PER_ROOT_MEMCMP_RANGES <= UINT32_MAX)
 * typedef uint32_t max_per_root_memcmp_ranges;
 * #else
 * // no typedef; compile failure
 * #endif
 * @endcode
 */
typedef uint8_t max_per_root_memcmp_ranges;

/**
 * @brief User influenced typedef.
 *
 * @link IH_MAX_PER_ROOT_MEMCMP_RANGES @endlink is set by the user.
 *
 * @code{.c}
 * #if (IH_MAX_PER_ROOT_MEMCMP_RANGES <= UINT8_MAX)
 * typedef uint8_t memcmp_idx_t;
 * #elif (IH_MAX_PER_ROOT_MEMCMP_RANGES > UINT8_MAX && IH_MAX_PER_ROOT_MEMCMP_RANGES <= UINT16_MAX)
 * typedef uint16_t memcmp_idx_t;
 * #elif (IH_MAX_PER_ROOT_MEMCMP_RANGES > UINT16_MAX && IH_MAX_PER_ROOT_MEMCMP_RANGES <= UINT32_MAX)
 * typedef uint32_t memcmp_idx_t;
 * #else
 * // no typedef; compile failure
 * #endif
 * @endcode
 */
typedef uint8_t memcmp_idx_t;
    #elif (IH_MAX_PER_ROOT_MEMCMP_RANGES > UINT8_MAX && IH_MAX_PER_ROOT_MEMCMP_RANGES <= UINT16_MAX)
typedef uint16_t max_per_root_memcmp_ranges;
typedef uint16_t memcmp_idx_t;
        #pragma message(" at " LOCATION)
        #warning IH_MAX_PER_ROOT_MEMCMP_RANGES|max_per_root_memcmp_ranges, memcmp_idx_t changed from uint8_t to uint16_t
    #elif (                                                                                        \
        IH_MAX_PER_ROOT_MEMCMP_RANGES > UINT16_MAX && IH_MAX_PER_ROOT_MEMCMP_RANGES <= UINT32_MAX)
typedef uint32_t max_per_root_memcmp_ranges;
typedef uint32_t memcmp_idx_t;
        #pragma message(" at " LOCATION)
        #warning IH_MAX_PER_ROOT_MEMCMP_RANGES|max_per_root_memcmp_ranges, memcmp_idx_t changed from uint8_t to uint32_t
    #elif (IH_MAX_PER_ROOT_MEMCMP_RANGES > ((UINT32_MAX)-1))
        #pragma message(" at " LOCATION)
        #warning IH_MAX_PER_ROOT_MEMCMP_RANGES cannot be greater than UINT32_MAX
    #endif // end IH_MAX_PER_ROOT_MEMCMP_RANGES
// end typedef sizing
} // end namespace IH

/** @cond */
// optional method toggles
// LIBRARY OUTPUT
    #if !defined(IH_ECHO_ONLY)
        #define IH_VERBOSE
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
    #endif                                                 // end public methods
    #if !defined(DISABLE_readCommandFromBufferErrorOutput) // private methods
        #define ENABLE_readCommandFromBufferErrorOutput
    #endif
    #if !defined(DISABLE_ui_out) // disables all output, even if you have an output buffer defined
        #define ENABLE_ui_out
    #endif // end private methods
           // end OPTIONAL METHODS
// end optional method toggles
/** @endcond */
#endif // end include guard
// end of file
