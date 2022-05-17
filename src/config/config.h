/**
   @file config.h
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
    #endif

    // error checking
    #if UI_MAX_ARGS > 255
        #error UI_MAX_ARGS MAX == 255
    #endif

    //  maximum tree depth
    #if !defined(UI_MAX_DEPTH)
        /*
           max is 255
        */
        #define UI_MAX_DEPTH 32
    #endif

    // error checking
    #if UI_MAX_DEPTH > 255
        #error UI_MAX_DEPTH MAX == 255
    #endif

    //  maximum number of subcommands that a command can branch to
    #if !defined(UI_MAX_SUBCOMMANDS)
        /*
           max is 255
        */
        #define UI_MAX_SUBCOMMANDS 32
    #endif

    // error checking
    #if UI_MAX_SUBCOMMANDS > 255
        #error UI_MAX_SUBCOMMANDS MAX == 255
    #endif

    //  maximum command/subcommand char length
    #if !defined(UI_MAX_CMD_LEN)
        /*
           max is 255
        */
        #define UI_MAX_CMD_LEN 32
    #endif

    // error checking
    #if UI_MAX_CMD_LEN > 255
        #error UI_MAX_CMD_LEN MAX == 255
    #endif

    // maximum number of delimiter sequences
    #if !defined(UI_MAX_DELIM_SEQ)
        /*
           max is 255
        */
        #define UI_MAX_DELIM_SEQ 5
    #endif

    // error checking
    #if UI_MAX_DELIM_SEQ > 255
        #error UI_MAX_DELIM_SEQ MAX == 255
    #endif

    // maximum number of start stop sequence len
    #if !defined(UI_MAX_START_STOP_SEQ)
        /*
           max is 255
        */
        #define UI_MAX_START_STOP_SEQ 5
    #endif

    // error checking
    #if UI_MAX_START_STOP_SEQ > 255
        #error UI_MAX_START_STOP_SEQ MAX == 255
    #endif

    //  maximum user input length
    #if !defined(UI_MAX_IN_LEN)
        /*
           max is 65535 - 2
           change to (UINT32_MAX - 2) POTENTIALLY LOTS OF RAM!!!
           to increase UI_MAX_IN_LEN (2^32) - 2
        */
        #define UI_MAX_IN_LEN (UINT16_MAX - 2U)
    #endif

    // error checking
    #if UI_MAX_IN_LEN > 65533
        #error UI_MAX_IN_LEN MAX exceeded
    #endif // end UI_MAX_IN_LEN

#endif // end include guard
// end of file
