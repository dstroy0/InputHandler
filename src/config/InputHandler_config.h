/**
   @file InputHandler_config.h
   @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
   @brief InputHandler library user configurable items
   @version 1.0
   @date 2022-03-02

   @copyright Copyright (c) 2022
*/
/*
 Copyright (C) 2022 Douglas Quigg (dstroy0) <dquigg123@gmail.com>

 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU General Public License
 version 3 as published by the Free Software Foundation.
 */

#ifndef __USER_INPUT_HANDLER_CONFIG_H__
    #define __USER_INPUT_HANDLER_CONFIG_H__

    /*
        User Configurable items
    */

    //  maximum number of arguments per command
    #if !defined(UI_MAX_ARGS)
        /*
          max is 255
        */
        #define UI_MAX_ARGS 32
    #else
        #error UI_MAX_ARGS already defined in __FILE__ at line (__LINE__ - 2)
    #endif

    //  maximum tree depth
    #if !defined(UI_MAX_DEPTH)
        /*
           max is 255
        */
        #define UI_MAX_DEPTH 32
    #else
        #error UI_MAX_DEPTH already defined in __FILE__ at line (__LINE__ - 2)
    #endif

    //  maximum number of subcommands that a command can branch to
    #if !defined(UI_MAX_SUBCOMMANDS)
        /*
           max is 255
        */
        #define UI_MAX_SUBCOMMANDS 32
    #else
        #error UI_MAX_SUBCOMMANDS already defined in __FILE__ at line (__LINE__ - 2)
    #endif

    //  maximum command/subcommand char length
    #if !defined(UI_MAX_CMD_LEN)
        /*
           max is 255
        */
        #define UI_MAX_CMD_LEN 32
    #else
        #error UI_MAX_CMD_LEN already defined in __FILE__ at line (__LINE__ - 2)
    #endif // end UI_MAX_CMD_LEN

    // maximum number of delimiter sequences
    #if !defined(UI_MAX_DELIM_SEQ)
    /*
      max is 255, increas
    */
        #define UI_MAX_DELIM_SEQ 5
    #else
        #error UI_MAX_DELIM_SEQ already defined in __FILE__ at line (__LINE__ - 2)
    #endif // end UI_MAX_DELIM_SEQ

    // maximum number of start stop sequence pairs
    #if !defined(UI_MAX_START_STOP_SEQ)
        #define UI_MAX_START_STOP_SEQ 5
    #else
        #error UI_MAX_START_STOP_SEQ already defined in __FILE__ at line (__LINE__ - 2)
    #endif // end UI_MAX_DELIM_SEQ

    //  maximum user input length
    #if !defined(UI_MAX_IN_LEN)
        /*
           max is 65535 - 2
           change to (UINT32_MAX - 2) POTENTIALLY LOTS OF RAM!!!
           to increase UI_MAX_IN_LEN (2^32) - 2
        */
        #define UI_MAX_IN_LEN (UINT16_MAX - 2U)
    #else
        #error UI_MAX_IN_LEN already defined in __FILE__ at line (__LINE__ - 2)
    #endif // end UI_MAX_IN_LEN

    /*
        Debug
        uncomment for debug output from process methods
    */
    //#define __DEBUG_USER_INPUT__

    // uncomment which method(s) to debug
    #if defined(__DEBUG_USER_INPUT__)
    //#define __DEBUG_GETCOMMANDFROMSTREAM__
    //#define __DEBUG_READCOMMANDFROMBUFFER__
    //#define __DEBUG_GET_TOKEN__
    //#define __DEBUG_SUBCOMMAND_SEARCH__
    //#define __DEBUG_ADDCOMMAND__
    //#define __DEBUG_LAUNCH_LOGIC__
    //#define __DEBUG_LAUNCH_FUNCTION__
    #endif // debug section

    /*
        Advanced

        optional methods, comment out to DISABLE and save some program space
        for your implementation, disabling these methods will break some examples
        some of these methods depend on other methods, 
    */
    
    //  public methods
    #define ENABLE_listSettings
    #define ENABLE_listCommands
    #define ENABLE_getCommandFromStream
    #define ENABLE_nextArgument
    #define ENABLE_getArgument
    #define ENABLE_outputIsAvailable
    #define ENABLE_outputIsEnabled
    #define ENABLE_outputToStream
    #define ENABLE_clearOutputBuffer
    // private methods
    #define ENABLE_readCommandFromBufferErrorOutput

#endif // end include guard
// end of file
