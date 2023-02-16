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
    // TODO make this less bad later
    #define TRM(x) ihconst::terminal_strings[static_cast<int>(ihconst::TRM::x)]    
    #define CMD_ERR_MSG ihconst::command_error_strings[static_cast<int>(ihconst::CMD_ERR_IDX::command_string)]
    #define CMD_ERR(x) ihconst::command_error_strings[static_cast<int>(ihconst::CMD_ERR_IDX::x)]     
    #define ERR_TYP(x) ihconst::error_type_strings[static_cast<int>(ihconst::ERR_TYP::x)]
    #define ERR_MSG(x) ihconst::error_message_strings[static_cast<int>(ihconst::ERR_MSG::x)]
    #define VAR_ID(x) ihconst::var_id_strings[static_cast<int>(ihconst::VAR_ID::x)]
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
    #define UI_ALL_WCC_CMD /** @cond */ ((ih_auto_t::ui_max_per_cmd_memcmp_ranges_t)-1) /** @endcond */ ///< UI_ALL_WCC_CMD MAX is equal to ih_auto_t::ui_max_per_cmd_memcmp_ranges_t - 1
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

    #include "utility/namespace.h" // lib specific namespaces

/** @cond */
// optional method toggles
// LIBRARY OUTPUT
    #if defined(UI_ECHO_ONLY)
        #define __UI_ECHO_ONLY__
    // #define UI_VERBOSE
    #endif
    #if defined(UI_VERBOSE)
        #define __UI_VERBOSE__
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
