/**
 * @file config.h
 * @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
 * @brief InputHandler config.h
 * @version 1.0
 * @date 2023-02-13
 *
 * @copyright Copyright (c) 2023
 */
/*
 * Copyright (c) 2023 Douglas Quigg (dstroy0) <dquigg123@gmail.com>
 *
 * License: GNU GPL3
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * version 3 as published by the Free Software Foundation.
 */

#if !defined(__INPUTHANDLER_CONFIG_H__)
    #define __INPUTHANDLER_CONFIG_H__
    /*
        User Configurable items
    */
    #if !defined(IH_MAX_COMMANDS_PER_TREE)
        #define IH_MAX_COMMANDS_PER_TREE 32
    #endif
    #if !defined(IH_MAX_ARGS_PER_COMMAND)
        #define IH_MAX_ARGS_PER_COMMAND 32
    #endif
    #if !defined(IH_MAX_TREE_DEPTH_PER_COMMAND)
        #define IH_MAX_TREE_DEPTH_PER_COMMAND 32
    #endif
    #if !defined(IH_MAX_NUM_CHILD_COMMANDS_PER_ROOT)
        #define IH_MAX_NUM_CHILD_COMMANDS_PER_ROOT 32
    #endif
    #if !defined(IH_MAX_CMD_STR_LEN)
        #define IH_MAX_CMD_STR_LEN 32
    #endif
    #if !defined(IH_MAX_NUM_PROC_DELIM_SEQ)
        #define IH_MAX_NUM_PROC_DELIM_SEQ 5
    #endif
    #if !defined(IH_MAX_NUM_START_STOP_SEQ)
        #define IH_MAX_NUM_START_STOP_SEQ 5
    #endif
    #if !defined(IH_MAX_PROC_INPUT_LEN)
        #define IH_MAX_PROC_INPUT_LEN 128
    #endif
    // maximum number of memcmp ranges per command
    #if !defined(IH_MAX_PER_ROOT_MEMCMP_RANGES)
        #define IH_MAX_PER_ROOT_MEMCMP_RANGES 5
    #endif
    /*
        PGM len
    */
    #if !defined(IH_INPUT_TYPE_STRINGS_PGM_LEN)
        #define IH_INPUT_TYPE_STRINGS_PGM_LEN 10
    #endif
    // if you edit these, some examples might break and your compiler might yell at you
    #if !defined(IH_EOL_SEQ_PGM_LEN)
        #define IH_EOL_SEQ_PGM_LEN 5
    #endif
    #if !defined(IH_DELIM_SEQ_PGM_LEN)
        #define IH_DELIM_SEQ_PGM_LEN 5
    #endif
    #if !defined(IH_START_STOP_SEQ_PGM_LEN)
        #define IH_START_STOP_SEQ_PGM_LEN 5
    #endif
    #if !defined(IH_PROCESS_NAME_PGM_LEN)
        #define IH_PROCESS_NAME_PGM_LEN 12
    #endif
    #if !defined(IH_INPUT_CONTROL_CHAR_SEQ_PGM_LEN)
        #define IH_INPUT_CONTROL_CHAR_SEQ_PGM_LEN 3
    #endif
    #if !defined(IH_WCC_SEQ_PGM_LEN)
        #define IH_WCC_SEQ_PGM_LEN 2
    #endif
    /*
        library output
        true == ON; false == OFF
    */
    /**
     * @var IH_ECHO_ONLY
     *
     * Enable this option to change the library's output to echo only.
     * It will only echo what was entered and indicate where the input error is.
     */
    #if !defined(IH_ECHO_ONLY)
        #define IH_ECHO_ONLY false
    #endif
    /**
     * @var IH_VERBOSE
     *
     * Enable this option to change the library's output to verbose.
     * Puts additional command information in the output buffer.
     */
    #if !defined(IH_VERBOSE)
        #define IH_VERBOSE true
    #endif
    /*
        DEBUGGING
        switch these on/off by commenting/uncommenting the #define
    */
    /**
     * @var DEBUG_GETCOMMANDFROMSTREAM
     *
     * Enable this option to debug Input::getCommandFromStream
     */
    #if !defined(DEBUG_GETCOMMANDFROMSTREAM)
        #define DEBUG_GETCOMMANDFROMSTREAM false
    #endif
    /**
     * @var DEBUG_READCOMMANDFROMBUFFER
     *
     * Enable this option to debug Input::readCommandFromBuffer
     */
    #if !defined(DEBUG_READCOMMANDFROMBUFFER)
        #define DEBUG_READCOMMANDFROMBUFFER false
    #endif
    /**
     * @var DEBUG_GET_TOKEN
     *
     * Enable this option to debug Input::getToken
     */
    #if !defined(DEBUG_GET_TOKEN)
        #define DEBUG_GET_TOKEN false
    #endif
    /**
     * @var DEBUG_SUBCOMMAND_SEARCH
     *
     * Enable this option to debug Input::launchLogic subcommand search; subcommand search is
     * recursive, uses no local variables and passes a Input::_rcfbprm object by reference to
     * itself.
     */
    #if !defined(DEBUG_SUBCOMMAND_SEARCH)
        #define DEBUG_SUBCOMMAND_SEARCH false
    #endif
    /**
     * @var DEBUG_ADDCOMMAND
     *
     * Enable this option to debug Input::addCommand
     */
    #if !defined(DEBUG_ADDCOMMAND)
        #define DEBUG_ADDCOMMAND false
    #endif
    /**
     * @var DEBUG_LAUNCH_LOGIC
     *
     * Enable this option to debug Input::launchLogic
     */
    #if !defined(DEBUG_LAUNCH_LOGIC)
        #define DEBUG_LAUNCH_LOGIC false
    #endif
    /**
     * @var DEBUG_LAUNCH_FUNCTION
     *
     * Enable this option to debug Input::launchFunction
     */
    #if !defined(DEBUG_LAUNCH_FUNCTION)
        #define DEBUG_LAUNCH_FUNCTION false
    #endif
    /**
     * @var DEBUG_INCLUDE_FREERAM
     *
     * Enable to debug src/utility/freeRam.h; only applicable if you are using freeRam.
     */
    #if !defined(DEBUG_INCLUDE_FREERAM)
        #define DEBUG_INCLUDE_FREERAM false
    #endif

    /*
        OPTIONAL METHODS
    */
    // public methods
    /**
     * @var DISABLE_listSettings
     *
     * Enable this option to disable Input::listSettings()
     */
    #if !defined(DISABLE_listSettings)
        #define DISABLE_listSettings false
    #endif
    /**
     * @var DISABLE_listCommands
     *
     * Enable this option to disable Input::listCommands
     */
    #if !defined(DISABLE_listCommands)
        #define DISABLE_listCommands false
    #endif
    /**
     * @var DISABLE_getCommandFromStream
     *
     * Enable this option to disable Input::getCommandFromStream
     */
    #if !defined(DISABLE_getCommandFromStream)
        #define DISABLE_getCommandFromStream false
    #endif
    /**
     * @var DISABLE_nextArgument
     *
     * Enable this option to disable Input::nextArgument, either this or Input::getArgument
     * are required to retrieve arguments.
     */
    #if !defined(DISABLE_nextArgument)
        #define DISABLE_nextArgument false
    #endif
    /**
     * @var DISABLE_getArgument
     *
     * Enable this option to disable Input::getArgument method, either this or
     * Input::nextArgument need to be enabled to retrieve arguments.
     */
    #if !defined(DISABLE_getArgument)
        #define DISABLE_getArgument false
    #endif
    /**
     * @var DISABLE_outputIsAvailable
     *
     * Enable this option to disable the output available flag.
     */
    #if !defined(DISABLE_outputIsAvailable)
        #define DISABLE_outputIsAvailable false
    #endif
    /**
     * @var DISABLE_outputIsEnabled
     *
     * Enable this option to disable Input::outputIsEnabled
     */
    #if !defined(DISABLE_outputIsEnabled)
        #define DISABLE_outputIsEnabled false
    #endif
    /**
     * @var DISABLE_outputToStream
     *
     * Enable this option to reduce codesize if you are only using
     * Input::readCommandFromBuffer. Default is false.
     */
    #if !defined(DISABLE_outputToStream)
        #define DISABLE_outputToStream false
    #endif
    /**
     * @var DISABLE_clearOutputBuffer
     *
     * Only disable this method if you have already disabled output.
     * Enable this option to disable Input::clearOutputBuffer()
     * Default is false.
     */
    #if !defined(DISABLE_clearOutputBuffer)
        #define DISABLE_clearOutputBuffer false
    #endif
    // private methods
    /**
     * @var DISABLE_readCommandFromBufferErrorOutput
     *
     * Enable this option to disable the library's error output.
     * Default is false.
     */
    #if !defined(DISABLE_readCommandFromBufferErrorOutput)
        #define DISABLE_readCommandFromBufferErrorOutput false
    #endif
    /**
     * @var DISABLE_ihout
     *
     * Enable this option to completely remove output functionality at buildtime from the library.
     * Default is false.
     */
    #if !defined(DISABLE_ihout)
        #define DISABLE_ihout false
    #endif
#endif // end include guard
// end of file
