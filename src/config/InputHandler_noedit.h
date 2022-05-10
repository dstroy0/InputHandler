/**
   @file InputHandler_noedit.h
   @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
   @brief InputHandler library C includes, buffer sizing macros
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

#if !defined(__INPUTHANDLER_NOEDIT_H__)
    #define __INPUTHANDLER_NOEDIT_H__
    
    #include <Arduino.h>
    #include "InputHandler_config.h"
    #include "InputHandler_portability.h"
    #include "InputHandler_functionlike_macros.h"
    #include "InputHandler_PROGMEM_settings.h"

    /*
        do not edit unless you know what will happen
    */
    #define UI_MAX_PER_CMD_MEMCMP_RANGES (UI_MAX_SUBCOMMANDS + 1) * 2 ///< UserInput::addCommand array sizing macro
    #define UI_ESCAPED_CHAR_STRLEN 3                                  ///< sram buffer size for a single escaped char, used by UserInput methods

#endif // end include guard
// end of file
