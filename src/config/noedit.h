/**
 * @file noedit.h
 * @authors Douglas Quigg (dstroy0 dquigg123@gmail.com) and Brendan Doherty (2bndy5
 * 2bndy5@gmail.com)
 * @brief InputHandler library C includes, do not edit.
 * This file sets up your platform to use InputHandler and
 * sizes certain library variables based on what is found in
 * [src/config.h](https://github.com/dstroy0/InputHandler/blob/main/src/config/config.h).
 * @version 1.0.0
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

    // function-like macros
    // TODO make this less bad later
    #define TRM(x) ihc::terminal_strings[static_cast<int>(ihc::TRM::x)]
    #define CMD_ERR_MSG ihc::command_error_strings[static_cast<int>(ihc::CMD_ERR_IDX::command_string)]
    #define CMD_ERR(x) ihc::command_error_strings[static_cast<int>(ihc::CMD_ERR_IDX::x)]
    #define AE_CMD_ERR(x) ihc::command_error_strings[static_cast<int>(x)]
    #define ERR_TYP(x) ihc::error_type_strings[static_cast<int>(ihc::ERR_TYP::x)]
    #define ERR_MSG(x) ihc::error_message_strings[static_cast<int>(ihc::ERR_MSG::x)]
    #define VAR_ID(x) ihc::var_id_strings[static_cast<int>(ihc::VAR_ID::x)]
    #define FE_VAR_ID(x) ihc::var_id_strings[static_cast<int>(x)]
    #define nprms(x) (sizeof(x) / sizeof((x)[0])) ///< gets the number of elements in an array
    #define buffsz(x) nprms(x) ///< gets the number of elements in an array
    #define nelems(x) nprms(x) ///< gets the number of elements in an array

    #define S(s) #s ///< gnu direct # stringify macro
    #define STR(s) S(s) ///< gnu indirect # stringify macro
    // file location directive
    #define LOC                                                                                                                                                                                                                                \
    __FILE__:                                                                                                                                                                                                                                  \
        __LINE__ ///< direct non-stringified file and line macro
    #define LOCATION STR(LOC) ///< indirect stringified file and line macro
    // end file location directive
    // "auto" Type macro
    #define UI_ALL_WCC_CMD /** @cond */ ((ih_auto::max_per_root_memcmp_ranges)-1) /** @endcond */ ///< UI_ALL_WCC_CMD MAX is equal to ih_auto::max_per_root_memcmp_ranges - 1
    // clang-format off
    #define ih_pgm_read_dword(addr)                                                                                                                                                                                                            \
        ({                                                                                                                                                                                                                                     \
            typeof(addr) _addr = (addr);                                                                                                                                                                                                       \
            *(const unsigned long*)(_addr);                                                                                                                                                                                                    \
        })
    // clang-format on
    // end function-like macros
    // sizing macro
    #define UI_ESCAPED_CHAR_STRLEN /** @cond */ 3 /** @endcond */ ///< sram buffer size in bytes for a single escaped char

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
        #include "utility/vsnprintf.h" // implement vsnprintf
        #include <avr/dtostrf.h> // implement dtostrf

        #define vsnprintf_P vsnprintf // this platform does not use vsnprintf_P
        #undef pgm_read_dword // use a different macro for pgm_read_dword
        #define pgm_read_dword ih_pgm_read_dword

    #elif defined(__MBED_CONFIG_DATA__) // MBED portability
        #include "utility/vsnprintf.h" // implement vsnprintf
        #include <avr/dtostrf.h> // implement dtostrf

        #define vsnprintf_P vsnprintf // this platform does not use vsnprintf_P
        #undef pgm_read_dword // use a different macro for pgm_read_dword
        #define pgm_read_dword ih_pgm_read_dword

    #elif defined(ARDUINO_SAM_DUE) // DUE portability
        #include "utility/vsnprintf.h" // implement vsnprintf
        #include <avr/dtostrf.h> // implement dtostrf
        #define vsnprintf_P vsnprintf // this platform does not use vsnprintf_P
        #undef pgm_read_dword // use a different macro for pgm_read_dword
        #define pgm_read_dword ih_pgm_read_dword

    #elif defined(TEENSYDUINO) // teensy portability
        // pgm/ram section type conflict fix macros (fixes PROGMEM addressing)
        #define QUO(x) #x
        #define QLINE(x, y)                                                                                                                                                                                                                    \
            QUO(x)                                                                                                                                                                                                                             \
            QUO(y)
        #define PFIX QLINE(.progmem.variable, __COUNTER__)
        #undef PROGMEM
        #define PROGMEM __attribute__((section(PFIX)))

    #elif defined(NRF_H) // Nordic NRF portability
        #include "utility/vsnprintf.h" // implement vsnprintf
        #include <avr/dtostrf.h> // implement dtostrf
        #define snprintf_P snprintf
        #define vsnprintf_P vsnprintf // this platform does not use vsnprintf_P
        #undef pgm_read_dword // use a different macro for pgm_read_dword
        #define pgm_read_dword ih_pgm_read_dword

    #endif
