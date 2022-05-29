/**
   @file advanced_config.h
   @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
   @brief InputHandler library advanced user settings
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

#if !defined(__INPUTHANDLER_ADVANCED_CONFIG_H__)
    #define __INPUTHANDLER_ADVANCED_CONFIG_H__

/*
    library output
    switch this on/off by commenting/uncommenting the #define
*/    
    // #define UI_ECHO_ONLY

/*
    DEBUGGING
    switch these on/off by commenting/uncommenting the #define
*/
    // #define DEBUG_GETCOMMANDFROMSTREAM
    // #define DEBUG_READCOMMANDFROMBUFFER
    // #define DEBUG_GET_TOKEN
    // #define DEBUG_SUBCOMMAND_SEARCH
    // #define DEBUG_ADDCOMMAND
    // #define DEBUG_LAUNCH_LOGIC
    // #define DEBUG_LAUNCH_FUNCTION
    // #define DEBUG_INCLUDE_FREERAM

/*
    OPTIONAL METHODS
    switch these on/off by commenting/uncommenting the #define
*/
    // public methods
    // #define DISABLE_listSettings
    // #define DISABLE_listCommands
    // #define DISABLE_getCommandFromStream
    // #define DISABLE_nextArgument
    // #define DISABLE_getArgument
    // #define DISABLE_outputIsAvailable
    // #define DISABLE_outputIsEnabled
    // #define DISABLE_outputToStream
    // #define DISABLE_clearOutputBuffer
    
    // private methods
    // #define DISABLE_readCommandFromBufferErrorOutput
    // #define DISABLE_ui_out
#endif // include guard
// end of file