// end portability directives
/** @endcond */

    #include "config.h" // user config file
    /** @cond */
    // optional method toggles
    // LIBRARY OUTPUT
    #if IH_ECHO_ONLY
        #define __UI_ECHO_ONLY__
    #endif
    #if IH_VERBOSE
        #define __UI_VERBOSE__
    #endif
    // end LIBRARY OUTPUT

    // DEBUGGING
    #if DEBUG_GETCOMMANDFROMSTREAM
        #define __DEBUG_GETCOMMANDFROMSTREAM__
    #endif
    #if DEBUG_READCOMMANDFROMBUFFER
        #define __DEBUG_READCOMMANDFROMBUFFER__
    #endif
    #if DEBUG_GET_TOKEN
        #define __DEBUG_GET_TOKEN__
    #endif
    #if DEBUG_SUBCOMMAND_SEARCH
        #define __DEBUG_SUBCOMMAND_SEARCH__
    #endif
    #if DEBUG_ADDCOMMAND
        #define __DEBUG_ADDCOMMAND__
    #endif
    #if DEBUG_LAUNCH_LOGIC
        #define __DEBUG_LAUNCH_LOGIC__
    #endif
    #if DEBUG_LAUNCH_FUNCTION
        #define __DEBUG_LAUNCH_FUNCTION__
    #endif
    #if DEBUG_INCLUDE_FREERAM
        #include "utility/freeRam.h"
    #endif
    // end DEBUGGING

    // OPTIONAL METHODS
    // public methods
    #if !DISABLE_listSettings
        #define ENABLE_listSettings
    #endif
    #if !DISABLE_listCommands
        #define ENABLE_listCommands
    #endif
    #if !DISABLE_getCommandFromStream
        #define ENABLE_getCommandFromStream
    #endif
    #if !DISABLE_nextArgument
        #define ENABLE_nextArgument
    #endif
    #if !DISABLE_getArgument
        #define ENABLE_getArgument
    #endif
    #if !DISABLE_outputIsAvailable
        #define ENABLE_outputIsAvailable
    #endif
    #if !DISABLE_outputIsEnabled
        #define ENABLE_outputIsEnabled
    #endif
    #if !DISABLE_outputToStream
        #define ENABLE_outputToStream
    #endif
    #if !DISABLE_clearOutputBuffer
        #define ENABLE_clearOutputBuffer
    #endif
    // end public methods
    // private methods
    #if !DISABLE_readCommandFromBufferErrorOutput
        #define ENABLE_readCommandFromBufferErrorOutput
    #endif
    #if !DISABLE_ihout // disables all output, even if you have an output buffer defined
        #define ENABLE_ihout
    #endif
// end private methods
// end OPTIONAL METHODS
/** @endcond */
    #include "utility/namespace.h" // lib specific namespaces
#endif // end include guard
// end of file
